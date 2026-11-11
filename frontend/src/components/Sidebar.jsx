export default function Sidebar() {
  return (
    <aside className="sidebar">
      <nav>
        <button className="nav-item active">
          <span>📊</span>
          <span>Dashboard</span>
        </button>

        <button className="nav-item">
          <span>🗺️</span>
          <span>Risk Analysis</span>
        </button>

        <button className="nav-item">
          <span>📈</span>
          <span>Historical Analysis</span>
        </button>

        <button className="nav-item">
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