from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import aiohttp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def format_anime(item):
    genres = [genre["name"] for genre in item.get("genres", [])]
    return {
        "mal_id": item["mal_id"],
        "title": item["title"],
        "image": item["images"]["jpg"]["image_url"],
        "synopsis": item.get("synopsis", ""),
        "score": item.get("score", 0),
        "url": item["url"],
        "genres": genres,
        "year": item.get("year", item.get("aired", {}).get("prop", {}).get("from", {}).get("year")), 
        "status": item.get("status"),
        "episodes": item.get("episodes"),
        "rank": item.get("rank"),
        "members": item.get("members"),
        "popularity": item.get("popularity"),
        "type": item.get("type"),
        "rating": item.get("rating"),
        "duration": item.get("duration")
    }

@app.get("/anime/top")
async def get_top_anime():
    """
    Fetches the top anime from Jikan API.
    """
    url = "https://api.jikan.moe/v4/top/anime"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status() 
            data = await response.json()
            results = [format_anime(anime) for anime in data.get("data", [])]
            return {"results": results}

@app.get("/anime") 
async def get_general_anime():
    """
    Fetches general top anime, primarily used for 'Top Rated' section.
    This is effectively the same as /anime/top but allows for a more general endpoint.
    """
    url = "https://api.jikan.moe/v4/top/anime"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            results = [format_anime(anime) for anime in data.get("data", [])]
            return {"results": results}

@app.get("/anime/airing")
async def get_top_airing_anime():
    """
    Fetches the top airing anime from Jikan API.
    """
    url = "https://api.jikan.moe/v4/top/anime?filter=airing"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            results = [format_anime(anime) for anime in data.get("data", [])]
            return {"results": results}

@app.get("/season/{year}/{season}")
async def get_seasonal_anime(year: int, season: str):
    """
    Fetches seasonal anime for a given year and season.
    """
    valid_seasons = ["winter", "spring", "summer", "fall"]
    if season.lower() not in valid_seasons:
        raise HTTPException(status_code=400, detail=f"Invalid season. Must be one of {', '.join(valid_seasons)}")

    url = f"https://api.jikan.moe/v4/seasons/{year}/{season.lower()}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 404: 
                return {"results": []} 
            response.raise_for_status()
            data = await response.json()
            results = [format_anime(anime) for anime in data.get("data", [])]
            return {"results": results}

@app.get("/anime/{mal_id}")
async def get_anime_detail(mal_id: int):
    """
    Fetches detailed information for a specific anime by its MAL ID.
    """
    url = f"https://api.jikan.moe/v4/anime/{mal_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 404:
                raise HTTPException(status_code=404, detail="Anime not found")
            response.raise_for_status()
            data = await response.json()
            if data and "data" in data:
                return format_anime(data["data"])
            raise HTTPException(status_code=500, detail="Failed to retrieve anime details.")
        
@app.get("/search-anime")
async def search_anime(q: str = Query(..., min_length=1)):
    """
    Searches for anime by title using the Jikan API.
    """
    url = f"[https://api.jikan.moe/v4/anime?q=](https://api.jikan.moe/v4/anime?q=){q}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()  
            result = await response.json()

            anime_list = [format_anime(anime) for anime in result.get("data", [])]

            return {"results": anime_list}