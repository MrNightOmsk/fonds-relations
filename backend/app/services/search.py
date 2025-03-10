from typing import List, Optional, Dict
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
        
        # Словарь для соответствия между формальными именами и их уменьшительными формами
        self.name_variants: Dict[str, List[str]] = {
            "василий": ["вася", "васька", "васёк", "васек", "васенька"],
            "иван": ["ваня", "ванька", "ванёк", "ванек", "ванечка"],
            "александр": ["саша", "сашка", "сашенька", "шурик"],
            "николай": ["коля", "колька", "коленька"],
            "петр": ["петя", "петька", "петенька"],
            "михаил": ["миша", "мишка", "мишенька"],
            "алексей": ["лёша", "леша", "лёшка", "лешка", "лёшенька", "лешенька"],
            "дмитрий": ["дима", "димка", "диман", "димон"],
            "сергей": ["серёжа", "сережа", "серёга", "серега"],
            "владимир": ["вова", "вовка", "вовочка", "володя", "володька"],
            "андрей": ["андрюша", "андрюшка", "андрюшенька"],
            "виктор": ["витя", "витька", "витенька"],
            "евгений": ["женя", "женька", "женечка"],
            "григорий": ["гриша", "гришка", "гриня"],
            "константин": ["костя", "костик", "костенька"],
            "валентин": ["валя", "валентинка", "валик"],
            "павел": ["паша", "пашка", "пашенька"],
            "антон": ["антошка", "антошенька"],
            "денис": ["денчик", "дениска"],
            "юрий": ["юра", "юрка", "юрик"],
            "вадим": ["вадик", "вадимка"]
        }
    
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
                                        "edge_ngram_filter",
                                        "russian_name_synonyms"
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
                                },
                                "russian_name_synonyms": {
                                    "type": "synonym",
                                    "synonyms": self._generate_name_synonyms()
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
    
    def _generate_name_synonyms(self) -> List[str]:
        """Generates synonym strings for Russian names in Elasticsearch format."""
        synonym_lines = []
        for formal_name, variants in self.name_variants.items():
            # Создаем синонимы для основного имени и всех его вариантов
            all_variants = [formal_name] + variants
            variant_str = f"{','.join(all_variants)} => {formal_name}"
            synonym_lines.append(variant_str)
            
            # Добавляем отдельные правила для каждого варианта
            for variant in variants:
                synonym_lines.append(f"{variant} => {formal_name}")
            
            # Добавляем обратное правило для поиска по формальному имени
            for variant in variants:
                synonym_lines.append(f"{formal_name} => {formal_name},{variant}")
        
        return synonym_lines
    
    async def index_player(self, player: Player) -> None:
        """Index a player in Elasticsearch."""
        try:
            # Разбиваем имя на части для улучшения поиска
            name_parts = player.full_name.split() if player.full_name else []
            first_name = name_parts[0] if name_parts else ""
            last_name = name_parts[1] if len(name_parts) > 1 else ""
            middle_name = name_parts[2] if len(name_parts) > 2 else ""
            
            # Безопасное получение количества кейсов
            cases_count = 0
            latest_case_date = None
            if hasattr(player, 'cases') and player.cases:
                cases_count = len(player.cases)
                # Безопасное получение максимальной даты кейса
                if cases_count > 0:
                    case_dates = [c.created_at for c in player.cases if hasattr(c, 'created_at') and c.created_at]
                    if case_dates:
                        latest_case_date = max(case_dates)
            
            # Безопасное получение имени фонда
            fund_name = ""
            if hasattr(player, 'created_by_fund') and player.created_by_fund:
                if hasattr(player.created_by_fund, 'name'):
                    fund_name = player.created_by_fund.name
            
            # Подготовка документа для индексации
            document = {
                "id": str(player.id),
                "full_name": player.full_name or "",
                "first_name": first_name,
                "last_name": last_name,
                "middle_name": middle_name,
                "nicknames": [
                    {
                        "room": getattr(n, 'room', ""),
                        "nickname": getattr(n, 'nickname', ""),
                        "discipline": getattr(n, 'discipline', "")
                    }
                    for n in (player.nicknames if hasattr(player, 'nicknames') and player.nicknames else [])
                ],
                "contacts": [
                    {
                        "type": getattr(c, 'type', ""),
                        "value": getattr(c, 'value', "")
                    }
                    for c in (player.contacts if hasattr(player, 'contacts') and player.contacts else [])
                ],
                "locations": [
                    {
                        "country": getattr(l, 'country', ""),
                        "city": getattr(l, 'city', ""),
                        "address": getattr(l, 'address', "")
                    }
                    for l in (player.locations if hasattr(player, 'locations') and player.locations else [])
                ],
                "cases_count": cases_count,
                "latest_case_date": latest_case_date,
                "fund_name": fund_name,
                "contacts_display": [
                    f"{getattr(c, 'type', '')}: {getattr(c, 'value', '')}" 
                    for c in (player.contacts if hasattr(player, 'contacts') and player.contacts else [])
                ],
                "locations_display": [
                    f"{getattr(l, 'city', '')}, {getattr(l, 'country', '')}" 
                    for l in (player.locations if hasattr(player, 'locations') and player.locations else [])
                    if getattr(l, 'city', '') and getattr(l, 'country', '')
                ]
            }
            
            await self.es.index(
                index=self.index_name,
                id=str(player.id),
                document=document
            )
        except Exception as e:
            # Логируем ошибку и перебрасываем исключение для обработки на уровне выше
            print(f"Ошибка при индексации игрока {player.id}: {str(e)}")
            raise
    
    async def search_players(
        self,
        query: str,
        room: Optional[str] = None,
        discipline: Optional[str] = None,
        skip: int = 0,
        limit: int = 10
    ) -> List[PlayerSearchResult]:
        """Search for players in Elasticsearch."""
        try:
            must_conditions = []
            
            # Проверяем, не является ли запрос именем или его вариантом
            is_name_query = False
            original_query = query
            query_lower = query.lower()
            
            # Ищем, является ли запрос именем или его вариантом
            for formal_name, variants in self.name_variants.items():
                if query_lower == formal_name or query_lower in variants:
                    is_name_query = True
                    # Используем формальное имя для более точного поиска
                    if query_lower in variants:
                        query = formal_name
                    break
            
            # Добавляем основной поисковый запрос с поддержкой неточного поиска
            if query:
                search_fields = ["full_name^4", "first_name^3", "last_name^3", "nicknames.nickname^2", 
                                "description", "contacts.value", "locations.city"]
                
                must_conditions.append({
                    "multi_match": {
                        "query": query,
                        "fields": search_fields,
                        "type": "best_fields",
                        "fuzziness": "AUTO",
                        "prefix_length": 1,
                        "boost": 2.0
                    }
                })
                
                # Если это поиск по имени, добавляем более специфичные условия
                if is_name_query:
                    must_conditions.append({
                        "bool": {
                            "should": [
                                {"match": {"first_name": {"query": query, "boost": 3.0}}},
                                {"match_phrase": {"full_name": {"query": query, "boost": 2.5}}}
                            ],
                            "boost": 2.0
                        }
                    })
                else:
                    # Добавляем дополнительный запрос для улучшения поиска по частичным совпадениям
                    must_conditions.append({
                        "bool": {
                            "should": [
                                {
                                    "match_phrase_prefix": {
                                        "full_name": {
                                            "query": query,
                                            "boost": 1.5
                                        }
                                    }
                                },
                                {
                                    "match_phrase_prefix": {
                                        "first_name": {
                                            "query": query,
                                            "boost": 1.2
                                        }
                                    }
                                },
                                {
                                    "match_phrase_prefix": {
                                        "last_name": {
                                            "query": query,
                                            "boost": 1.0
                                        }
                                    }
                                },
                                {
                                    "nested": {
                                        "path": "nicknames",
                                        "query": {
                                            "match_phrase_prefix": {
                                                "nicknames.nickname": {
                                                    "query": query,
                                                    "boost": 0.8
                                                }
                                            }
                                        }
                                    }
                                }
                            ],
                            "minimum_should_match": 1,
                            "boost": 1.5
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
                        {"_score": {"order": "desc"}}
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
                        first_name=source.get("first_name", ""),
                        last_name=source.get("last_name", None),
                        middle_name=source.get("middle_name", None),
                        description=source.get("description", None),
                        nicknames=source.get("nicknames", []),
                        cases_count=source.get("cases_count", 0),
                        latest_case_date=source.get("latest_case_date"),
                        fund_name=source.get("fund_name", ""),
                        contacts=source.get("contacts_display", []),
                        locations=source.get("locations_display", [])
                    )
                )
            
            return results
        except Exception as e:
            # Логируем ошибку и перебрасываем исключение для обработки на уровне выше
            print(f"Ошибка при поиске игроков: {str(e)}")
            raise
    
    async def close(self) -> None:
        """Close the Elasticsearch connection."""
        await self.es.close()


# Global instance
search_service = SearchService() 