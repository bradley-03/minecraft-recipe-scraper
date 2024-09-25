# minecraft-recipe-scraper

A simple Python app that fetches the latest Minecraft crafting recipes and stores them in a MongoDB database.

## Features

- Automatically retrieves the latest Minecraft crafting recipes.
- Dumps the recipes into a MongoDB collection for easy querying.
- Get recipes from latest snapshot or latest full release.

## Setup

**1. Clone the repository:**

```bash
git clone https://github.com/bradley-03/minecraft-recipe-scraper.git
cd minecraft-recipe-scraper
```

**2. Install dependencies:**

```bash
pip install -r requirements.txt
```

**3. Configure MongoDB connection:**

Setup MongoDB connection url and db name in `config.py`.

**4. Run the app:**

```bash
python main.py
```

## Configuration

All configuration options can be found in `config.py`. Edit to your liking.
