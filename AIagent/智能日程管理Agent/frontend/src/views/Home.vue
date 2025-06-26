<template>
  <div class="home-container">
    <Chat />
  </div>
</template>

<script>
import Chat from '@/components/Chat.vue'

export default {
  name: 'Home',
  components: {
    Chat
  }
}
</script>

<style scoped>
.home-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}
</style>