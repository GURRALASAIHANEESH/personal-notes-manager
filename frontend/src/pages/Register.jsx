import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Register() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    if (form.password.length < 8) { setError('Password must be at least 8 characters'); return }
    setLoading(true)
    try {
      await register(form.email, form.password)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.message || 'Registration failed')
    } finally { setLoading(false) }
  }

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h1 style={styles.title}>Notes Manager</h1>
        <h2 style={styles.subtitle}>Create Account</h2>
        {error && <div style={styles.error}>{error}</div>}
        <form onSubmit={handleSubmit}>
          <input style={styles.input} type="email" placeholder="Email" required value={form.email} onChange={e => setForm({...form, email: e.target.value})} />
          <input style={styles.input} type="password" placeholder="Password (min 8 chars)" required value={form.password} onChange={e => setForm({...form, password: e.target.value})} />
          <button style={styles.btn} type="submit" disabled={loading}>{loading ? 'Creating...' : 'Create Account'}</button>
        </form>
        <p style={styles.link}>Have an account? <Link to="/login">Sign In</Link></p>
      </div>
    </div>
  )
}

const styles = {
  page: { minHeight: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center', background: '#f0f2f5' },
  card: { background: '#fff', padding: '40px', borderRadius: '12px', boxShadow: '0 2px 16px rgba(0,0,0,0.1)', width: '360px' },
  title: { textAlign: 'center', marginBottom: '8px', fontSize: '24px' },
  subtitle: { textAlign: 'center', marginBottom: '24px', color: '#555', fontWeight: '500' },
  input: { width: '100%', padding: '10px 14px', marginBottom: '14px', border: '1px solid #ddd', borderRadius: '8px', fontSize: '15px', display: 'block' },
  btn: { width: '100%', padding: '11px', background: '#4f46e5', color: '#fff', border: 'none', borderRadius: '8px', fontSize: '15px', cursor: 'pointer', fontWeight: '600' },
  error: { background: '#fef2f2', color: '#dc2626', padding: '10px', borderRadius: '8px', marginBottom: '14px', fontSize: '14px' },
  link: { textAlign: 'center', marginTop: '16px', fontSize: '14px', color: '#555' }
}
