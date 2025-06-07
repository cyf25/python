import axios from 'axios';

const API_URL = 'http://localhost:5000'; // 后端API的基础URL

// 获取天气信息
export const getWeather = async (city, date) => {
    try {
        const response = await axios.get(`${API_URL}/weather`, {
            params: { city, date }
        });
        return response.data;
    } catch (error) {
        console.error('获取天气信息失败:', error);
        throw error;
    }
};

// 设置提醒
export const setReminder = async (content) => {
    try {
        const response = await axios.post(`${API_URL}/reminder`, { content });
        return response.data;
    } catch (error) {
        console.error('设置提醒失败:', error);
        throw error;
    }
};

// 获取提醒列表
export const getReminders = async () => {
    try {
        const response = await axios.get(`${API_URL}/reminders`);
        return response.data;
    } catch (error) {
        console.error('获取提醒列表失败:', error);
        throw error;
    }
};

// 创建日程
export const createEvent = async (time, description) => {
    try {
        const response = await axios.post(`${API_URL}/calendar`, { time, description });
        return response.data;
    } catch (error) {
        console.error('创建日程失败:', error);
        throw error;
    }
};

// 查询日程
export const getEvents = async (date) => {
    try {
        const response = await axios.get(`${API_URL}/calendar`, {
            params: { date }
        });
        return response.data;
    } catch (error) {
        console.error('查询日程失败:', error);
        throw error;
    }
};