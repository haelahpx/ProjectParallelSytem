import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/home.vue'; // This will be your current App.vue content
import AnimeDetail from '../views/anime.vue'; // Your anime detail page

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView // Assign HomeView as the component for the root path
  },
  {
    path: '/anime/:id', // Dynamic segment for the anime ID
    name: 'AnimeDetail',
    component: AnimeDetail,
    props: true // This allows the route parameter 'id' to be passed as a prop to the AnimeDetail component
  },
];

const router = createRouter({
  history: createWebHistory(), // Recommended for cleaner URLs (e.g., /anime/123 instead of /#anime/123)
  routes
});

export default router;