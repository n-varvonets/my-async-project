# -*- coding: utf-8 -*-
import requests
import asyncio
import aiohttp

from logger import init_logger

BL_TYPES = ['grass', 'fire']  # by condition of task
POKEMON_API_URL = 'https://pokeapi.co/api/v2/pokemon'
limit = 50  # by condition
offset = 0  # by def (from which pok start count)
SERVER_URL = 'http://localhost:8080'


async def send_data(pokemon, session):
    async with session.post(SERVER_URL, json=pokemon) as resp:
        return await resp.json()


async def get_pokemon(pokemon, session):
    async with session.get(pokemon['url']) as response:
        pokemon = await response.json()

        poke_types = pokemon['types']
        if len(poke_types) > 1:
            for pokemon_type in poke_types:
                if pokemon_type['type']['name'] in BL_TYPES:
                    return
        log.info(f"Pokemon ID {pokemon['id']} | Pokemon name: {pokemon['name']}")
        received_pokemon = await send_data(pokemon, session)
        return received_pokemon


async def main():
    url = f'{POKEMON_API_URL}?limit={limit}&offset={offset}'
    pokemons_data = requests.get(url).json()

    async with aiohttp.ClientSession() as session:
        tasks = [loop.create_task(get_pokemon(pokemon, session)) for pokemon in pokemons_data['results']]
        result = await asyncio.gather(*tasks)


if __name__ == '__main__':
    log = init_logger('processing_pokemon', 'processing_pokemon')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
