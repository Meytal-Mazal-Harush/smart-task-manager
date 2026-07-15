import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import { useAuthStore } from '../store/authStore'

interface LoginResponse {
  access_token: string
  token_type: string
  role: string
  full_name: string
  user_id: number
}

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const setAuth = useAuthStore((s) => s.setAuth)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const { data } = await api.post<LoginResponse>('/users/login', {
        full_name: 'placeholder',
        email,
        password
      })
      setAuth(data.access_token, data.role, data.full_name, data.user_id)
      navigate('/tasks')
    } catch {
      setError('אימייל או סיסמה שגויים')
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>📋 Task Manager</h2>
        <p>מערכת ניהול משימות חכמה</p>
        <form onSubmit={handleSubmit} className="form-group">
          <input
            type="email"
            placeholder="אימייל"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="סיסמה"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && <p className="error-msg">{error}</p>}
          <button type="submit">התחבר</button>
        </form>
        <p style={{ textAlign: 'center', marginTop: 16, color: '#888' }}>
          אין לך חשבון? <span style={{ color: '#0f3460', cursor: 'pointer' }} onClick={() => navigate('/register')}>הרשם</span>
        </p>
      </div>
    </div>
  )
}
