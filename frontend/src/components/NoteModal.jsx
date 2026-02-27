import React, { useState } from 'react'
import api from '../api/axiosClient'

export default function NoteModal({ note, onClose, onSaved }) {
  const isEdit = !!note
  const [form, setForm] = useState({
    title: note?.title || '',
    content: note?.content || '',
    tags: note?.tags?.join(', ') || '',
    is_private: note?.is_private ?? true,
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    const payload = {
      title: form.title,
      content: form.content,
      tags: form.tags.split(',').map(t => t.trim()).filter(Boolean),
      is_private: form.is_private,
    }
    try {
      if (isEdit) { await api.put(`/notes/${note.id}`, payload) }
      else { await api.post('/notes', payload) }
      onSaved()
      onClose()
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to save note')
    } finally { setLoading(false) }
  }

  return (
    <div style={styles.overlay} onClick={onClose}>
      <div style={styles.modal} onClick={e => e.stopPropagation()}>
        <h2 style={styles.heading}>{isEdit ? 'Edit Note' : 'New Note'}</h2>
        {error && <div style={styles.error}>{error}</div>}
        <form onSubmit={handleSubmit}>
          <input style={styles.input} placeholder="Title" required value={form.title} onChange={e => setForm({...form, title: e.target.value})} />
          <textarea style={styles.textarea} placeholder="Content" required rows={6} value={form.content} onChange={e => setForm({...form, content: e.target.value})} />
          <input style={styles.input} placeholder="Tags (comma separated)" value={form.tags} onChange={e => setForm({...form, tags: e.target.value})} />
          <label style={styles.checkLabel}>
            <input type="checkbox" checked={form.is_private} onChange={e => setForm({...form, is_private: e.target.checked})} />
            &nbsp; Private note
          </label>
          <div style={styles.actions}>
            <button type="button" style={styles.cancelBtn} onClick={onClose}>Cancel</button>
            <button type="submit" style={styles.saveBtn} disabled={loading}>{loading ? 'Saving...' : 'Save Note'}</button>
          </div>
        </form>
      </div>
    </div>
  )
}

const styles = {
  overlay: { position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.45)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 100 },
  modal: { background: '#fff', borderRadius: '12px', padding: '32px', width: '480px', maxWidth: '95vw' },
  heading: { marginBottom: '20px', fontSize: '20px' },
  input: { width: '100%', padding: '10px 14px', marginBottom: '12px', border: '1px solid #ddd', borderRadius: '8px', fontSize: '15px', display: 'block' },
  textarea: { width: '100%', padding: '10px 14px', marginBottom: '12px', border: '1px solid #ddd', borderRadius: '8px', fontSize: '15px', resize: 'vertical', fontFamily: 'inherit' },
  checkLabel: { display: 'flex', alignItems: 'center', marginBottom: '20px', fontSize: '14px', cursor: 'pointer' },
  actions: { display: 'flex', gap: '10px', justifyContent: 'flex-end' },
  cancelBtn: { padding: '9px 20px', border: '1px solid #ddd', borderRadius: '8px', background: '#fff', cursor: 'pointer', fontSize: '14px' },
  saveBtn: { padding: '9px 20px', background: '#4f46e5', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '14px', fontWeight: '600' },
  error: { background: '#fef2f2', color: '#dc2626', padding: '10px', borderRadius: '8px', marginBottom: '14px', fontSize: '14px' },
}
