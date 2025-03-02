from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from elasticsearch_dsl import Search, Q
from elasticsearch.helpers import bulk

from app.core.elasticsearch import es_client, ARBITRAGE_INDEX_MAPPING
from app.core.config import settings
from app.models.arbitrage import ArbitrageCase
from app.schemas.arbitrage import ArbitrageCaseSearch

class SearchService:
    def __init__(self):
        self.index_name = f"{settings.ELASTICSEARCH_INDEX_PREFIX}_arbitrage"
        self.client = es_client

    async def create_index(self) -> None:
        """Создает индекс с нужным маппингом."""
        if not self.client.indices.exists(index=self.index_name):
            self.client.indices.create(
                index=self.index_name,
                body=ARBITRAGE_INDEX_MAPPING
            )

    def _prepare_case_for_indexing(self, case: ArbitrageCase) -> Dict[str, Any]:
        """Подготавливает данные для индексации."""
        return {
            "id": str(case.id),
            "status": case.status,
            "created_at": case.created_at.isoformat(),
            "updated_at": case.updated_at.isoformat(),
            "person": {
                "first_name": case.person.first_name,
                "last_name": case.person.last_name,
                "middle_name": case.person.middle_name
            },
            "nicknames": [
                {
                    "nickname": n.nickname,
                    "room": n.room.name,
                    "discipline": n.discipline.name
                } for n in case.nicknames
            ],
            "contacts": [
                {
                    "type": c.type,
                    "value": c.value
                } for c in case.contacts
            ],
            "address": {
                "country": case.address.country if case.address else None,
                "city": case.address.city if case.address else None,
                "street": case.address.street if case.address else None
            } if case.address else None,
            "incidents": [
                {
                    "type": i.type,
                    "description": i.description,
                    "amount": float(i.amount) if i.amount else None,
                    "currency": i.currency
                } for i in case.incidents
            ]
        }

    async def index_case(self, case: ArbitrageCase) -> None:
        """Индексирует один арбитражный случай."""
        doc = self._prepare_case_for_indexing(case)
        self.client.index(
            index=self.index_name,
            id=str(case.id),
            body=doc
        )

    async def bulk_index_cases(self, cases: List[ArbitrageCase]) -> None:
        """Массовая индексация арбитражных случаев."""
        actions = [
            {
                "_index": self.index_name,
                "_id": str(case.id),
                "_source": self._prepare_case_for_indexing(case)
            }
            for case in cases
        ]
        bulk(self.client, actions)

    async def search(
        self,
        search_params: ArbitrageCaseSearch,
        skip: int = 0,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Выполняет поиск по арбитражным случаям."""
        s = Search(using=self.client, index=self.index_name)

        # Базовый поиск по всем полям
        if search_params.query:
            s = s.query(
                Q("multi_match",
                  query=search_params.query,
                  fields=[
                      "person.first_name^3",
                      "person.first_name.russian^2",
                      "person.last_name^3",
                      "person.last_name.russian^2",
                      "person.middle_name^2",
                      "person.middle_name.russian^2",
                      "nicknames.nickname^3",
                      "contacts.value^2",
                      "address.country",
                      "address.city",
                      "incidents.description"
                  ],
                  type="best_fields",
                  fuzziness="AUTO"
                )
            )

        # Фильтры по датам
        if search_params.date_from:
            s = s.filter("range", created_at={"gte": search_params.date_from})
        if search_params.date_to:
            s = s.filter("range", created_at={"lte": search_params.date_to})

        # Фильтры по сумме
        if search_params.amount_from or search_params.amount_to:
            range_params = {}
            if search_params.amount_from:
                range_params["gte"] = search_params.amount_from
            if search_params.amount_to:
                range_params["lte"] = search_params.amount_to
            s = s.filter("nested", path="incidents", query=Q("range", incidents__amount=range_params))

        # Фильтры по румам и дисциплинам
        if search_params.rooms:
            s = s.filter("nested", path="nicknames", query=Q("terms", nicknames__room=search_params.rooms))
        if search_params.disciplines:
            s = s.filter("nested", path="nicknames", query=Q("terms", nicknames__discipline=search_params.disciplines))

        # Пагинация
        s = s[skip:skip + limit]

        # Выполняем поиск
        response = s.execute()
        
        return [hit.to_dict() for hit in response]

search_service = SearchService() 