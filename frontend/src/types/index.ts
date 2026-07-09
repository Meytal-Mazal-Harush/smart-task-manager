export interface User {
  user_id: number
  full_name: string
  email: string
  role: string
}

export interface Task {
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

export interface Project {
  project_id: number
  name: string
  description?: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  role: string
  full_name: string
}
