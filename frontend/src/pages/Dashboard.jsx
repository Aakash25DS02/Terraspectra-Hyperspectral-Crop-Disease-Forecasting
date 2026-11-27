import { useRef } from 'react'
import StatCard from '../components/StatCard'
import RiskOverview from '../components/RiskOverview'
import AIInsight from '../components/AIInsight'
import FarmRiskMap from '../map/FarmRiskMap'
import RiskAnalytics from '../components/RiskAnalytics'
import { farmZones } from '../data/farmData'

const totalArea = farmZones.reduce((total, zone) => total + zone.area, 0)

const healthyArea = farmZones
  .filter(zone => zone.risk === 'healthy')
  .reduce((total, zone) => total + zone.area, 0)

const moderateArea = farmZones
  .filter(zone => zone.risk === 'moderate')
  .reduce((total, zone) => total + zone.area, 0)

const highRiskArea = farmZones
  .filter(zone => zone.risk === 'high')
  .reduce((total, zone) => total + zone.area, 0)

const criticalZones = farmZones.filter(zone => zone.score >= 80).length

const healthyPercentage = Math.round((healthyArea / totalArea) * 100)

const farmStats = [
  {
    title: 'Total Farm Area',
    value: `${totalArea.toLocaleString()} acres`,
    description: 'Monitored area',
    icon: '🌾'
  },
  {
    title: 'Healthy Area',
    value: `${healthyArea} acres`,
    description: `${healthyPercentage}% of total area`,
    icon: '🌱'
  },
  {
    title: 'Moderate Risk',
    value: `${moderateArea} acres`,
    description: 'Requires monitoring',
    icon: '🟡'
  },
  {
    title: 'High Risk',
    value: `${highRiskArea} acres`,
    description: 'Requires attention',
    icon: '🔴'
  },
  {
    title: 'Critical Zones',
    value: `${criticalZones}`,
    description: 'High priority areas',
    icon: '🚨'
  }
]

export default function Dashboard ({
  onAskAI,
  onRiskSelect,
  onZoneSelect,
  mapRiskFilter,
  mapSelectedZone
}) {
  const mapSectionRef = useRef(null)
  return (
    <main className='dashboard'>
      <div className='page-heading'>
        <div>
          <span className='page-label'>TERRASPECTRA MONITORING</span>

          <h2>Farm Health Dashboard</h2>

          <p>Monitor crop health using hyperspectral analysis</p>
        </div>

        <div className='date-info'>
          <span>Last Updated</span>
          <strong>Today</strong>
        </div>
      </div>

      <section className='stats-grid'>
        {farmStats.map(stat => (
          <StatCard
            key={stat.title}
            title={stat.title}
            value={stat.value}
            description={stat.description}
            icon={stat.icon}
          />
        ))}
      </section>

      <section className='map-section' ref={mapSectionRef}>
        <div className='section-heading'>
          <div>
            <h3>Farm Risk Map</h3>
            <p>Spatial visualization of crop disease risk</p>
          </div>

          <button
            className='map-control'
            onClick={() => mapSectionRef.current?.requestFullscreen()}
          >
            🗺️ View Full Map
          </button>
        </div>

        <FarmRiskMap
          onAskAI={onAskAI}
          externalRiskFilter={mapRiskFilter}
          externalSelectedZone={mapSelectedZone}
        />
      </section>

      <RiskOverview />

      <RiskAnalytics onRiskSelect={onRiskSelect} onZoneSelect={onZoneSelect} />

      <AIInsight />
    </main>
  )
}
