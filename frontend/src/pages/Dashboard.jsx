import StatCard from '../components/StatCard'

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
    title: 'High Risk',
    value: '100 acres',
    description: 'Requires attention',
    icon: '⚠️'
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

      <section className="dashboard-placeholder">
        <div>
          <span className="placeholder-icon">
            🗺️
          </span>

          <h3>Farm Risk Map</h3>

          <p>
            Interactive hyperspectral disease-risk map
            will be integrated here.
          </p>
        </div>
      </section>

    </main>
  )
}