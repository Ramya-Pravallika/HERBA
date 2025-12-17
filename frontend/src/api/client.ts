import axios from 'axios';

const API_URL = 'http://localhost:8002';

export const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const sendMessage = async (message: string, sessionId?: string): Promise<import('../types').ChatResponse> => {
    const response = await apiClient.post('/chat', {
        message,
        session_id: sessionId,
    });
    return response.data;
};

export const resetSession = async (sessionId: string) => {
    const response = await apiClient.post('/reset', { session_id: sessionId });
    return response.data;
};
