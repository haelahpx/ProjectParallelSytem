<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
// Navbar is now in App.vue, so no need to import it here unless specific to this page
// import Navbar from '../components/navbar.vue'; // Removed, handled by App.vue

// Define the detailed anime interface based on Jikan API response for a single anime
interface AnimeDetail {
    mal_id: number;
    title: string;
    images: {
        jpg: {
            image_url: string;
            large_image_url: string;
        };
    };
    synopsis: string;
    score: number;
    url: string;
    genres: { mal_id: number; type: string; name: string }[]; // Jikan returns objects for genres
    year: number;
    status: string;
    episodes: number;
    aired: {
        from: string;
        to: string | null;
        prop: {
            from: { day: number; month: number; year: number };
            to: { day: number | null; month: number | null; year: number | null };
        };
        string: string;
    };
    studios: { mal_id: number; type: string; name: string; url: string }[]; // Jikan returns objects for studios
    trailer: {
        youtube_id: string | null;
        url: string | null;
        embed_url: string | null;
        images: {
            image_url: string | null;
            small_image_url: string | null;
            medium_image_url: string | null;
            large_image_url: string | null;
            maximum_image_url: string | null;
        };
    };
    rank: number;
    popularity: number;
    members: number;
    favorites: number;
    type: string;
    source: string;
    rating: string;
    duration: string;
    season: string;
}

const route = useRoute();
const anime = ref<AnimeDetail | null>(null);
const loading = ref(true);
const error = ref<string | null>(null);

const fetchAnimeDetails = async (id: string) => {
    try {
        loading.value = true;
        error.value = null;

        const response = await fetch(`http://localhost:8000/anime/${id}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        if (data.data) {
            anime.value = data.data;
        } else {
            throw new Error('Anime data not found.');
        }
    } catch (err) {
        console.error('Error fetching anime details:', err);
        error.value = err instanceof Error ? err.message : 'Failed to load anime details. Please try again later.';
    } finally {
        loading.value = false;
    }
};

const getRatingColor = (score: number) => {
    if (score >= 9) return 'bg-green-500';
    if (score >= 8) return 'bg-yellow-500';
    if (score >= 7) return 'bg-orange-500';
    return 'bg-red-500';
};

const formatGenres = (genres: { name: string }[] | undefined) => {
    if (!genres || genres.length === 0) return 'Unknown';
    return genres.map(genre => genre.name).join(', ');
};

const handleImageError = (event: Event) => {
    const target = event.target as HTMLImageElement;
    target.src = 'https://via.placeholder.com/300x400?text=No+Image';
};

onMounted(() => {
    const animeId = route.params.id;
    if (animeId) {
        fetchAnimeDetails(animeId as string);
    } else {
        error.value = "No anime ID provided.";
        loading.value = false;
    }
});
</script>

<template>
    <div class="py-12">
        <div v-if="loading" class="flex justify-center items-center min-h-[calc(100vh-80px)]">
            <div class="text-center">
                <div class="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500 mx-auto"></div>
                <p class="mt-4 text-lg">Loading anime details...</p>
            </div>
        </div>

        <div v-else-if="error" class="flex justify-center items-center min-h-[calc(100vh-80px)]">
            <div class="text-center">
                <div class="text-red-400 text-lg mb-4">
                    <svg class="w-16 h-16 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z">
                        </path>
                    </svg>
                    {{ error }}
                </div>
            </div>
        </div>

        <div v-else-if="anime" class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="md:col-span-1">
                    <img :src="anime.images.jpg.large_image_url || anime.images.jpg.image_url" :alt="anime.title"
                        class="w-full rounded-lg shadow-lg" @error="handleImageError">
                    <div :class="getRatingColor(anime.score || 0)"
                        class="mt-4 text-white px-3 py-1 rounded-full text-lg font-bold text-center">
                        Score: {{ anime.score ? anime.score.toFixed(2) : 'N/A' }}
                    </div>
                </div>

                <div class="md:col-span-2">
                    <h1 class="text-4xl font-bold mb-4">{{ anime.title }}</h1>

                    <div class="flex flex-wrap gap-4 text-gray-300 mb-6">
                        <span v-if="anime.genres && anime.genres.length"
                            class="bg-gray-800 px-3 py-1 rounded-full text-sm">
                            {{ formatGenres(anime.genres) }}
                        </span>
                        <span v-if="anime.year" class="bg-gray-800 px-3 py-1 rounded-full text-sm">
                            Year: {{ anime.year }}
                        </span>
                        <span v-if="anime.status" class="bg-gray-800 px-3 py-1 rounded-full text-sm">
                            Status: {{ anime.status }}
                        </span>
                        <span v-if="anime.episodes" class="bg-gray-800 px-3 py-1 rounded-full text-sm">
                            Episodes: {{ anime.episodes }}
                        </span>
                        <span v-if="anime.aired && anime.aired.string"
                            class="bg-gray-800 px-3 py-1 rounded-full text-sm">
                            Aired: {{ anime.aired.string }}
                        </span>
                        <span v-if="anime.studios && anime.studios.length"
                            class="bg-gray-800 px-3 py-1 rounded-full text-sm">
                            Studio: {{ anime.studios[0]?.name || 'N/A' }}
                        </span>
                        <span v-if="anime.type" class="bg-gray-800 px-3 py-1 rounded-full text-sm">
                            Type: {{ anime.type }}
                        </span>
                        <span v-if="anime.source" class="bg-gray-800 px-3 py-1 rounded-full text-sm">
                            Source: {{ anime.source }}
                        </span>
                        <span v-if="anime.duration" class="bg-gray-800 px-3 py-1 rounded-full text-sm">
                            Duration: {{ anime.duration }}
                        </span>
                        <span v-if="anime.rating" class="bg-gray-800 px-3 py-1 rounded-full text-sm">
                            Rating: {{ anime.rating }}
                        </span>
                        <span v-if="anime.rank" class="bg-gray-800 px-3 py-1 rounded-full text-sm">
                            Rank: #{{ anime.rank }}
                        </span>
                        <span v-if="anime.popularity" class="bg-gray-800 px-3 py-1 rounded-full text-sm">
                            Popularity: #{{ anime.popularity }}
                        </span>
                    </div>

                    <h2 class="text-2xl font-bold mb-3">Synopsis</h2>
                    <p class="text-gray-300 leading-relaxed mb-8">
                        {{ anime.synopsis || 'No synopsis available.' }}
                    </p>

                    <div v-if="anime.trailer && anime.trailer.embed_url">
                        <h2 class="text-2xl font-bold mb-3">Trailer</h2>
                        <div class="aspect-w-16 aspect-h-9 bg-gray-800 rounded-lg overflow-hidden">
                            <iframe :src="anime.trailer.embed_url.replace('autoplay=1', 'autoplay=0')" frameborder="0"
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                allowfullscreen class="w-full h-full"></iframe>
                        </div>
                    </div>
                    <p v-else class="text-gray-400">No trailer available for this anime.</p>

                    <div class="mt-8">
                        <a :href="anime.url" target="_blank" rel="noopener noreferrer"
                            class="inline-block px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors font-medium">
                            View on MyAnimeList
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Aspect ratio classes for responsive video */
.aspect-w-16 {
    position: relative;
    width: 100%;
}

.aspect-w-16::before {
    content: '';
    display: block;
    padding-bottom: 56.25%;
    /* 16:9 aspect ratio */
}

.aspect-h-9 {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}
</style>