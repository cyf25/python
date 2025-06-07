<template>
  <div class="calendar">
    <h1>日历</h1>
    <div>
      <input type="date" v-model="selectedDate" @change="fetchEvents" />
      <button @click="createEvent">创建日程</button>
    </div>
    <ul>
      <li v-for="event in events" :key="event.id">
        {{ event.time }} - {{ event.description }}
      </li>
    </ul>
  </div>
</template>

<script>
import { ref } from 'vue';
import { fetchEvents, createEvent } from '../api/index';

export default {
  name: 'Calendar',
  setup() {
    const selectedDate = ref(new Date().toISOString().split('T')[0]);
    const events = ref([]);

    const fetchEvents = async () => {
      try {
        const response = await fetchEvents(selectedDate.value);
        events.value = response.data;
      } catch (error) {
        console.error('获取日程失败:', error);
      }
    };

    const createEvent = async () => {
      const description = prompt('请输入日程描述:');
      if (description) {
        try {
          await createEvent({ time: selectedDate.value, description });
          fetchEvents();
        } catch (error) {
          console.error('创建日程失败:', error);
        }
      }
    };

    return {
      selectedDate,
      events,
      fetchEvents,
      createEvent,
    };
  },
};
</script>

<style scoped>
.calendar {
  padding: 20px;
}
</style>