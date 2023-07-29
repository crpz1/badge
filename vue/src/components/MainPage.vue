<template>
 <NavigationBar></NavigationBar>
 <v-progress-linear :active="isActive" height="4" indeterminate></v-progress-linear>
  <v-container class="fill-height">
    <v-responsive class="align-center text-center fill-height">
      <v-card class="mx-auto" v-for="image in images" :key="image" style="margin-bottom: 1em">
        <v-img :src="'http://hyperdeath.local:8000' + image.path" cover @click.stop="selectImage"></v-img>
        <v-card-title>{{ image.path }}</v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn icon="mdi-check" @click.stop="selectImage"></v-btn>
          <v-btn icon="mdi-delete"></v-btn>
        </v-card-actions>
      </v-card>
    </v-responsive>
  </v-container>
</template>

<script setup>
  import NavigationBar from './NavigationBar.vue'; 
  //
</script>

<script>
  import { ref } from "vue";
  let loading = ref(false);

  function selectImage(a) {
    if (loading.value) return;
    loading.value = true
    fetch("http://hyperdeath.local:8000/pick_image", {
      method: "POST",
      body: JSON.stringify({image: a.currentTarget.parentElement.children[2].innerText}),
      mode: "no-cors"
    }).then(() => loading.value = false)
  }

  export default {
    data: () => ({
      images: {},
      group: null,
      isActive: loading
    }),

    watch: {
      group () {
        this.images = {}
      },
    },

    beforeMount() {
      fetch("http://hyperdeath.local:8000/enumerate_images").then(res => res.json()).then(obj => this.images = obj)
    }
  }
</script>
