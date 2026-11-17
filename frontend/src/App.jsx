import { useEffect, useState } from 'react'
import api from './api/client'

export default function App() {
  const [status, setStatus] = useState('verificando...')

  useEffect(() => {
    api.get('/health')
      .then((res) => setStatus(`API respondeu: ${res.data.status}`))
      .catch((err) => setStatus(`Falha: ${err.message}`))
  }, [])

  return <h1>{status}</h1>
}