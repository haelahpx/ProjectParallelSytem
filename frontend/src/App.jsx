import AnimeSearch from "./AnimeSearch";
import TopAnime from './TopAnime';

function App() {
  return (
    <div className="container mx-auto p-4">
      <div className="min-h-screen bg-gray-100">
        <AnimeSearch />
        <TopAnime />
      </div>
    </div>
  );
}

export default App;
