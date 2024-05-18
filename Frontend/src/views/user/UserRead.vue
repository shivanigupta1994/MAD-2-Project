<template>
  <div style="height: 80vh">
    <VueReader :url="epubUrl" loadingView />
  </div>
</template>

<script setup>
import { VueReader } from 'vue-reader'
import { useRoute } from 'vue-router'

const route = useRoute()

// Change the url to the epub file using the query parameter from the url route.query.epub_url
const epubUrl = route.query.epub_url

// Pass the epubUrl to the VueReader component
const props = {
  VueReader,
  epubUrl
}
</script>
