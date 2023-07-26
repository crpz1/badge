/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from './App.vue';
import MainPage from "@/components/MainPage.vue";
import UploadPage from "@/components/UploadPage.vue";

// Composables
import { createApp } from 'vue';

// Plugins
import { registerPlugins } from '@/plugins';

import { createRouter } from 'vue-router';
import { createWebHistory } from 'vue-router';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: "/", name: "Home", component: MainPage },
        { path: "/upload", name: "Upload", component: UploadPage },
    ]
});

const app = createApp(App);

registerPlugins(app);

app.use(router);

app.mount('#app');
