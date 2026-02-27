import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import api from '../api/axiosClient'

export default function NoteDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [note, setNote] = useState(null)
  const [error, setError] = useState('')
  const [summary, setSummary] = useState('')
  const [suggestedTags, setSuggestedTags] = useState([])
  const [aiLoading, setAiLoading] = useState('')  // 'summarize' | 'tags' | ''

  useEffect(() => {
    api.get(`/notes/${id}`)
      .then(res => setNote(res.data.note))
      .catch(() => setError('Note not found or access denied'))
  }, [id])

  const handleSummarize = async () => {
    setAiLoading('summarize')
    setSummary('')
    try {
      const res = await api.post(`/notes/${id}/summarize`)
      setSummary(res.data.summary)
    } catch {
      setSummary('AI service unavailable. Try again.')
    } finally { setAiLoading('') }
  }

  const handleSuggestTags = async () => {
    setAiLoading('tags')
    setSuggestedTags([])
    try {
      const res = await api.post(`/notes/${id}/suggest-tags`)
      setSuggestedTags(res.data.suggested_tags)
    } catch {
      setSuggestedTags([])
    } finally { setAiLoading('') }
  }

  if (error) return (
    <div style={styles.page}><div style={styles.card}>
      <div style={styles.error}>{error}</div>
      <button style={styles.backBtn} onClick={() => navigate('/dashboard')}>← Back</button>
    </div></div>
  )
  if (!note) return <div style={styles.page}><div style={styles.loading}>Loading...</div></div>

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <button style={styles.backBtn} onClick={() => navigate('/dashboard')}>← Dashboard</button>
        <h1 style={styles.title}>{note.title}</h1>

        <div style={styles.meta}>
          <span style={note.is_private ? styles.badgePrivate : styles.badgePublic}>
            {note.is_private ? '🔒 Private' : '🌐 Public'}
          </span>
          <span style={styles.date}>Updated: {new Date(note.updated_at).toLocaleString()}</span>
        </div>

        {note.tags?.length > 0 && (
          <div style={styles.tags}>
            {note.tags.map(tag => <span key={tag} style={styles.tag}>#{tag}</span>)}
          </div>
        )}

        <p style={styles.content}>{note.content}</p>

        {/* AI Actions */}
        <div style={styles.aiSection}>
          <h3 style={styles.aiHeading}>🤖 AI Assistant</h3>
          <div style={styles.aiButtons}>
            <button style={styles.aiBtn} onClick={handleSummarize} disabled={!!aiLoading}>
              {aiLoading === 'summarize' ? '⏳ Summarizing...' : '✨ Summarize Note'}
            </button>
            <button style={styles.aiBtn} onClick={handleSuggestTags} disabled={!!aiLoading}>
              {aiLoading === 'tags' ? '⏳ Thinking...' : '🏷️ Suggest Tags'}
            </button>
          </div>

          {summary && (
            <div style={styles.aiResult}>
              <strong>Summary:</strong>
              <p style={styles.aiText}>{summary}</p>
            </div>
          )}

          {suggestedTags.length > 0 && (
            <div style={styles.aiResult}>
              <strong>Suggested Tags:</strong>
              <div style={styles.suggestedTags}>
                {suggestedTags.map(tag => (
                  <span key={tag} style={styles.suggestedTag}>#{tag}</span>
                ))}
              </div>
            </div>
          )}
        </div>

      </div>
    </div>
  )
}

const styles = {
  page: { minHeight: '100vh', background: '#f0f2f5', display: 'flex', justifyContent: 'center', paddingTop: '40px', paddingBottom: '40px' },
  card: { background: '#fff', borderRadius: '12px', padding: '36px', width: '600px', maxWidth: '95vw', boxShadow: '0 2px 16px rgba(0,0,0,0.1)', height: 'fit-content' },
  backBtn: { background: 'none', border: 'none', color: '#4f46e5', cursor: 'pointer', fontSize: '14px', marginBottom: '20px', padding: 0 },
  title: { fontSize: '24px', fontWeight: '700', marginBottom: '12px' },
  meta: { display: 'flex', gap: '12px', alignItems: 'center', marginBottom: '14px' },
  date: { fontSize: '13px', color: '#888' },
  tags: { display: 'flex', gap: '6px', flexWrap: 'wrap', marginBottom: '20px' },
  tag: { background: '#ede9fe', color: '#7c3aed', padding: '3px 10px', borderRadius: '12px', fontSize: '13px' },
  content: { fontSize: '16px', lineHeight: '1.8', color: '#333', whiteSpace: 'pre-wrap', marginBottom: '28px' },
  badgePrivate: { fontSize: '12px', background: '#fef3c7', color: '#92400e', padding: '3px 8px', borderRadius: '12px' },
  badgePublic: { fontSize: '12px', background: '#d1fae5', color: '#065f46', padding: '3px 8px', borderRadius: '12px' },
  error: { color: '#dc2626', marginBottom: '14px' },
  loading: { fontSize: '18px', color: '#888' },
  aiSection: { borderTop: '1px solid #f0f0f0', paddingTop: '20px' },
  aiHeading: { fontSize: '15px', fontWeight: '600', marginBottom: '12px', color: '#4f46e5' },
  aiButtons: { display: 'flex', gap: '10px', marginBottom: '16px', flexWrap: 'wrap' },
  aiBtn: { padding: '9px 18px', background: '#4f46e5', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '14px', fontWeight: '500' },
  aiResult: { background: '#f5f3ff', borderRadius: '8px', padding: '14px', marginBottom: '12px' },
  aiText: { marginTop: '6px', fontSize: '14px', lineHeight: '1.6', color: '#333' },
  suggestedTags: { display: 'flex', gap: '6px', flexWrap: 'wrap', marginTop: '8px' },
  suggestedTag: { background: '#4f46e5', color: '#fff', padding: '3px 10px', borderRadius: '12px', fontSize: '13px' },
}
