<template>
  <div class="reminder">
    <h2>提醒管理</h2>
    <input v-model="reminderContent" placeholder="输入提醒内容" />
    <button @click="setReminder">设置提醒</button>
    
    <h3>活跃提醒</h3>
    <ul>
      <li v-for="(reminder, index) in activeReminders" :key="index">
        {{ reminder.content }}（创建于{{ formatDate(reminder.created_at) }}）
      </li>
    </ul>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { fetchActiveReminders, createReminder } from '../api/index';

export default {
  name: 'Reminder',
  setup() {
    const reminderContent = ref('');
    const activeReminders = ref([]);

    const setReminder = async () => {
      if (reminderContent.value.trim()) {
        await createReminder(reminderContent.value);
        reminderContent.value = '';
        loadActiveReminders();
      }
    };

    const loadActiveReminders = async () => {
      activeReminders.value = await fetchActiveReminders();
    };

    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' };
      return new Date(dateString).toLocaleString('zh-CN', options);
    };

    onMounted(loadActiveReminders);

    return {
      reminderContent,
      activeReminders,
      setReminder,
      formatDate,
    };
  },
};
</script>

<style scoped>
.reminder {
  padding: 20px;
}

.reminder input {
  margin-right: 10px;
}
</style>