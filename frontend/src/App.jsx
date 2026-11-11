import Header from './components/Header'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'

function App() {
  return (
    <div className="app">

      <Header />

      <div className="main-layout">

        <Sidebar />

        <Dashboard />

      </div>

    </div>
  )
}

export default App