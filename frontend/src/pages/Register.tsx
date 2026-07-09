import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

export default function Register() {
  const [form, setForm] = useState({ full_name: '', email: '', password: '', role: 'developer' })
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await api.post('/users/register', form)
      setSuccess('המשתמש נוצר בהצלחה! מעביר להתחברות...')
      setTimeout(() => navigate('/login'), 2000)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'שגיאה ביצירת המשתמש')
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>📋 Task Manager</h2>
        <p>יצירת משתמש חדש</p>
        <form onSubmit={handleSubmit} className="form-group">
          <input placeholder="שם מלא" required value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} />
          <input type="email" placeholder="אימייל" required value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
          <input type="password" placeholder="סיסמה (לפחות 6 תווים)" required value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
          {error && <p className="error-msg">{error}</p>}
          {success && <p style={{ color: '#27ae60', textAlign: 'center' }}>{success}</p>}
          <button type="submit">הרשם</button>
        </form>
        <p style={{ textAlign: 'center', marginTop: 16, color: '#888' }}>
          יש לך כבר חשבון? <span style={{ color: '#0f3460', cursor: 'pointer' }} onClick={() => navigate('/login')}>התחבר</span>
        </p>
      </div>
    </div>
  )
}
