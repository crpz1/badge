<template>
 <NavigationBar></NavigationBar>
 <v-progress-linear class="position-fixed" style="top: 64px; z-index: 1;" :active="isActive" height="4" indeterminate></v-progress-linear>
  <v-container :class="fade.join(' ')">
    <v-responsive class="align-center text-center fill-height">
      <v-card class="mx-auto" v-for="image in images" :key="image" style="margin-bottom: 1em">
        <v-img v-ripple :src="'http://localhost:8000' + image.path" cover @click.stop="selectImage"></v-img>
        <v-card-title>{{ image.path }}</v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn icon="mdi-check" @click.stop="selectImage"></v-btn>
          <v-btn icon="mdi-delete" @click.stop="deleteImage"></v-btn>
        </v-card-actions>
      </v-card>
    </v-responsive>
  </v-container>
</template>

<script setup>
  import NavigationBar from './NavigationBar.vue'; 
  import '../assets/styles.css';
  //
</script>

<script>
  import { ref } from "vue";
  let loading = ref(false);
  let imageObject = ref({});
  let fade = ref(["fill-height"]);

  function selectImage(a) {
    if (loading.value) return;
    loading.value = true
    fade.value.push("fade-animation");
    fetch("http://hyperdeath.local:8000/pick_image", {
      method: "POST",
      body: JSON.stringify({image: a.currentTarget.parentElement.children[2].innerText}),
      mode: "no-cors"
    }).then(() => {loading.value = false; fade.value.pop();})
  }

  function deleteImage(a) {
    if (loading.value) return;
    loading.value = true;
    fade.value.push("fade-animation");
    fetch("http://hyperdeath.local:8000" + a.currentTarget.parentElement.parentElement.children[2].innerText, {
      method: "DELETE"
    }).then(fetch("http://hyperdeath.local:8000/enumerate_images").then(res => res.json()).then(obj => {
      imageObject.value = obj;
      loading.value = false;
      fade.value.pop();
    }))
  }

  export default {
    data: () => ({
      images: imageObject,
      group: null,
      isActive: loading,
      fade
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
