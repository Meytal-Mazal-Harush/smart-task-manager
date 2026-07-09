import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import { useAuthStore } from '../store/authStore'

interface Task {
  task_id: number
  title: string
  description?: string
  priority: number
  due_date?: string
  status: string
  approved: boolean
  project_id: number
  assigned_to?: number
}

export default function Tasks() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [showForm, setShowForm] = useState(false)
  const [filterStatus, setFilterStatus] = useState('')
  const [filterPriority, setFilterPriority] = useState('')
  const [filterTitle, setFilterTitle] = useState('')
  const [newTask, setNewTask] = useState({ title: '', description: '', priority: 1, due_date: '', project_id: 1 })
  const { logout, full_name, role } = useAuthStore()
  const navigate = useNavigate()

  const loadTasks = async () => {
    const params: Record<string, string> = {}
    if (filterStatus) params.status = filterStatus
    if (filterPriority) params.priority = filterPriority
    if (filterTitle) params.title = filterTitle
    const { data } = await api.get<Task[]>('/tasks/', { params })
    setTasks(data)
  }

  useEffect(() => { loadTasks() }, [filterStatus, filterPriority, filterTitle])

  const handleLogout = () => { logout(); navigate('/login') }

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    await api.post('/tasks/', newTask)
    setShowForm(false)
    setNewTask({ title: '', description: '', priority: 1, due_date: '', project_id: 1 })
    loadTasks()
  }

  const handleStatusChange = async (task_id: number, status: string) => {
    await api.put(`/tasks/${task_id}`, { status })
    loadTasks()
  }

  const handleDelete = async (task_id: number) => {
    if (!confirm('למחוק את המשימה?')) return
    await api.delete(`/tasks/${task_id}`)
    loadTasks()
  }

  const handleApprove = async (task_id: number) => {
    await api.put(`/tasks/${task_id}`, { approved: true, status: 'closed' })
    loadTasks()
  }

  const priorityLabel = (p: number) => p === 1 ? '🟢 נמוך' : p === 2 ? '🟡 בינוני' : '🔴 גבוה'

  return (
    <>
      <nav className="navbar">
        <h2>📋 Task Manager</h2>
        <div className="navbar-links">
          <span style={{ color: '#aaa', fontSize: '0.9rem' }}>שלום, {full_name} | <span className={`badge badge-${role}`}>{role}</span></span>
          <button className="btn-outline" onClick={() => navigate('/projects')}>פרויקטים</button>
          {role === 'admin' && <button className="btn-outline" onClick={() => navigate('/users')}>משתמשים</button>}
          <button className="btn-danger" onClick={handleLogout}>התנתק</button>
        </div>
      </nav>

      <div className="page-container">
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <h3>משימות ({tasks.length})</h3>
            {role === 'admin' && (
              <button className="btn-primary" onClick={() => setShowForm(!showForm)}>+ משימה חדשה</button>
            )}
          </div>

          <div className="filter-bar">
            <input placeholder="🔍 חיפוש לפי כותרת" value={filterTitle} onChange={(e) => setFilterTitle(e.target.value)} style={{ minWidth: 200 }} />
            <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
              <option value="">כל הסטטוסים</option>
              <option value="open">פתוח</option>
              <option value="in_progress">בתהליך</option>
              <option value="closed">סגור</option>
            </select>
            <select value={filterPriority} onChange={(e) => setFilterPriority(e.target.value)}>
              <option value="">כל העדיפויות</option>
              <option value="1">נמוך</option>
              <option value="2">בינוני</option>
              <option value="3">גבוה</option>
            </select>
          </div>

          {showForm && (
            <form onSubmit={handleCreate} className="form-group card" style={{ marginBottom: 20 }}>
              <h4>משימה חדשה</h4>
              <input placeholder="כותרת *" required value={newTask.title} onChange={(e) => setNewTask({ ...newTask, title: e.target.value })} />
              <input placeholder="תיאור" value={newTask.description} onChange={(e) => setNewTask({ ...newTask, description: e.target.value })} />
              <select value={newTask.priority} onChange={(e) => setNewTask({ ...newTask, priority: Number(e.target.value) })}>
                <option value={1}>🟢 נמוך</option>
                <option value={2}>🟡 בינוני</option>
                <option value={3}>🔴 גבוה</option>
              </select>
              <input type="date" value={newTask.due_date} onChange={(e) => setNewTask({ ...newTask, due_date: e.target.value })} />
              <input type="number" placeholder="מזהה פרויקט *" required value={newTask.project_id} onChange={(e) => setNewTask({ ...newTask, project_id: Number(e.target.value) })} />
              <div style={{ display: 'flex', gap: 8 }}>
                <button type="submit" className="btn-primary">שמור</button>
                <button type="button" className="btn-secondary" onClick={() => setShowForm(false)}>ביטול</button>
              </div>
            </form>
          )}

          <table>
            <thead>
              <tr>
                <th>כותרת</th>
                <th>עדיפות</th>
                <th>סטטוס</th>
                <th>תאריך יעד</th>
                <th>אושר</th>
                <th>פעולות</th>
              </tr>
            </thead>
            <tbody>
              {tasks.length === 0 ? (
                <tr><td colSpan={6} style={{ textAlign: 'center', padding: 32, color: '#aaa' }}>אין משימות להצגה</td></tr>
              ) : tasks.map((t) => (
                <tr key={t.task_id}>
                  <td><strong>{t.title}</strong>{t.description && <div style={{ fontSize: '0.8rem', color: '#888' }}>{t.description}</div>}</td>
                  <td>{priorityLabel(t.priority)}</td>
                  <td>
                    {t.approved ? (
                      <span className="badge badge-closed">סגור</span>
                    ) : (
                      <select className={`badge badge-${t.status}`} value={t.status} onChange={(e) => handleStatusChange(t.task_id, e.target.value)}>
                        <option value="open">פתוח</option>
                        <option value="in_progress">בתהליך</option>
                        <option value="closed">סגור</option>
                      </select>
                    )}
                  </td>
                  <td>{t.due_date ?? '-'}</td>
                  <td>{t.approved ? '✅ אושר' : '⏳ ממתין'}</td>
                  <td style={{ display: 'flex', gap: 6 }}>
                    {role === 'admin' && !t.approved && t.status === 'closed' && (
                      <button className="btn-success" onClick={() => handleApprove(t.task_id)}>✔ אשר</button>
                    )}
                    {role === 'admin' && (
                      <button className="btn-danger" onClick={() => handleDelete(t.task_id)}>🗑️</button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}
