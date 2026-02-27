import React, { useEffect, useState } from 'react'
import api from '../api/axiosClient'

export default function StatsWidget() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/stats')
      .then(res => setStats(res.data))
      .catch(() => setStats(null))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div style={styles.card}>Loading stats...</div>
  if (!stats) return null

  return (
    <div style={styles.card}>
      <h3 style={styles.heading}>📊 Your Dashboard</h3>
      <div style={styles.grid}>
        <div style={styles.stat}>
          <span style={styles.number}>{stats.total_notes}</span>
          <span style={styles.label}>Total Notes</span>
        </div>
        <div style={styles.stat}>
          <span style={styles.number}>{stats.private_notes}</span>
          <span style={styles.label}>Private</span>
        </div>
        <div style={styles.stat}>
          <span style={styles.number}>{stats.public_notes}</span>
          <span style={styles.label}>Public</span>
        </div>
        {stats.total_users !== undefined && (
          <div style={styles.stat}>
            <span style={styles.number}>{stats.total_users}</span>
            <span style={styles.label}>Users</span>
          </div>
        )}
      </div>
      {stats.top_tags?.length > 0 && (
        <div style={styles.tagsSection}>
          <span style={styles.tagsLabel}>Top Tags: </span>
          {stats.top_tags.map(({ tag, count }) => (
            <span key={tag} style={styles.tag}>#{tag} ({count})</span>
          ))}
        </div>
      )}
    </div>
  )
}

const styles = {
  card: { background: '#fff', borderRadius: '10px', padding: '20px', boxShadow: '0 1px 6px rgba(0,0,0,0.08)', marginBottom: '20px' },
  heading: { fontSize: '16px', fontWeight: '600', marginBottom: '16px', color: '#1a1a1a' },
  grid: { display: 'flex', gap: '16px', flexWrap: 'wrap', marginBottom: '14px' },
  stat: { display: 'flex', flexDirection: 'column', alignItems: 'center', background: '#f5f3ff', borderRadius: '8px', padding: '12px 20px', minWidth: '80px' },
  number: { fontSize: '24px', fontWeight: '700', color: '#4f46e5' },
  label: { fontSize: '12px', color: '#666', marginTop: '2px' },
  tagsSection: { display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: '6px' },
  tagsLabel: { fontSize: '13px', color: '#666' },
  tag: { background: '#ede9fe', color: '#7c3aed', padding: '2px 8px', borderRadius: '12px', fontSize: '12px' },
}
