import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

interface User {
  user_id: number
  full_name: string
  email: string
  role: string
}

export default function Users() {
  const [users, setUsers] = useState<User[]>([])
  const navigate = useNavigate()

  const loadUsers = async () => {
    const { data } = await api.get<User[]>('/users/')
    setUsers(data)
  }

  useEffect(() => { loadUsers() }, [])

  const handleDelete = async (user_id: number) => {
    if (!confirm('למחוק את המשתמש?')) return
    await api.delete(`/users/${user_id}`)
    loadUsers()
  }

  return (
    <>
      <nav className="navbar">
        <h2>📋 Task Manager</h2>
        <div className="navbar-links">
          <button className="btn-outline" onClick={() => navigate('/tasks')}>משימות</button>
          <button className="btn-outline" onClick={() => navigate('/projects')}>פרויקטים</button>
        </div>
      </nav>

      <div className="page-container">
        <div className="card">
          <div style={{ marginBottom: 20 }}>
            <h3>ניהול משתמשים ({users.length})</h3>
          </div>

          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>שם מלא</th>
                <th>אימייל</th>
                <th>תפקיד</th>
                <th>פעולות</th>
              </tr>
            </thead>
            <tbody>
              {users.length === 0 ? (
                <tr><td colSpan={5} style={{ textAlign: 'center', padding: 32, color: '#aaa' }}>אין משתמשים להצגה</td></tr>
              ) : users.map((u) => (
                <tr key={u.user_id}>
                  <td>{u.user_id}</td>
                  <td><strong>{u.full_name}</strong></td>
                  <td>{u.email}</td>
                  <td><span className={`badge badge-${u.role}`}>{u.role}</span></td>
                  <td><button className="btn-danger" onClick={() => handleDelete(u.user_id)}>🗑️ מחק</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}
