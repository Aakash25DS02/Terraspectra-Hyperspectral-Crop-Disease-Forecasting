export default function Sidebar({
  activePage,
  setActivePage
}) {
  return (
    <aside className="sidebar">
      <nav>

        <button
          className={`nav-item ${
            activePage === 'dashboard' ? 'active' : ''
          }`}
          onClick={() => setActivePage('dashboard')}
        >
          <span>📊</span>
          <span>Dashboard</span>
        </button>

        <button
          className="nav-item"
          onClick={() => setActivePage('risk')}
        >
          <span>🗺️</span>
          <span>Risk Analysis</span>
        </button>

        <button
          className="nav-item"
          onClick={() => setActivePage('history')}
        >
          <span>📈</span>
          <span>Historical Analysis</span>
        </button>

        <button
          className={`nav-item ${
            activePage === 'ai' ? 'active' : ''
          }`}
          onClick={() => setActivePage('ai')}
        >
          <span>🤖</span>
          <span>AI Assistant</span>
        </button>

      </nav>

      <div className="sidebar-bottom">
        <p>TerraSpectra</p>
        <small>AI-Powered Agriculture</small>
      </div>
    </aside>
  )
}