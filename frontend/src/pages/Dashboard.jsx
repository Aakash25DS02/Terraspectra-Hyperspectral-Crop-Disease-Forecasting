import StatCard from '../components/StatCard'
import RiskOverview from '../components/RiskOverview'
import AIInsight from '../components/AIInsight'
import FarmRiskMap from '../map/FarmRiskMap'

const farmStats = [
  {
    title: 'Total Farm Area',
    value: '1,000 acres',
    description: 'Monitored area',
    icon: '🌾'
  },
  {
    title: 'Healthy Area',
    value: '720 acres',
    description: '72% of total area',
    icon: '🌱'
  },
  {
    title: 'Moderate Risk',
    value: '50 acres',
    description: 'Requires monitoring',
    icon: '🟡'
  },
  {
    title: 'High Risk',
    value: '100 acres',
    description: 'Requires attention',
    icon: '🔴'
  },
  {
    title: 'Critical Zones',
    value: '8',
    description: 'High priority areas',
    icon: '🚨'
  }
]

export default function Dashboard() {
  return (
    <main className="dashboard">

      <div className="page-heading">
        <div>
          <span className="page-label">
            TERRASPECTRA MONITORING
          </span>

          <h2>Farm Health Dashboard</h2>

          <p>
            Monitor crop health using hyperspectral analysis
          </p>
        </div>

        <div className="date-info">
          <span>Last Updated</span>
          <strong>Today</strong>
        </div>
      </div>

      <section className="stats-grid">
        {farmStats.map((stat) => (
          <StatCard
            key={stat.title}
            title={stat.title}
            value={stat.value}
            description={stat.description}
            icon={stat.icon}
          />
        ))}
      </section>

      <section className="map-section">
        <div className="section-heading">
          <div>
            <h3>Farm Risk Map</h3>
            <p>
              Spatial visualization of crop disease risk
            </p>
          </div>

          <button className="map-control">
            🗺️ View Full Map
          </button>
        </div>

        <FarmRiskMap />
      </section>

      <RiskOverview />

      <AIInsight />

    </main>
  )
}