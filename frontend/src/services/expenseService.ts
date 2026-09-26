import { api } from './api'
import type { Category, Dashboard, Expense, ExpenseInput } from '../types/expense'
export const expenseService = {
  list: (search = '') => api<Expense[]>(`/expenses?search=${encodeURIComponent(search)}`),
  get: (id: string) => api<Expense>(`/expenses/${id}`),
  create: (data: ExpenseInput) => api<Expense>('/expenses', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }),
  update: (id: string, data: ExpenseInput) => api<Expense>(`/expenses/${id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }),
  remove: (id: string) => api<void>(`/expenses/${id}`, { method: 'DELETE' }),
  categories: () => api<Category[]>('/categories'),
  dashboard: () => api<Dashboard>('/dashboard/summary'),
}
