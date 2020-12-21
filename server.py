import json

from aiohttp import web

MAX_WEIGHT = 100  # by def
MIN_WEIGHT = 50  # by def


async def process_pokemon_handler(request):
    pokemon = json.loads(await request.text())

    valid, field = check_required_field(pokemon)
    if not valid:
        raise web.HTTPBadRequest(text=f'Missed required field: "{field}"')

    new_name = change_pokemon_name(pokemon)
    data = {
        'name': new_name,
        'id': pokemon['id']
    }
    return web.json_response(data)


def check_required_field(pokemon):
    for field in ['weight', 'name', 'id']:
        if field not in pokemon:
            return False, field
    return True, None


def change_pokemon_name(pokemon):
    weight = pokemon['weight']
    name = pokemon['name']
    if weight > MAX_WEIGHT:
        new_name = f"{name}_the_boss"
    elif weight < MIN_WEIGHT:
        new_name = f"like_a_feather_{name}"
    else:
        new_name = name
    return new_name


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.post('/', process_pokemon_handler)])
    web.run_app(app)
