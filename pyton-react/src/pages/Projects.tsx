import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import { useAuthStore } from '../store/authStore'

interface Project {
  project_id: number
  name: string
  description?: string
}

export default function Projects() {
  const [projects, setProjects] = useState<Project[]>([])
  const [showForm, setShowForm] = useState(false)
  const [newProject, setNewProject] = useState({ name: '', description: '' })
  const { role } = useAuthStore()
  const navigate = useNavigate()

  const loadProjects = async () => {
    const { data } = await api.get<Project[]>('/projects/')
    setProjects(data)
  }

  useEffect(() => { loadProjects() }, [])

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    await api.post('/projects/', newProject)
    setShowForm(false)
    setNewProject({ name: '', description: '' })
    loadProjects()
  }

  const handleDelete = async (project_id: number) => {
    if (!confirm('למחוק את הפרויקט?')) return
    await api.delete(`/projects/${project_id}`)
    loadProjects()
  }

  return (
    <>
      <nav className="navbar">
        <h2>📋 Task Manager</h2>
        <div className="navbar-links">
          <button className="btn-outline" onClick={() => navigate('/tasks')}>משימות</button>
          {role === 'admin' && <button className="btn-outline" onClick={() => navigate('/users')}>משתמשים</button>}
        </div>
      </nav>

      <div className="page-container">
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
            <h3>פרויקטים ({projects.length})</h3>
            {role === 'admin' && (
              <button className="btn-primary" onClick={() => setShowForm(!showForm)}>+ פרויקט חדש</button>
            )}
          </div>

          {showForm && (
            <form onSubmit={handleCreate} className="form-group card" style={{ marginBottom: 20 }}>
              <h4>פרויקט חדש</h4>
              <input placeholder="שם פרויקט *" required value={newProject.name} onChange={(e) => setNewProject({ ...newProject, name: e.target.value })} />
              <input placeholder="תיאור" value={newProject.description} onChange={(e) => setNewProject({ ...newProject, description: e.target.value })} />
              <div style={{ display: 'flex', gap: 8 }}>
                <button type="submit" className="btn-primary">שמור</button>
                <button type="button" className="btn-secondary" onClick={() => setShowForm(false)}>ביטול</button>
              </div>
            </form>
          )}

          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>שם הפרויקט</th>
                <th>תיאור</th>
                {role === 'admin' && <th>פעולות</th>}
              </tr>
            </thead>
            <tbody>
              {projects.length === 0 ? (
                <tr><td colSpan={4} style={{ textAlign: 'center', padding: 32, color: '#aaa' }}>אין פרויקטים להצגה</td></tr>
              ) : projects.map((p) => (
                <tr key={p.project_id}>
                  <td>{p.project_id}</td>
                  <td><strong>{p.name}</strong></td>
                  <td>{p.description ?? '-'}</td>
                  {role === 'admin' && (
                    <td><button className="btn-danger" onClick={() => handleDelete(p.project_id)}>🗑️ מחק</button></td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}
