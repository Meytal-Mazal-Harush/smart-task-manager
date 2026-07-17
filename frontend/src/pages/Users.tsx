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
  const [editingUser, setEditingUser] = useState<User | null>(null)
  const [editForm, setEditForm] = useState({ full_name: '', email: '', role: '', password: '123456' })
  const [showAddForm, setShowAddForm] = useState(false)
  const [addForm, setAddForm] = useState({ full_name: '', email: '', password: '', role: 'developer' })
  const navigate = useNavigate()

  const loadUsers = async () => {
    const { data } = await api.get<User[]>('/users/')
    setUsers([...data].sort((a, b) => (a.role === 'admin' ? -1 : b.role === 'admin' ? 1 : 0)))
  }

  useEffect(() => { loadUsers() }, [])

  const handleDelete = async (user_id: number) => {
    if (!confirm('למחוק את המשתמש?')) return
    await api.delete(`/users/${user_id}`)
    loadUsers()
  }

  const handleEditClick = (u: User) => {
    setEditingUser(u)
    setEditForm({ full_name: u.full_name, email: u.email, role: u.role, password: '123456' })
  }

  const handleEditSave = async () => {
    if (!editingUser) return
    await api.put(`/users/${editingUser.user_id}`, editForm)
    setEditingUser(null)
    loadUsers()
  }

  const handleAddSave = async () => {
    await api.post('/users/admin/add', addForm)
    setShowAddForm(false)
    setAddForm({ full_name: '', email: '', password: '', role: 'developer' })
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
          <div style={{ marginBottom: 20, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3>ניהול משתמשים ({users.length})</h3>
            <button className="btn-primary" onClick={() => setShowAddForm(true)}>+ הוסף משתמש</button>
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
                  <td style={{ display: 'flex', gap: 8 }}>
                    <button className="btn-outline" onClick={() => handleEditClick(u)}>✏️ ערוך</button>
                    {u.role !== 'admin' && <button className="btn-danger" onClick={() => handleDelete(u.user_id)}>🗑️ מחק</button>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {editingUser && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>עריכת משתמש</h3>
            <input placeholder="שם מלא" value={editForm.full_name} onChange={e => setEditForm({ ...editForm, full_name: e.target.value })} />
            <input placeholder="אימייל" value={editForm.email} onChange={e => setEditForm({ ...editForm, email: e.target.value })} />
            <select value={editForm.role} onChange={e => setEditForm({ ...editForm, role: e.target.value })}>
              <option value="developer">developer</option>
              <option value="admin">admin</option>
            </select>
            <div style={{ display: 'flex', gap: 8, marginTop: 12 }}>
              <button className="btn-primary" onClick={handleEditSave}>שמור</button>
              <button className="btn-outline" style={{ color: '#333', borderColor: '#ccc' }} onClick={() => setEditingUser(null)}>ביטול</button>
            </div>
          </div>
        </div>
      )}

      {showAddForm && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>הוספת משתמש</h3>
            <input placeholder="שם מלא" value={addForm.full_name} onChange={e => setAddForm({ ...addForm, full_name: e.target.value })} />
            <input placeholder="אימייל" value={addForm.email} onChange={e => setAddForm({ ...addForm, email: e.target.value })} />
            <input placeholder="סיסמה" type="password" value={addForm.password} onChange={e => setAddForm({ ...addForm, password: e.target.value })} />
            <select value={addForm.role} onChange={e => setAddForm({ ...addForm, role: e.target.value })}>
              <option value="developer">developer</option>
              <option value="admin">admin</option>
            </select>
            <div style={{ display: 'flex', gap: 8, marginTop: 12 }}>
              <button className="btn-primary" onClick={handleAddSave}>הוסף</button>
              <button className="btn-outline" style={{ color: '#333', borderColor: '#ccc' }} onClick={() => setShowAddForm(false)}>ביטול</button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
