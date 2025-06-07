<template>
  <div class="about">
    <h1>关于智能日程管理助手</h1>
    <p>智能日程管理助手是一个基于Vue.js的应用，旨在帮助用户高效管理日程、提醒和天气信息。</p>
    <h2>功能特点</h2>
    <ul>
      <li>日历管理：创建、查询和管理日程事件。</li>
      <li>提醒功能：设置和查看提醒事项。</li>
      <li>天气查询：获取实时天气信息。</li>
    </ul>
    <h2>技术栈</h2>
    <p>本项目使用以下技术构建：</p>
    <ul>
      <li>Vue.js：用于构建用户界面。</li>
      <li>Vite：快速的前端构建工具。</li>
      <li>Axios：用于与后端API进行交互。</li>
    </ul>
    <h2>如何使用</h2>
    <p>您可以通过访问主页来开始使用智能日程管理助手，输入您的日程、提醒和天气查询。</p>
  </div>
</template>

<script>
export default {
  name: 'About'
}
</script>

<style scoped>
.about {
  padding: 20px;
}
.about h1 {
  font-size: 2em;
}
.about h2 {
  margin-top: 20px;
}
.about ul {
  list-style-type: disc;
  margin-left: 20px;
}
</style>