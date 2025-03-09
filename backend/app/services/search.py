from typing import List, Optional
from uuid import UUID

from elasticsearch import AsyncElasticsearch
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.player import Player
from app.schemas.player import PlayerSearchResult


class SearchService:
    def __init__(self):
        self.es = AsyncElasticsearch([settings.ELASTICSEARCH_URL])
        self.index_name = "players"
    
    async def create_index(self) -> None:
        """Create the Elasticsearch index if it doesn't exist."""
        if not await self.es.indices.exists(index="players"):
            await self.es.indices.create(
                index="players",
                body={
                    "settings": {
                        "analysis": {
                            "analyzer": {
                                "russian_analyzer": {
                                    "type": "custom",
                                    "tokenizer": "standard",
                                    "filter": [
                                        "lowercase",
                                        "russian_stop",
                                        "russian_stemmer",
                                        "edge_ngram_filter"
                                    ]
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
                                },
                                "edge_ngram_filter": {
                                    "type": "edge_ngram",
                                    "min_gram": 2,
                                    "max_gram": 20
                                }
                            }
                        }
                    },
                    "mappings": {
                        "properties": {
                            "full_name": {
                                "type": "text",
                                "analyzer": "russian_analyzer",
                                "fields": {
                                    "raw": {"type": "keyword"}
                                }
                            },
                            "first_name": {"type": "text", "analyzer": "russian_analyzer"},
                            "last_name": {"type": "text", "analyzer": "russian_analyzer"},
                            "middle_name": {"type": "text", "analyzer": "russian_analyzer"},
                            "description": {"type": "text", "analyzer": "russian_analyzer"},
                            "nicknames": {"type": "nested", "properties": {
                                "id": {"type": "keyword"},
                                "player_id": {"type": "keyword"},
                                "nickname": {"type": "text", "analyzer": "russian_analyzer"},
                                "created_at": {"type": "date"},
                                "updated_at": {"type": "date"}
                            }},
                            "contacts": {"type": "nested", "properties": {
                                "type": {"type": "keyword"},
                                "value": {"type": "text", "fields": {"raw": {"type": "keyword"}}}
                            }},
                            "locations": {"type": "nested", "properties": {
                                "country": {"type": "keyword"},
                                "city": {"type": "text", "fields": {"raw": {"type": "keyword"}}}
                            }},
                            "cases_count": {"type": "integer"},
                            "open_cases_count": {"type": "integer"},
                            "latest_case_date": {"type": "date"},
                            "fund_name": {"type": "text", "fields": {"raw": {"type": "keyword"}}},
                            "contacts_display": {"type": "text"},
                            "locations_display": {"type": "text"}
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
                    "type": c.type,
                    "value": c.value
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
        """Search for players based on the query."""
        must_conditions = []
        
        # Добавляем основной поисковый запрос с поддержкой неточного поиска
        if query:
            must_conditions.append({
                "multi_match": {
                    "query": query,
                    "fields": ["full_name^3", "nicknames.nickname^2", 
                               "first_name", "last_name", "description", 
                               "contacts.value", "locations.city"],
                    "type": "best_fields",
                    "fuzziness": "AUTO",
                    "prefix_length": 1
                }
            })
        
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
                    first_name=source["full_name"].split()[0] if source["full_name"] else "",
                    last_name=source.get("last_name", None),
                    middle_name=source.get("middle_name", None),
                    description=source.get("description", None),
                    nicknames=[],
                    cases_count=source["cases_count"],
                    latest_case_date=source.get("latest_case_date"),
                    fund_name=source.get("fund_name", ""),
                    contacts=source.get("contacts_display", []),
                    locations=source.get("locations_display", [])
                )
            )
        
        return results
    
    async def close(self) -> None:
        """Close the Elasticsearch connection."""
        await self.es.close()


# Global instance
search_service = SearchService() 