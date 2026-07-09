import { create } from 'zustand'

interface AuthState {
  token: string | null
  role: string | null
  full_name: string | null
  setAuth: (token: string, role: string, full_name: string) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('token'),
  role: localStorage.getItem('role'),
  full_name: localStorage.getItem('full_name'),
  setAuth: (token, role, full_name) => {
    localStorage.setItem('token', token)
    localStorage.setItem('role', role)
    localStorage.setItem('full_name', full_name)
    set({ token, role, full_name })
  },
  logout: () => {
    localStorage.clear()
    set({ token: null, role: null, full_name: null })
  }
}))
