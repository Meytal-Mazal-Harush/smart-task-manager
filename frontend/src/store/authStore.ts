import { create } from 'zustand'

interface AuthState {
  token: string | null
  role: string | null
  full_name: string | null
  user_id: number | null
  setAuth: (token: string, role: string, full_name: string, user_id: number) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('token'),
  role: localStorage.getItem('role'),
  full_name: localStorage.getItem('full_name'),
  user_id: localStorage.getItem('user_id') ? Number(localStorage.getItem('user_id')) : null,
  setAuth: (token, role, full_name, user_id) => {
    localStorage.setItem('token', token)
    localStorage.setItem('role', role)
    localStorage.setItem('full_name', full_name)
    localStorage.setItem('user_id', String(user_id))
    set({ token, role, full_name, user_id })
  },
  logout: () => {
    localStorage.clear()
    set({ token: null, role: null, full_name: null, user_id: null })
  }
}))
