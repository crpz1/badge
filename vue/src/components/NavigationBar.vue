<template>
    <v-app-bar>
        <template v-slot:prepend>
            <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
        </template>
        <v-app-bar-title>{{page}}</v-app-bar-title>
    </v-app-bar>
    <v-navigation-drawer v-model="drawer" temporary>
        <v-list>
          <v-list-item prepend-icon="mdi-home" title="Home" value="home" to="/"></v-list-item>
          <v-list-item prepend-icon="mdi-monitor" title="Display" value="display" to="/display"></v-list-item>
          <v-list-item prepend-icon="mdi-upload" title="Upload" value="upload" to="upload"></v-list-item>
        </v-list>
    </v-navigation-drawer>
</template>

<script setup>
  import { useRoute } from 'vue-router';
  const route = useRoute();
  const page = route.name;
</script>

<script>
  export default {
    data: () => ({
      drawer: false,
      group: null,
    }),

    watch: {
      group () {
        this.drawer = false
      },
    },
  }
</script>