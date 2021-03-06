import allure
import pytest
from aiohttp import web

from server import process_pokemon_handler, change_pokemon_name, check_required_field

MOCK_POKEMON_REQUEST_DATA = """{
    "id": 18, 
    "name": "pidgeot", 
    "types": [
        {"slot": 1, "type": {"name": "normal", "url": "https://pokeapi.co/api/v2/type/1/"}},
        {"slot": 2, "type": {"name": "flying", "url": "https://pokeapi.co/api/v2/type/3/"}}
    ],
    "weight": 395}"""

MOCK_POKEMON_REQUEST_DATA_BAD_REQUEST = """{
    "name": "pidgeot", 
    "types": [
        {"slot": 1, "type": {"name": "normal", "url": "https://pokeapi.co/api/v2/type/1/"}},
        {"slot": 2, "type": {"name": "flying", "url": "https://pokeapi.co/api/v2/type/3/"}}
    ],
    "weight": 395}"""


@pytest.fixture
def cli(loop, aiohttp_client):
    app = web.Application()
    app.router.add_post('/', process_pokemon_handler)
    return loop.run_until_complete(aiohttp_client(app))


@allure.feature('Method "process_pokemon_handler"')
@allure.story('Handler works correct')
@allure.severity("blocker")
async def test_process_pokemon_handler(cli):
    resp = await cli.post('/', data=MOCK_POKEMON_REQUEST_DATA)

    with allure.step("Check status code"):
        assert resp.status == 200
    with allure.step("Check text response"):
        assert await resp.text() == '{"name": "pidgeot_the_boss", "id": 18}'


@allure.feature('Method "process_pokemon_handler"')
@allure.story('Handler return BAD REQUEST')
@allure.severity("blocker")
async def test_process_pokemon_handler_bad_request(cli):
    resp = await cli.post('/', data=MOCK_POKEMON_REQUEST_DATA_BAD_REQUEST)

    with allure.step("Check status code"):
        assert resp.status == 400
    with allure.step("Check text response"):
        assert await resp.text() == 'Missed required field: "id"'


@allure.feature('Name changing')
@allure.story('Name change for a boss pokemon')
@allure.severity("critical")
def test_change_pokemon_name_boss():
    pokemon = {"id": 18, "name": "pidgeot", "weight": 395}
    assert change_pokemon_name(pokemon) == "pidgeot_the_boss"


@allure.feature('Name changing')
@allure.story('Name change for a little pokemon')
@allure.severity("critical")
def test_change_pokemon_name_feather():
    pokemon = {"id": 18, "name": "pidgeot", "weight": 40}
    assert change_pokemon_name(pokemon) == "like_a_feather_pidgeot"


@allure.feature('Name changing')
@allure.story('Name does not change')
@allure.severity("critical")
def test_change_pokemon_name_normal():
    pokemon = {"id": 18, "name": "pidgeot", "weight": 51}
    assert change_pokemon_name(pokemon) == "pidgeot"


@allure.feature('Checking for required fields')
@allure.story('All required fields are present')
@allure.severity("critical")
def test_check_required_field():
    pokemon = {"id": 18, "name": "pidgeot", "weight": 395}
    valid, field = check_required_field(pokemon)
    assert valid
    assert field is None


@allure.feature('Checking for required fields')
@allure.story('Missing field "name"')
@allure.severity("critical")
def test_check_required_field_no_name():
    pokemon = {"id": 18, "weight": 395}
    valid, field = check_required_field(pokemon)
    assert not valid
    assert field == "name"


@allure.feature('Checking for required fields')
@allure.story('Missing field "id"')
@allure.severity("critical")
def test_check_required_field_no_id():
    pokemon = {"name": "pidgeot", "weight": 395}
    valid, field = check_required_field(pokemon)
    assert not valid
    assert field == "id"