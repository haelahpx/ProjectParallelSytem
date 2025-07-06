<template>
    <div class="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black text-white">
        <header class="sticky top-0 z-40 backdrop-blur-md bg-black/90 border-b border-blue-500/20">
            <div class="container mx-auto px-4 py-4">
                <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-3">
                        <div class="relative">
                            <div
                                class="w-10 h-10 bg-gradient-to-br from-blue-400 to-blue-600 rounded-xl flex items-center justify-center shadow-lg">
                                <img class="w-6 h-6" src="/logo.png" alt="Logo">
                            </div>
                            <div class="absolute -top-1 -right-1 w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
                        </div>
                        <h1
                            class="text-xl font-bold bg-gradient-to-r from-blue-400 to-blue-200 bg-clip-text text-transparent">
                            NimeView
                        </h1>
                    </div>

                    <div class="hidden md:flex flex-1 max-w-md mx-8">
                        <div class="relative w-full">
                            <input v-model="searchQuery" @input="handleSearch" type="text" placeholder="Search anime..."
                                class="w-full bg-gray-900/50 border border-blue-500/30 rounded-xl px-4 py-2 pl-10 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-all" />
                            <svg class="absolute left-3 top-2.5 w-5 h-5 text-gray-400" fill="none"
                                stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                        </div>
                    </div>

                    <nav class="hidden md:flex items-center space-x-1 bg-gray-900/50 rounded-xl p-1">
                        <button v-for="tab in tabs" :key="tab.id" @click="setActiveTab(tab.id)" :class="[
                                'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200',
                                activeTab === tab.id
                                    ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/25'
                                    : 'text-gray-400 hover:text-white hover:bg-gray-800'
                            ]">
                            {{ tab.label }}
                        </button>
                    </nav>

                    <button @click="showMobileMenu = !showMobileMenu"
                        class="md:hidden p-2 rounded-lg hover:bg-gray-800 transition-colors">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    </button>
                </div>

                <div v-if="showMobileMenu" class="md:hidden mt-4 space-y-3">
                    <div class="relative">
                        <input v-model="searchQuery" @input="handleSearch" type="text" placeholder="Search anime..."
                            class="w-full bg-gray-900/50 border border-blue-500/30 rounded-xl px-4 py-2 pl-10 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-400" />
                        <svg class="absolute left-3 top-2.5 w-5 h-5 text-gray-400" fill="none" stroke="currentColor"
                            viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                    </div>

                    <div class="flex flex-wrap gap-2">
                        <button v-for="tab in tabs" :key="tab.id" @click="setActiveTab(tab.id)" :class="[
                                'flex-1 px-3 py-2 rounded-lg text-sm font-medium transition-all',
                                activeTab === tab.id
                                    ? 'bg-blue-500 text-white'
                                    : 'bg-gray-900 text-gray-400 hover:text-white'
                            ]">
                            {{ tab.label }}
                        </button>
                    </div>
                </div>
            </div>
        </header>

        <main class="container mx-auto px-4 py-8">
            <div v-if="activeTab === 'seasonal'" class="mb-8">
                <div class="flex flex-wrap gap-4 items-center">
                    <div class="flex items-center space-x-2">
                        <label class="text-sm font-medium text-gray-400">Year:</label>
                        <select v-model="selectedYear" @change="fetchSeasonalAnime"
                            class="bg-gray-900 border border-blue-500/30 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-400">
                            <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
                        </select>
                    </div>
                    <div class="flex items-center space-x-2">
                        <label class="text-sm font-medium text-gray-400">Season:</label>
                        <select v-model="selectedSeason" @change="fetchSeasonalAnime"
                            class="bg-gray-900 border border-blue-500/30 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-400">
                            <option v-for="season in seasons" :key="season" :value="season">
                                {{ season.charAt(0).toUpperCase() + season.slice(1) }}
                            </option>
                        </select>
                    </div>
                </div>
            </div>

            <div v-if="!loading && animeList.length > 0" class="mb-8">
                <div class="bg-gray-900/50 backdrop-blur-sm rounded-xl p-4 border border-blue-500/20">
                    <div class="flex items-center justify-between text-sm">
                        <span class="text-gray-400">
                            Showing {{ animeList.length }} anime
                            <span v-if="searchQuery" class="text-blue-400">for "{{ searchQuery }}"</span>
                        </span>
                        <div class="flex items-center space-x-4">
                            <button @click="viewMode = 'grid'"
                                :class="viewMode === 'grid' ? 'text-blue-400' : 'text-gray-400 hover:text-white'"
                                class="p-1 rounded transition-colors">
                                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                    <path
                                        d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                                </svg>
                            </button>
                            <button @click="viewMode = 'list'"
                                :class="viewMode === 'list' ? 'text-blue-400' : 'text-gray-400 hover:text-white'"
                                class="p-1 rounded transition-colors">
                                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd"
                                        d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" />
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="loading" class="flex flex-col items-center justify-center py-20">
                <div class="relative">
                    <div class="w-12 h-12 border-4 border-gray-700 border-t-blue-500 rounded-full animate-spin"></div>
                    <div
                        class="absolute inset-0 w-12 h-12 border-4 border-transparent border-r-blue-400 rounded-full animate-spin animation-delay-150">
                    </div>
                </div>
                <p class="mt-4 text-gray-400 animate-pulse">Loading anime...</p>
            </div>

            <div v-else-if="error" class="text-center py-20">
                <div class="inline-flex items-center justify-center w-16 h-16 bg-blue-500/10 rounded-full mb-4">
                    <svg class="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                    </svg>
                </div>
                <h3 class="text-xl font-semibold text-blue-400 mb-2">Oops! Something went wrong</h3>
                <p class="text-gray-400 mb-6">{{ error }}</p>
                <button @click="fetchData"
                    class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg transition-colors font-medium">
                    Try Again
                </button>
            </div>

            <div v-else-if="animeList.length === 0" class="text-center py-20">
                <div class="inline-flex items-center justify-center w-16 h-16 bg-gray-800/50 rounded-full mb-4">
                    <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                </div>
                <h3 class="text-xl font-semibold text-gray-300 mb-2">No anime found</h3>
                <p class="text-gray-400">Try adjusting your search or filters.</p>
            </div>

            <div v-else>
                <div v-if="viewMode === 'grid'"
                    class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4 md:gap-6">
                    <div v-for="anime in animeList" :key="anime.mal_id"
                        class="group relative bg-gray-900/50 backdrop-blur-sm rounded-xl overflow-hidden hover:bg-gray-900/70 transition-all duration-300 hover:scale-105 cursor-pointer border border-blue-500/20 hover:border-blue-500/50"
                        @click="selectAnime(anime)">
                        <div class="relative aspect-[3/4] overflow-hidden">
                            <img :src="anime.image" :alt="anime.title"
                                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                                loading="lazy" />

                            <div
                                class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                            </div>

                            <div v-if="anime.score && anime.score > 0"
                                class="absolute top-2 right-2 bg-gradient-to-r from-blue-500 to-blue-600 text-white text-xs font-bold px-2 py-1 rounded-full shadow-lg">
                                {{ anime.score }}
                            </div>

                            <div v-if="anime.rank"
                                class="absolute top-2 left-2 bg-black/70 backdrop-blur-sm text-white text-xs font-bold px-2 py-1 rounded-full">
                                #{{ anime.rank }}
                            </div>
                        </div>

                        <div class="p-3">
                            <h3
                                class="font-semibold text-sm mb-2 line-clamp-2 group-hover:text-blue-400 transition-colors">
                                {{ anime.title }}
                            </h3>
                            <div class="flex flex-wrap gap-1 mb-2">
                                <span v-for="genre in anime.genres.slice(0, 2)" :key="genre"
                                    class="bg-gray-800/50 text-xs px-2 py-1 rounded-full text-gray-300">
                                    {{ genre }}
                                </span>
                            </div>
                            <div class="flex justify-between items-center text-xs text-gray-400">
                                <span v-if="anime.year">{{ anime.year }}</span>
                                <span v-if="anime.type" class="bg-gray-800/50 px-2 py-1 rounded-full">{{ anime.type
                                    }}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-else class="space-y-4">
                    <div v-for="anime in animeList" :key="anime.mal_id"
                        class="group bg-gray-900/50 backdrop-blur-sm rounded-xl p-4 hover:bg-gray-900/70 transition-all duration-300 cursor-pointer border border-blue-500/20 hover:border-blue-500/50"
                        @click="selectAnime(anime)">
                        <div class="flex items-center space-x-4">
                            <img :src="anime.image" :alt="anime.title"
                                class="w-16 h-20 object-cover rounded-lg group-hover:scale-105 transition-transform duration-300"
                                loading="lazy" />
                            <div class="flex-1 min-w-0">
                                <h3 class="font-semibold text-lg group-hover:text-blue-400 transition-colors truncate">
                                    {{ anime.title }}
                                </h3>
                                <div class="flex items-center space-x-4 text-sm text-gray-400 mt-1">
                                    <span v-if="anime.year">{{ anime.year }}</span>
                                    <span v-if="anime.type">{{ anime.type }}</span>
                                    <span v-if="anime.score && anime.score > 0" class="text-blue-400 font-medium">
                                        ★ {{ anime.score }}
                                    </span>
                                    <span v-if="anime.rank" class="text-gray-300 font-medium">
                                        #{{ anime.rank }}
                                    </span>
                                </div>
                                <div class="flex flex-wrap gap-1 mt-2">
                                    <span v-for="genre in anime.genres.slice(0, 4)" :key="genre"
                                        class="bg-gray-800/50 text-xs px-2 py-1 rounded-full text-gray-300">
                                        {{ genre }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="animeList.length > 0 && !loading && !searchQuery" class="text-center mt-12">
                <button @click="loadMore"
                    class="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white px-8 py-3 rounded-xl transition-all font-medium shadow-lg hover:shadow-xl transform hover:scale-105">
                    Load More
                </button>
            </div>
        </main>

        <div v-if="selectedAnime"
            class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 z-50"
            @click="selectedAnime = null">
            <div class="bg-gray-900/95 backdrop-blur-md rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto border border-blue-500/20 shadow-2xl"
                @click.stop>
                <div class="flex flex-col md:flex-row">
                    <div class="w-full md:w-1/3 flex-shrink-0 relative">
                        <img :src="selectedAnime.image" :alt="selectedAnime.title"
                            class="w-full h-64 md:h-full object-cover rounded-t-2xl md:rounded-l-2xl md:rounded-tr-none" />
                        <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent md:hidden"></div>
                    </div>

                    <div class="flex-1 p-6">
                        <div class="flex justify-between items-start mb-4">
                            <h2
                                class="text-2xl font-bold bg-gradient-to-r from-blue-400 to-blue-200 bg-clip-text text-transparent">
                                {{ selectedAnime.title }}
                            </h2>
                            <button @click="selectedAnime = null"
                                class="text-gray-400 hover:text-white text-2xl p-2 hover:bg-gray-800/50 rounded-full transition-colors">
                                ×
                            </button>
                        </div>

                        <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
                            <div v-if="selectedAnime.score" class="bg-gray-800/50 rounded-lg p-3 text-center">
                                <div class="text-2xl font-bold text-blue-400">{{ selectedAnime.score }}</div>
                                <div class="text-xs text-gray-400">Score</div>
                            </div>
                            <div v-if="selectedAnime.rank" class="bg-gray-800/50 rounded-lg p-3 text-center">
                                <div class="text-2xl font-bold text-blue-300">#{{ selectedAnime.rank }}</div>
                                <div class="text-xs text-gray-400">Rank</div>
                            </div>
                            <div v-if="selectedAnime.year" class="bg-gray-800/50 rounded-lg p-3 text-center">
                                <div class="text-2xl font-bold text-blue-200">{{ selectedAnime.year }}</div>
                                <div class="text-xs text-gray-400">Year</div>
                            </div>
                            <div v-if="selectedAnime.episodes" class="bg-gray-800/50 rounded-lg p-3 text-center">
                                <div class="text-2xl font-bold text-blue-500">{{ selectedAnime.episodes }}</div>
                                <div class="text-xs text-gray-400">Episodes</div>
                            </div>
                            <div v-if="selectedAnime.status" class="bg-gray-800/50 rounded-lg p-3 text-center">
                                <div class="text-sm font-bold text-blue-300">{{ selectedAnime.status }}</div>
                                <div class="text-xs text-gray-400">Status</div>
                            </div>
                            <div v-if="selectedAnime.type" class="bg-gray-800/50 rounded-lg p-3 text-center">
                                <div class="text-sm font-bold text-blue-400">{{ selectedAnime.type }}</div>
                                <div class="text-xs text-gray-400">Type</div>
                            </div>
                        </div>

                        <div v-if="selectedAnime.genres.length > 0" class="mb-6">
                            <h3 class="text-sm font-semibold text-gray-300 mb-3">Genres</h3>
                            <div class="flex flex-wrap gap-2">
                                <span v-for="genre in selectedAnime.genres" :key="genre"
                                    class="bg-blue-500/20 border border-blue-500/30 text-blue-300 text-sm px-3 py-1 rounded-full">
                                    {{ genre }}
                                </span>
                            </div>
                        </div>

                        <div v-if="selectedAnime.synopsis" class="mb-6">
                            <h3 class="text-sm font-semibold text-gray-300 mb-3">Synopsis</h3>
                            <p class="text-gray-300 text-sm leading-relaxed">{{ selectedAnime.synopsis }}</p>
                        </div>

                        <div class="flex gap-4 pt-4 border-t border-blue-500/20">
                            <a :href="selectedAnime.url" target="_blank"
                                class="flex-1 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white px-4 py-3 rounded-xl text-sm font-medium transition-all text-center shadow-lg hover:shadow-xl transform hover:scale-105">
                                View on MyAnimeList
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch} from 'vue'

interface Anime {
    mal_id: number
    title: string
    image: string
    score: number
    rank: number
    year: number
    episodes: number
    status: string
    type: string
    genres: string[]
    synopsis: string
    url: string
}

interface Tab {
    id: string
    label: string
}

export default defineComponent({
    name: 'AnimeHomepage',
    setup() {
        const activeTab = ref<string>('top')
        const animeList = ref<Anime[]>([])
        const loading = ref<boolean>(false)
        const error = ref<string | null>(null)
        const selectedAnime = ref<Anime | null>(null)
        const selectedYear = ref<number>(new Date().getFullYear())
        const selectedSeason = ref<string>('winter')
        const searchQuery = ref<string>('')
        const showMobileMenu = ref<boolean>(false)
        const viewMode = ref<'grid' | 'list'>('grid')

        const seasons = ['winter', 'spring', 'summer', 'fall']
        const years = ref<number[]>([])
        const apiBaseUrl = 'http://localhost:8000'

        const tabs: Tab[] = [
            { id: 'top', label: 'Top Rated' },
            { id: 'airing', label: 'Airing' },
            { id: 'seasonal', label: 'Seasonal' }
        ]
        const initializeYears = () => {
            const currentYear = new Date().getFullYear()
            years.value = Array.from({ length: currentYear - 1989 }, (_, i) => currentYear - i)
        }

        const setActiveTab = (tabId: string) => {
            activeTab.value = tabId;
            searchQuery.value = ''; 
            showMobileMenu.value = false;
            fetchData(); 
        }

        const fetchData = async () => {
            loading.value = true
            error.value = null

            try {
                let url: string
                if (searchQuery.value) {
                    url = `${apiBaseUrl}/search-anime?q=${encodeURIComponent(searchQuery.value)}`;
                } else {
                    switch (activeTab.value) {
                        case 'top':
                            url = `${apiBaseUrl}/anime`
                            break
                        case 'airing':
                            url = `${apiBaseUrl}/anime/airing`
                            break
                        case 'seasonal':
                            url = `${apiBaseUrl}/season/${selectedYear.value}/${selectedSeason.value}`
                            break
                        default:
                            url = `${apiBaseUrl}/anime`
                    }
                }


                const response = await fetch(url)
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`)
                }

                const data = await response.json()
                animeList.value = data.results || []
            } catch (err) {
                error.value = 'Failed to fetch anime data. Please check your connection and try again.'
                console.error('Error fetching anime:', err)
            } finally {
                loading.value = false
            }
        }

        const fetchSeasonalAnime = async () => {
            if (activeTab.value === 'seasonal' && !searchQuery.value) { 
                await fetchData()
            }
        }

        const selectAnime = (anime: Anime) => {
            selectedAnime.value = anime
        }

        let searchTimeout: number;

        const handleSearch = () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                fetchData();
            }, 500); 
        };

        const loadMore = () => {
            console.log('Load more function triggered. Implement pagination if your API supports it.');
        }

        onMounted(() => {
            initializeYears()
            fetchData()
        })

        watch(activeTab, () => {
            if (!searchQuery.value) fetchData(); 
        });
        watch([selectedYear, selectedSeason], () => {
            fetchSeasonalAnime();
        });

        return {
            activeTab,
            animeList,
            loading,
            error,
            selectedAnime,
            selectedYear,
            selectedSeason,
            searchQuery,
            showMobileMenu,
            viewMode,
            seasons,
            years,
            tabs,
            setActiveTab,
            fetchData,
            fetchSeasonalAnime,
            selectAnime,
            loadMore,
            handleSearch, 
        }
    }
})
</script>

<style>
.animation-delay-150 {
    animation-delay: 150ms;
}
</style>