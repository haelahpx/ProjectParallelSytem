import { useEffect, useState } from "react";

function TopAnime() {
    const [animeList, setAnimeList] = useState([]);

    useEffect(() => {
        fetch("http://localhost:8000/anime")
            .then(res => res.json())
            .then(data => {
                console.log(data);
                setAnimeList(data.results);  // ✅ pakai data.results sesuai API kamu
            });
    }, []);

    return (
        <div>
            <h1 className="text-2xl font-bold mb-4">Top Anime</h1>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {animeList.map((anime, index) => (
                    <div key={index} className="bg-white p-4 rounded shadow">
                        <img src={anime.image} alt={anime.title} className="w-full h-auto" />
                        <h2 className="mt-2 font-semibold">{anime.title}</h2>
                        <p className="text-sm">{anime.synopsis?.slice(0, 100)}...</p>
                        <p className="text-yellow-500 font-bold">⭐ {anime.score}</p>
                        <a href={anime.url} target="_blank" rel="noopener noreferrer" className="text-blue-600">
                            View
                        </a>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default TopAnime;
