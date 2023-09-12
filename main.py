# main.py
from fastapi import FastAPI
from tortoise import Tortoise, fields, models
from tortoise.models import Model
from tortoise.transactions import in_transaction
import httpx
from decouple import config
from fastapi import FastAPI, Query

app = FastAPI()

# Replace these with your actual database connection settings
DATABASE_URL = config('DATABASE_URL')


# Define your database models
class Pokemon(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    image_url = fields.CharField(max_length=255)
    type = fields.CharField(max_length=255)


async def init():
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={"models": ["main"]},
    )
    await Tortoise.generate_schemas()


@app.on_event("startup")
async def startup_db_client():
    await init()


@app.on_event("shutdown")
async def shutdown_db_client():
    await Tortoise.close_connections()


@app.get("/fetch_and_store_pokemons")
async def fetch_and_store_pokemons():
    async with httpx.AsyncClient() as client:
        # Fetch the list of Pokémon from the PokeAPI
        response = await client.get("https://pokeapi.co/api/v2/pokemon?limit=100")

        if response.status_code == 200:
            data = response.json()["results"]

            async with in_transaction() as transaction:
                for item in data:
                    pokemon_details = await client.get(item["url"])
                    pokemon_data = pokemon_details.json()

                    # Extract relevant data
                    name = pokemon_data["name"]
                    image_url = pokemon_data["sprites"]["front_default"]
                    types = [t["type"]["name"] for t in pokemon_data["types"]]
                    type_str = ", ".join(types)

                    # Store the Pokémon data in the database
                    await Pokemon.create(name=name, image_url=image_url, type=type_str)

    return {"message": "Pokémon data fetched and stored successfully!"}


@app.get("/api/v1/pokemons")
async def list_pokemons(
        name: str = Query(None),
        type: str = Query(None),
):
    # Query the database and filter Pokémon based on the provided name and type parameters
    query = Pokemon.all()

    if name:
        query = query.filter(name__icontains=name)

    if type:
        query = query.filter(type__icontains=type)

    pokemons = await query.all()

    # Create a list of dictionaries to return as JSON
    pokemon_list = [{"name": p.name, "image_url": p.image_url, "type": p.type} for p in pokemons]

    return {"pokemons": pokemon_list}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
