<template>
  <div id="app">
    <header>
      <h1>智能日程管理助手</h1>
    </header>
    <main>
      <router-view />
    </main>
    <footer>
      <p>© 2025 智能日程管理助手</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
header {
  background-color: #42b983;
  padding: 20px;
  color: white;
}
main {
  flex: 1;
  padding: 20px;
}
footer {
  margin-top: 20px;
  font-size: 14px;
  color: #888;
}
</style>