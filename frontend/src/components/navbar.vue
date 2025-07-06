<template>
    <header class="bg-black border-b border-gray-800">
        <div class="container mx-auto px-4 py-4">
            <div class="flex items-center justify-between">
                <h1 class="text-2xl font-bold text-blue-400">AnimeList</h1>
                <nav class="flex space-x-6">
                    <button @click="$emit('change-tab', 'top')"
                        :class="activeTab === 'top' ? 'text-blue-400 border-b-2 border-blue-400' : 'text-gray-400 hover:text-white'"
                        class="pb-2 transition-colors">
                        Top Rated
                    </button>
                    <button @click="$emit('change-tab', 'airing')"
                        :class="activeTab === 'airing' ? 'text-blue-400 border-b-2 border-blue-400' : 'text-gray-400 hover:text-white'"
                        class="pb-2 transition-colors">
                        Airing
                    </button>
                    <button @click="$emit('change-tab', 'seasonal')"
                        :class="activeTab === 'seasonal' ? 'text-blue-400 border-b-2 border-blue-400' : 'text-gray-400 hover:text-white'"
                        class="pb-2 transition-colors">
                        Seasonal
                    </button>
                </nav>
            </div>
        </div>
    </header>
</template>

<script>
export default {
    name: 'AppNavbar',
    props: {
        activeTab: {
            type: String,
            required: true
        }
    }
};
</script>

<style scoped>
/* Any specific styles for the Navbar can go here if needed */
</style>