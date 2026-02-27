import React from 'react'
import { useNavigate } from 'react-router-dom'

export default function NoteCard({ note, onEdit, onDelete }) {
  const navigate = useNavigate()
  return (
    <div style={styles.card}>
      <div style={styles.header}>
        <span style={styles.title} onClick={() => navigate(`/notes/${note.id}`)}>{note.title}</span>
        <span style={note.is_private ? styles.badgePrivate : styles.badgePublic}>
          {note.is_private ? 'Private' : 'Public'}
        </span>
      </div>
      <p style={styles.content}>{note.content.slice(0, 120)}{note.content.length > 120 ? '...' : ''}</p>
      {note.tags?.length > 0 && (
        <div style={styles.tags}>
          {note.tags.map(tag => <span key={tag} style={styles.tag}>#{tag}</span>)}
        </div>
      )}
      <div style={styles.footer}>
        <span style={styles.date}>{new Date(note.updated_at).toLocaleDateString()}</span>
        <div style={styles.actions}>
          <button style={styles.editBtn} onClick={() => onEdit(note)}>Edit</button>
          <button style={styles.deleteBtn} onClick={() => onDelete(note.id)}>Delete</button>
        </div>
      </div>
    </div>
  )
}

const styles = {
  card: { background: '#fff', borderRadius: '10px', padding: '20px', boxShadow: '0 1px 6px rgba(0,0,0,0.08)', marginBottom: '14px' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' },
  title: { fontWeight: '600', fontSize: '16px', cursor: 'pointer', color: '#4f46e5' },
  content: { color: '#555', fontSize: '14px', lineHeight: '1.5', marginBottom: '10px' },
  tags: { display: 'flex', gap: '6px', flexWrap: 'wrap', marginBottom: '10px' },
  tag: { background: '#ede9fe', color: '#7c3aed', padding: '2px 8px', borderRadius: '12px', fontSize: '12px' },
  badgePrivate: { fontSize: '12px', background: '#fef3c7', color: '#92400e', padding: '3px 8px', borderRadius: '12px' },
  badgePublic: { fontSize: '12px', background: '#d1fae5', color: '#065f46', padding: '3px 8px', borderRadius: '12px' },
  footer: { display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  date: { fontSize: '12px', color: '#999' },
  actions: { display: 'flex', gap: '8px' },
  editBtn: { padding: '5px 14px', border: '1px solid #ddd', borderRadius: '6px', background: '#fff', cursor: 'pointer', fontSize: '13px' },
  deleteBtn: { padding: '5px 14px', border: '1px solid #fecaca', borderRadius: '6px', background: '#fff5f5', color: '#dc2626', cursor: 'pointer', fontSize: '13px' },
}
