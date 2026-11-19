import { useEffect, useState } from 'react'
import { checkBackendHealth } from '../services/api'

export default function Header () {
  const [backendStatus, setBackendStatus] = useState('checking')

  useEffect(() => {
    const checkHealth = async () => {
      try {
        await checkBackendHealth()
        setBackendStatus('online')
      } catch {
        setBackendStatus('offline')
      }
    }

    checkHealth()
  }, [])

  const statusText = {
    checking: 'Checking Backend...',
    online: 'Backend Online',
    offline: 'Backend Offline'
  }

  return (
    <header className='header'>
      <div className='logo'>
        <span className='logo-icon'>🌱</span>

        <div>
          <h1>TerraSpectra</h1>
          <p>Hyperspectral Crop Disease Forecasting</p>
        </div>
      </div>

      <div className='header-status'>
        <span
          className={`status-dot ${backendStatus}`}
        ></span>

        <span>{statusText[backendStatus]}</span>
      </div>
    </header>
  )
}