<template>
  <NavigationBar></NavigationBar>
  <v-progress-linear :active="uploading" :model-value="progress"></v-progress-linear>
  <v-container class="fill-height">
    <v-responsive class="align-center text-center fill-height">
      <v-btn prepend-icon="mdi-upload" @click.stop="openFilePicker()">
        Upload Images
      </v-btn>
      <v-row class="d-flex align-center justify-center">
        <input id="file" type="file" style="visibility: hidden" v-on:change="doFileUpload()" accept="image/png, image/jpeg" multiple>
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
  let count = ref(0);

  function openFilePicker() {
    document.getElementById('file').click()
    showBar.value = false;
  }

  function doFileUpload() {
    const picker = document.getElementById('file');
    if (picker.files.length == 0) {
      return;
  }
  showBar.value = true;
  count.value = 0;
  const perItem = 100 / picker.files.length;
  Array.from(picker.files).forEach(file => {
    console.log(file);
    const form = new FormData();
    form.append("file", file, file.name);
    fetch("http://hyperdeath.local:8000/upload_image", {
      method: "POST",
      body: form,
      mode: "no-cors"
    }).then(() => count.value += perItem)
  })
}

export default {
    data: () => ({
      uploading: showBar,
      progress: count,
      group: null,
    }),

    watch: {
      group () {
        this.uploading = showBar,
        this.progress = count;
      },
    },
  }
</script>