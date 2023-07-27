<template>
  <NavigationBar></NavigationBar>
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
function openFilePicker() {
  document.getElementById('file').click()
}

function doFileUpload() {
  const picker = document.getElementById('file');
  if (picker.files.length == 0) {
    return;
  }
  Array.from(picker.files).forEach(file => {
    console.log(file);
    const form = new FormData();
    form.append("file", file, file.name);
    fetch("http://hyperdeath.local:8000/upload_image", {
      method: "POST",
      body: form,
      mode: "no-cors"
    }).then(_ => console.log(1))
  })
}
</script>