import axios from 'axios'

// const baseURL = process.env.REACT_APP_API_BASE_URL;
const baseURL = 'http://localhost:8000/';

// Axios 인스턴스 생성
const apiClient = axios.create({
    baseURL: baseURL,
    timeout: 10000, // 요청 타임아웃 
})

// 요청 인터셉터
apiClient.interceptors.request.use(
    (config) => {
        const accessToken = localStorage.getItem('accessToken')
        if (accessToken) {
            config.headers['Authorization'] = `Bearer ${accessToken}`
        }
        return config
    },
    (error) => Promise.reject(error),
)

// 응답 인터셉터
apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config
        // 재전송 방지용 플래그
        originalRequest._retry = originalRequest._retry || false

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true
            const refresh = localStorage.getItem('refreshToken')
            if (refresh) {
                try {
                    const response = await axios.post(`${baseURL}/api/token/refresh/`, {
                        refresh: refresh,
                    })
                    const accessToken = response.data.access
                    const refreshToken = response.data.refresh
                    localStorage.setItem('accessToken', accessToken)
                    localStorage.setItem('refreshToken', refreshToken)

                    originalRequest.headers['Authorization'] = `Bearer ${accessToken}`
                    return apiClient(originalRequest)
                } catch (refreshError) {
                    localStorage.removeItem('accessToken')
                    localStorage.removeItem('refreshToken')
                    if (window.location.pathname !== '/login') {
                        const currentUrl = encodeURIComponent(window.location.pathname + window.location.search)
                        window.location.href = `/login?redirectUrl=${currentUrl}`
                        return Promise.reject(refreshError)
                    }
                }
            } else {
                if (window.location.pathname !== '/login') {
                    const currentUrl = encodeURIComponent(window.location.pathname + window.location.search)
                    window.location.href = `/login?redirectUrl=${currentUrl}`
                    return Promise.reject(error)
                }
            }
        }
        return Promise.reject(error)
    },
)

export default apiClient
