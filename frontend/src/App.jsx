import { useState } from 'react'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import AIAssistant from './pages/AIAssistant'

function App() {
  const [activePage, setActivePage] = useState('dashboard')

  return (
    <div className="app">
      <Header />

      <div className="main-layout">
        <Sidebar
          activePage={activePage}
          setActivePage={setActivePage}
        />

        {activePage === 'dashboard' && <Dashboard />}

        {activePage === 'ai' && <AIAssistant />}
      </div>
    </div>
  )
}

export default App