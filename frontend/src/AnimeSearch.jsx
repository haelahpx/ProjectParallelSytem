import { useState } from "react";

function AnimeSearch() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);

    const searchAnime = async () => {
        if (!query.trim()) return;

        setLoading(true);
        try {
            const response = await fetch(`http://localhost:8000/search-anime?q=${query}`);
            const data = await response.json();
            setResults(data.results || []);
        } catch (err) {
            console.error("Gagal fetch:", err);
        }
        setLoading(false);
    };

    return (
        <div className="max-w-4xl mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4 text-center">Cari Anime 🎌</h1>

            <div className="flex gap-2 mb-6">
                <input
                    type="text"
                    placeholder="Contoh: naruto"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    className="flex-grow p-2 border rounded"
                />
                <button
                    onClick={searchAnime}
                    className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                >
                    Cari
                </button>
            </div>

            {loading && <p className="text-center">🔄 Mencari...</p>}

            <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
                {results.map((anime, index) => (
                    <div key={index} className="bg-white rounded shadow p-3">
                        <img src={anime.image} alt={anime.title} className="w-full h-60 object-cover rounded" />
                        <h2 className="text-xl font-semibold mt-2">{anime.title}</h2>
                        <p className="text-sm text-gray-600 line-clamp-3">{anime.synopsis}</p>
                        <p className="text-sm font-medium mt-2">⭐ {anime.score}</p>
                        <a
                            href={anime.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-500 text-sm"
                        >
                            Lihat di MyAnimeList
                        </a>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default AnimeSearch;
