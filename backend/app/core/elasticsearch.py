from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from app.core.config import settings

# Создаем клиент Elasticsearch
es_client = Elasticsearch(
    hosts=[{
        'host': settings.ELASTICSEARCH_HOST,
        'port': settings.ELASTICSEARCH_PORT,
        'scheme': settings.ELASTICSEARCH_SCHEME
    }],
    basic_auth=(
        settings.ELASTICSEARCH_USER,
        settings.ELASTICSEARCH_PASSWORD
    ) if settings.ELASTICSEARCH_USER else None
)

# Определяем маппинг для индекса
ARBITRAGE_INDEX_MAPPING = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "status": {"type": "keyword"},
            "created_at": {"type": "date"},
            "updated_at": {"type": "date"},
            "person": {
                "properties": {
                    "first_name": {
                        "type": "text",
                        "analyzer": "standard",
                        "fields": {
                            "keyword": {"type": "keyword"},
                            "russian": {"type": "text", "analyzer": "russian"}
                        }
                    },
                    "last_name": {
                        "type": "text",
                        "analyzer": "standard",
                        "fields": {
                            "keyword": {"type": "keyword"},
                            "russian": {"type": "text", "analyzer": "russian"}
                        }
                    },
                    "middle_name": {
                        "type": "text",
                        "analyzer": "standard",
                        "fields": {
                            "keyword": {"type": "keyword"},
                            "russian": {"type": "text", "analyzer": "russian"}
                        }
                    }
                }
            },
            "nicknames": {
                "type": "nested",
                "properties": {
                    "nickname": {"type": "keyword"},
                    "room": {"type": "keyword"},
                    "discipline": {"type": "keyword"}
                }
            },
            "contacts": {
                "type": "nested",
                "properties": {
                    "type": {"type": "keyword"},
                    "value": {"type": "keyword"}
                }
            },
            "address": {
                "properties": {
                    "country": {
                        "type": "text",
                        "fields": {
                            "keyword": {"type": "keyword"},
                            "russian": {"type": "text", "analyzer": "russian"}
                        }
                    },
                    "city": {
                        "type": "text",
                        "fields": {
                            "keyword": {"type": "keyword"},
                            "russian": {"type": "text", "analyzer": "russian"}
                        }
                    },
                    "street": {
                        "type": "text",
                        "fields": {
                            "keyword": {"type": "keyword"},
                            "russian": {"type": "text", "analyzer": "russian"}
                        }
                    }
                }
            },
            "incidents": {
                "type": "nested",
                "properties": {
                    "type": {"type": "keyword"},
                    "description": {
                        "type": "text",
                        "analyzer": "standard",
                        "fields": {
                            "russian": {"type": "text", "analyzer": "russian"}
                        }
                    },
                    "amount": {"type": "float"},
                    "currency": {"type": "keyword"}
                }
            }
        }
    },
    "settings": {
        "analysis": {
            "analyzer": {
                "russian": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "russian_stop",
                        "russian_stemmer"
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
                }
            }
        }
    }
} 