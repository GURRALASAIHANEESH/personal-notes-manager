import React, { createContext, useContext, useState, useEffect } from 'react'
import api from '../api/axiosClient'

const AuthContext = createContext(null)

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const saved = localStorage.getItem('notes_user')
    if (saved) {
      const parsed = JSON.parse(saved)
      setUser(parsed.user)
      window.__authToken = parsed.token
    }
    setIsLoading(false)
  }, [])

  const login = async (email, password) => {
    const res = await api.post('/auth/login', { email, password })
    const { access_token, user: userData } = res.data
    window.__authToken = access_token
    localStorage.setItem('notes_user', JSON.stringify({ token: access_token, user: userData }))
    setUser(userData)
    return userData
  }

  const register = async (email, password) => {
    const res = await api.post('/auth/register', { email, password })
    const { access_token, user: userData } = res.data
    window.__authToken = access_token
    localStorage.setItem('notes_user', JSON.stringify({ token: access_token, user: userData }))
    setUser(userData)
    return userData
  }

  const logout = () => {
    window.__authToken = null
    localStorage.removeItem('notes_user')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, login, register, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
