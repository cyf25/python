<template>
  <div class="chat-container">
    <div class="chat-header">
      <h2>智能日程管理助手</h2>
    </div>
    
    <div class="chat-messages" ref="messagesContainer">
      <div v-for="(message, index) in messages" :key="index" 
           :class="['message', message.type]">
        <div class="message-content">{{ message.content }}</div>
      </div>
    </div>

    <div class="chat-input">
      <input v-model="inputMessage" 
             @keyup.enter="sendMessage"
             placeholder="输入你的日程管理需求...">
      <button @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Chat',
  data() {
    return {
      inputMessage: '',
      messages: [
        { type: 'assistant', content: '你好！我是智能日程管理助手，请问有什么可以帮您？' }
      ]
    }
  },
  methods: {
    async sendMessage() {
      if (!this.inputMessage.trim()) return
      
      // 添加用户消息
      this.messages.push({
        type: 'user',
        content: this.inputMessage
      })
      
      const userMessage = this.inputMessage
      this.inputMessage = ''
      
      try {
        // 调用后端API
        const response = await axios.post('/api/chat', {
          input: userMessage
        })
        
        // 添加助手回复
        this.messages.push({
          type: 'assistant',
          content: response.data.output
        })
      } catch (error) {
        this.messages.push({
          type: 'error',
          content: '处理请求时出错，请稍后再试'
        })
      }
      
      // 滚动到底部
      this.$nextTick(() => {
        this.$refs.messagesContainer.scrollTop = 
          this.$refs.messagesContainer.scrollHeight
      })
    }
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 20px;
  background-color: #f5f5f5;
}

.chat-header {
  text-align: center;
  margin-bottom: 20px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 20px;
  padding: 10px;
  background-color: white;
  border-radius: 8px;
}

.message {
  margin-bottom: 15px;
}

.message-content {
  padding: 10px 15px;
  border-radius: 18px;
  max-width: 80%;
  word-wrap: break-word;
}

.user {
  display: flex;
  justify-content: flex-end;
}

.user .message-content {
  background-color: #dcf8c6;
}

.assistant {
  display: flex;
  justify-content: flex-start;
}

.assistant .message-content {
  background-color: #e5e5ea;
}

.error .message-content {
  background-color: #ffebee;
  color: #d32f2f;
}

.chat-input {
  display: flex;
  gap: 10px;
}

.chat-input input {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 20px;
  outline: none;
}

.chat-input button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
}

.chat-input button:hover {
  background-color: #45a049;
}
</style>