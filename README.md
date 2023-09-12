# Pokémon API with FastAPI

This FastAPI project allows you to fetch Pokémon data from the [PokeAPI](https://pokeapi.co/) and store it in a PostgreSQL database. It also provides an API to list Pokémon and filter them by name and type.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following prerequisites installed:

- Python 3.x
- [Pip](https://pip.pypa.io/en/stable/installation/)
- [PostgreSQL](https://www.postgresql.org/download/)

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/pokemon-api.git
   cd pokemon-api
2. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS and Linux
    # or
    venv\Scripts\activate

3. Install project dependencies:
    ```bash
    pip install -r requirements.txt


4. Initialize the database schema:
    ```bash
    python main.py db init
    python main.py db migrate
    python main.py db upgrade

5. Run the FastAPI application:

    ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload

## API Endpoints


You can use the query parameters name and type to filter Pokémon by name and type, respectively. For example:

List all Pokémon: /api/v1/pokemons
Filter by name: /api/v1/pokemons?name=Pikachu
Filter by type: /api/v1/pokemons?type=Electric
Filter by both name and type: /api/v1/pokemons?name=Pikachu&type=Electric