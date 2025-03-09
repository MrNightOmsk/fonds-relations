#!/usr/bin/env python3
import asyncio
from app.services.search import SearchService

async def main():
    search = SearchService()
    query = 'васи'
    results = await search.search_players(query)
    print(f'Найдено игроков для запроса "{query}": {len(results)}')
    for i, player in enumerate(results[:10]):
        print(f'{i+1}. {player.full_name}')
    await search.close()

if __name__ == "__main__":
    asyncio.run(main()) 