<template>
  <NavigationBar></NavigationBar>
  <v-progress-linear :active="uploading" indeterminate></v-progress-linear>
  <v-container :class='fade.join(" ")'>
    <v-responsive class="align-center text-center fill-height">
      <v-container class="d-flex">
        <v-img class="v-col-9" style="aspect-ratio: 64/40;" :src='"http://localhost:8000" + displayStatus.displayData.image'></v-img>
        <v-col class="ml-2 v-col-3" style="display:grid">
          <div>
            <div>
              <small>Saturation</small>
              <v-slider id="sat" step="0.1" max="1" thumb-label></v-slider>
            </div>
          </div>
          <div class="align-self-end d-flex flex-column">
            <v-btn class="flex-fill ma-1" prepend-icon="mdi-magnify" @click.stop="previewImage()">
            Preview
          </v-btn>
          <v-btn class="flex-fill ma-1" prepend-icon="mdi-upload" @click.stop="selectImage()">
            Update Image
          </v-btn>
          </div>
          
        </v-col>
      </v-container>
      <v-row class="d-flex align-center justify-center">
        <input id="file" type="file" style="visibility: hidden" v-on:change="doFileUpload()"
          accept="image/png, image/jpeg" multiple>
      </v-row>
    </v-responsive>
  </v-container>
</template>

<script setup>
import NavigationBar from './NavigationBar.vue';
//
</script>

<script>
import { ref } from "vue";
let showBar = ref(false);
let statusObject = ref({ displayData: { image: "" } });
let fade = ref(["fill-height"]);
let preview = ref("");

function previewImage() {
  preview.value = "/preview_image?saturation=" + document.getElementById("sat").value;
}

function selectImage() {
    if (showBar.value) return;
    showBar.value = true
    fade.value.push("fade-animation");
    fetch("http://hyperdeath.local:8000/pick_image", {
      method: "POST",
      body: JSON.stringify({image: statusObject.value.displayData.image, saturation: document.getElementById("sat").value}),
      mode: "no-cors"
    }).then(() => {showBar.value = false; fade.value.pop();})
  }

export default {
  data: () => ({
    displayStatus: statusObject,
    preview,
    uploading: showBar,
    group: null,
    fade
  }),

  watch: {
    group() {
      this.uploading = showBar,
        this.displayStatus = {},
        this.preview = "";
    },
  },
  beforeMount() {
    fetch("http://hyperdeath.local:8000/status").then(res => res.json()).then(res => {
      this.displayStatus = res;
      if (res.currentDisplay == "image") {
        this.preview = res.displayData.image;
      }
    });
  }
}
</script>