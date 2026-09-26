import { api } from './api'
import type { OCRResult } from '../types/expense'
export const documentService = {
  upload: async (file: File) => { const body = new FormData(); body.append('file', file); return api<{id: number}>('/documents/upload', { method: 'POST', body }) },
  extract: (id: number) => api<OCRResult>(`/documents/${id}/extract`, { method: 'POST' }),
}
