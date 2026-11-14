import { useState } from 'react'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import AIAssistant from './pages/AIAssistant'

function App() {
  const [activePage, setActivePage] = useState('dashboard')
  const [selectedZone, setSelectedZone] = useState(null)

  const openAIForZone = (zone) => {
    setSelectedZone(zone)
    setActivePage('ai')
  }

  return (
    <div className="app">
      <Header />

      <div className="main-layout">
        <Sidebar
          activePage={activePage}
          setActivePage={setActivePage}
        />

        {activePage === 'dashboard' && (
          <Dashboard
            onAskAI={openAIForZone}
          />
        )}

        {activePage === 'ai' && (
          <AIAssistant
            selectedZone={selectedZone}
          />
        )}
      </div>
    </div>
  )
}

export default App