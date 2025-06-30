from fastapi import FastAPI, Query
import aiohttp
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS agar React bisa fetch dari FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Bisa ganti ke ["http://localhost:5173"] untuk keamanan
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Anime API aktif"}

@app.get("/search-anime")
async def search_anime(q: str = Query(..., min_length=1)):
    url = f"https://api.jikan.moe/v4/anime?q={q}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.json()

            # Ambil hanya data penting
            anime_list = [
                {
                    "title": anime["title"],
                    "image": anime["images"]["jpg"]["image_url"],
                    "synopsis": anime["synopsis"],
                    "score": anime["score"],
                    "url": anime["url"],
                }
                for anime in result.get("data", [])
            ]

            return {"results": anime_list}

@app.get("/anime")
async def get_top_anime():
    url = "https://api.jikan.moe/v4/top/anime"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.json()

            anime_list = [
                {
                    "title": anime["title"],
                    "image": anime["images"]["jpg"]["image_url"],
                    "synopsis": anime["synopsis"],
                    "score": anime["score"],
                    "url": anime["url"],
                }
                for anime in result.get("data", [])
            ]

            return {"results": anime_list}
