<template>
  <div class="weather">
    <h2>天气查询</h2>
    <input v-model="city" placeholder="输入城市" />
    <input v-model="date" placeholder="输入日期（如：今天、明天）" />
    <button @click="fetchWeather">查询天气</button>
    
    <div v-if="loading">加载中...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="weatherData">
      <h3>{{ city }} 的天气</h3>
      <p>{{ weatherData }}</p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { getWeather } from '../api/index';

export default {
  name: 'Weather',
  setup() {
    const city = ref('');
    const date = ref('今天');
    const weatherData = ref(null);
    const loading = ref(false);
    const error = ref(null);

    const fetchWeather = async () => {
      loading.value = true;
      error.value = null;
      try {
        const response = await getWeather(city.value, date.value);
        weatherData.value = response.data;
      } catch (err) {
        error.value = '获取天气信息失败，请重试。';
      } finally {
        loading.value = false;
      }
    };

    return {
      city,
      date,
      weatherData,
      loading,
      error,
      fetchWeather,
    };
  },
};
</script>

<style scoped>
.weather {
  margin: 20px;
}
.error {
  color: red;
}
</style>