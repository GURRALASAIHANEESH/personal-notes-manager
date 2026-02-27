import React, { useState, useEffect, useCallback } from 'react'
import { useAuth } from '../context/AuthContext'
import api from '../api/axiosClient'
import NoteCard from '../components/NoteCard'
import NoteModal from '../components/NoteModal'
import StatsWidget from '../components/StatsWidget'

export default function Dashboard() {
  const { user, logout } = useAuth()
  const [notes, setNotes] = useState([])
  const [pagination, setPagination] = useState({})
  const [search, setSearch] = useState('')
  const [tag, setTag] = useState('')
  const [page, setPage] = useState(1)
  const [showModal, setShowModal] = useState(false)
  const [editNote, setEditNote] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [statsKey, setStatsKey] = useState(0) // increment to refresh stats

  const fetchNotes = useCallback(async () => {
    setLoading(true); setError('')
    try {
      const params = { page, per_page: 8 }
      if (search) params.q = search
      if (tag) params.tag = tag
      const res = await api.get('/notes', { params })
      setNotes(res.data.notes)
      setPagination(res.data.pagination)
    } catch { setError('Failed to load notes') }
    finally { setLoading(false) }
  }, [page, search, tag])

  useEffect(() => { fetchNotes() }, [fetchNotes])

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this note?')) return
    await api.delete(`/notes/${id}`)
    fetchNotes()
    setStatsKey(k => k + 1) // refresh stats after delete
  }

  const handleSaved = () => {
    fetchNotes()
    setStatsKey(k => k + 1) // refresh stats after create/edit
  }

  return (
    <div style={styles.page}>
      {/* Navbar */}
      <nav style={styles.nav}>
        <span style={styles.brand}>📝 Notes Manager</span>
        <div style={styles.navRight}>
          <span style={styles.userEmail}>{user?.email}</span>
          <span style={styles.role}>{user?.role}</span>
          <button style={styles.logoutBtn} onClick={logout}>Logout</button>
        </div>
      </nav>

      <div style={styles.container}>

        {/* Stats Widget — re-renders on statsKey change */}
        <StatsWidget key={statsKey} />

        {/* Toolbar */}
        <div style={styles.toolbar}>
          <input style={styles.search} placeholder="🔍 Search notes..."
            value={search} onChange={e => { setSearch(e.target.value); setPage(1) }} />
          <input style={styles.search} placeholder="🏷️ Filter by tag..."
            value={tag} onChange={e => { setTag(e.target.value); setPage(1) }} />
          <button style={styles.newBtn} onClick={() => { setEditNote(null); setShowModal(true) }}>
            + New Note
          </button>
        </div>

        {error && <div style={styles.error}>{error}</div>}
        {loading && <div style={styles.loading}>Loading...</div>}
        {!loading && notes.length === 0 && (
          <div style={styles.empty}>No notes found. Create your first note!</div>
        )}

        {notes.map(note => (
          <NoteCard key={note.id} note={note}
            onEdit={(n) => { setEditNote(n); setShowModal(true) }}
            onDelete={handleDelete} />
        ))}

        {/* Pagination */}
        {pagination.pages > 1 && (
          <div style={styles.pager}>
            <button disabled={!pagination.has_prev} style={styles.pageBtn}
              onClick={() => setPage(p => p - 1)}>← Prev</button>
            <span style={styles.pageInfo}>Page {pagination.page} of {pagination.pages}</span>
            <button disabled={!pagination.has_next} style={styles.pageBtn}
              onClick={() => setPage(p => p + 1)}>Next →</button>
          </div>
        )}
      </div>

      {showModal && (
        <NoteModal note={editNote} onClose={() => setShowModal(false)} onSaved={handleSaved} />
      )}
    </div>
  )
}

const styles = {
  page: { minHeight: '100vh', background: '#f0f2f5' },
  nav: { background: '#fff', padding: '14px 32px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', boxShadow: '0 1px 4px rgba(0,0,0,0.08)' },
  brand: { fontWeight: '700', fontSize: '18px' },
  navRight: { display: 'flex', alignItems: 'center', gap: '12px' },
  userEmail: { fontSize: '14px', color: '#555' },
  role: { background: '#ede9fe', color: '#7c3aed', padding: '2px 10px', borderRadius: '12px', fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' },
  logoutBtn: { padding: '7px 16px', border: '1px solid #ddd', borderRadius: '8px', background: '#fff', cursor: 'pointer', fontSize: '14px' },
  container: { maxWidth: '720px', margin: '32px auto', padding: '0 16px' },
  toolbar: { display: 'flex', gap: '10px', marginBottom: '20px', flexWrap: 'wrap' },
  search: { flex: 1, minWidth: '160px', padding: '9px 14px', border: '1px solid #ddd', borderRadius: '8px', fontSize: '14px' },
  newBtn: { padding: '9px 20px', background: '#4f46e5', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600', fontSize: '14px' },
  error: { background: '#fef2f2', color: '#dc2626', padding: '12px', borderRadius: '8px', marginBottom: '14px' },
  loading: { textAlign: 'center', color: '#888', padding: '40px' },
  empty: { textAlign: 'center', color: '#999', padding: '60px 0', fontSize: '16px' },
  pager: { display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '16px', marginTop: '24px' },
  pageBtn: { padding: '8px 18px', border: '1px solid #ddd', borderRadius: '8px', background: '#fff', cursor: 'pointer', fontSize: '14px' },
  pageInfo: { fontSize: '14px', color: '#555' },
}
