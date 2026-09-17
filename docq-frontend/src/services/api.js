import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({ baseURL: BASE_URL });

// For now, skip Supabase auth attachment (will add when API is ready)
api.interceptors.request.use((config) => {
  // TODO: Add Supabase JWT when auth is set up
  return config;
});

// ── Documents ──────────────────────────────────────
export const getDocuments = ()            => api.get('/documents');
export const uploadDocument = (formData, config = {})  => api.post('/documents/upload', formData, {
  headers: { 'Content-Type': 'multipart/form-data' },
  ...config,
});
export const deleteDocument = (id)        => api.delete(`/documents/${id}`);

// ── Chats ──────────────────────────────────────────
export const getChats = ()                => api.get('/chats');
export const createChat = (documentId)    => api.post('/chats', { document_id: documentId });
export const deleteChat = (id)            => api.delete(`/chats/${id}`);

// ── Messages ───────────────────────────────────────
export const getMessages = (chatId)       => api.get(`/chats/${chatId}/messages`);
export const sendMessage = (chatId, text) => api.post(`/chats/${chatId}/messages`, { content: text });

// ── User ───────────────────────────────────────────
export const getProfile   = ()            => api.get('/users/me');
export const updateProfile = (data)       => api.put('/users/me', data);

export default api;

