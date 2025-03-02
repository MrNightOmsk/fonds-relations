from typing import List, Optional
from uuid import UUID

from elasticsearch import AsyncElasticsearch
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.player import Player
from app.schemas.player import PlayerSearchResult


class SearchService:
    def __init__(self):
        self.es = AsyncElasticsearch([settings.ELASTICSEARCH_URI])
        self.index_name = "players"
    
    async def create_index(self) -> None:
        """Create the Elasticsearch index with proper mappings."""
        if not await self.es.indices.exists(index=self.index_name):
            await self.es.indices.create(
                index=self.index_name,
                body={
                    "settings": {
                        "analysis": {
                            "analyzer": {
                                "custom_analyzer": {
                                    "type": "custom",
                                    "tokenizer": "standard",
                                    "filter": ["lowercase", "russian_stop", "russian_stemmer"],
                                }
                            },
                            "filter": {
                                "russian_stop": {
                                    "type": "stop",
                                    "stopwords": "_russian_"
                                },
                                "russian_stemmer": {
                                    "type": "stemmer",
                                    "language": "russian"
                                }
                            }
                        }
                    },
                    "mappings": {
                        "properties": {
                            "id": {"type": "keyword"},
                            "full_name": {
                                "type": "text",
                                "analyzer": "custom_analyzer",
                                "fields": {
                                    "raw": {"type": "keyword"}
                                }
                            },
                            "nicknames": {
                                "type": "nested",
                                "properties": {
                                    "room": {"type": "keyword"},
                                    "nickname": {
                                        "type": "text",
                                        "analyzer": "custom_analyzer",
                                        "fields": {
                                            "raw": {"type": "keyword"}
                                        }
                                    },
                                    "discipline": {"type": "keyword"}
                                }
                            },
                            "contacts": {
                                "type": "nested",
                                "properties": {
                                    "type": {"type": "keyword"},
                                    "value": {
                                        "type": "text",
                                        "analyzer": "custom_analyzer",
                                        "fields": {
                                            "raw": {"type": "keyword"}
                                        }
                                    }
                                }
                            },
                            "locations": {
                                "type": "nested",
                                "properties": {
                                    "country": {
                                        "type": "text",
                                        "analyzer": "custom_analyzer",
                                        "fields": {
                                            "raw": {"type": "keyword"}
                                        }
                                    },
                                    "city": {
                                        "type": "text",
                                        "analyzer": "custom_analyzer",
                                        "fields": {
                                            "raw": {"type": "keyword"}
                                        }
                                    },
                                    "address": {
                                        "type": "text",
                                        "analyzer": "custom_analyzer"
                                    }
                                }
                            },
                            "cases_count": {"type": "integer"},
                            "latest_case_date": {"type": "date"}
                        }
                    }
                }
            )
    
    async def index_player(self, player: Player) -> None:
        """Index a player in Elasticsearch."""
        document = {
            "id": str(player.id),
            "full_name": player.full_name,
            "nicknames": [
                {
                    "room": n.room,
                    "nickname": n.nickname,
                    "discipline": n.discipline
                }
                for n in player.nicknames
            ],
            "contacts": [
                {
                    "type": c.contact_type,
                    "value": c.contact_value
                }
                for c in player.contacts
            ],
            "locations": [
                {
                    "country": l.country,
                    "city": l.city,
                    "address": l.address
                }
                for l in player.locations
            ],
            "cases_count": len(player.cases),
            "latest_case_date": max(c.created_at for c in player.cases) if player.cases else None
        }
        
        await self.es.index(
            index=self.index_name,
            id=str(player.id),
            document=document
        )
    
    async def search_players(
        self,
        query: str,
        room: Optional[str] = None,
        discipline: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[PlayerSearchResult]:
        """
        Search for players using various criteria.
        
        Args:
            query: Search query string
            room: Filter by poker room
            discipline: Filter by game discipline
            skip: Number of results to skip
            limit: Maximum number of results to return
        """
        # Build the search query
        must_conditions = [
            {
                "multi_match": {
                    "query": query,
                    "fields": [
                        "full_name^3",
                        "nicknames.nickname^2",
                        "contacts.value",
                        "locations.country",
                        "locations.city",
                        "locations.address"
                    ],
                    "type": "best_fields",
                    "fuzziness": "AUTO"
                }
            }
        ]
        
        if room:
            must_conditions.append({
                "nested": {
                    "path": "nicknames",
                    "query": {
                        "term": {"nicknames.room": room}
                    }
                }
            })
        
        if discipline:
            must_conditions.append({
                "nested": {
                    "path": "nicknames",
                    "query": {
                        "term": {"nicknames.discipline": discipline}
                    }
                }
            })
        
        # Execute the search
        response = await self.es.search(
            index=self.index_name,
            body={
                "query": {"bool": {"must": must_conditions}},
                "sort": [
                    {"_score": {"order": "desc"}},
                    {"latest_case_date": {"order": "desc"}}
                ],
                "from": skip,
                "size": limit
            }
        )
        
        # Convert results to schema objects
        results = []
        for hit in response["hits"]["hits"]:
            source = hit["_source"]
            results.append(
                PlayerSearchResult(
                    id=UUID(source["id"]),
                    full_name=source["full_name"],
                    nicknames=source["nicknames"],
                    cases_count=source["cases_count"],
                    latest_case_date=source.get("latest_case_date")
                )
            )
        
        return results
    
    async def close(self) -> None:
        """Close the Elasticsearch connection."""
        await self.es.close()


# Global instance
search_service = SearchService() 