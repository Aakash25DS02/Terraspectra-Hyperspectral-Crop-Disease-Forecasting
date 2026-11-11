export default function Header() {
  return (
    <header className="header">
      <div className="logo">
        <span className="logo-icon">🌱</span>

        <div>
          <h1>TerraSpectra</h1>
          <p>Hyperspectral Crop Disease Forecasting</p>
        </div>
      </div>

      <div className="header-status">
        <span className="status-dot"></span>
        <span>System Online</span>
      </div>
    </header>
  )
}