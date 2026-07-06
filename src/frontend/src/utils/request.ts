import axios from 'axios'

const request = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '',
    timeout: 10000
})

request.interceptors.request.use(function (config) {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers = config.headers || {};
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
}, function (error) {
  console.error('请求拦截器错误:', error)
  return Promise.reject(error);
});

request.interceptors.response.use(function (response) {
  return response;
}, function (error) {
  console.error('响应错误:', error.response?.status, error.config?.url)
  console.error('错误详情:', error.response?.data || error.message)
  
  if (error.response?.status === 401) {
    localStorage.removeItem('token');
    localStorage.removeItem('userInfo');
    window.location.href = '/login';
  }
  return Promise.reject(error);
});

export { request }