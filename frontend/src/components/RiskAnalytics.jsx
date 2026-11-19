import { farmZones } from '../data/farmData'

const totalZones = farmZones.length

const healthyZones = farmZones.filter(
  zone => zone.risk === 'healthy'
).length

const moderateZones = farmZones.filter(
  zone => zone.risk === 'moderate'
).length

const highZones = farmZones.filter(
  zone => zone.risk === 'high'
).length

const riskData = [
  {
    label: 'Healthy',
    value: healthyZones,
    percentage: Math.round((healthyZones / totalZones) * 100),
    icon: '🌱'
  },
  {
    label: 'Moderate',
    value: moderateZones,
    percentage: Math.round((moderateZones / totalZones) * 100),
    icon: '🟡'
  },
  {
    label: 'High',
    value: highZones,
    percentage: Math.round((highZones / totalZones) * 100),
    icon: '🔴'
  }
]

const zoneScores = farmZones.map(zone => ({
  zone: zone.zone,
  score: zone.score,
  risk:
    zone.risk === 'healthy'
      ? 'Healthy'
      : zone.risk === 'moderate'
        ? 'Moderate'
        : 'High'
}))

export default function RiskAnalytics ({ onRiskSelect, onZoneSelect }) {
  return (
    <section className='analytics-section'>
      <div className='section-heading'>
        <div>
          <h3>Farm Risk Analytics</h3>
          <p>Overview of disease-risk distribution across monitored zones</p>
        </div>
      </div>

      <div className='analytics-grid'>
        <div className='analytics-card'>
          <h4>Risk Distribution</h4>

          <div className='risk-bars'>
            {riskData.map(item => (
              <div
                className='risk-bar-item clickable'
                key={item.label}
                onClick={() => onRiskSelect(item.label.toLowerCase())}
              >
                <div className='risk-bar-label'>
                  <span>
                    {item.icon} {item.label}
                  </span>

                  <strong>{item.value} zones</strong>
                </div>

                <div className='analytics-progress'>
                  <div
                    className={`analytics-progress-fill ${item.label.toLowerCase()}`}
                    style={{
                      width: `${item.percentage}%`
                    }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className='analytics-card'>
          <h4>Zone Risk Scores</h4>

          <div className='zone-score-list'>
            {zoneScores.map(zone => (
              <div
                className='zone-score-item clickable'
                key={zone.zone}
                onClick={() => onZoneSelect(zone.zone)}
              >
                <div>
                  <strong>{zone.zone}</strong>
                  <span>{zone.risk}</span>
                </div>

                <div className='score-value'>{zone.score}%</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className='monitoring-summary'>
        <div className='monitoring-icon'>🧠</div>

        <div>
          <span>AI MONITORING SUMMARY</span>

          <h4>
            {highZones} high-risk zone{highZones !== 1 ? 's' : ''} requires
            immediate attention
          </h4>

          <p>
            {farmZones.find(zone => zone.risk === 'high')?.zone} currently has
            the highest disease-risk score at{' '}
            {Math.max(...farmZones.map(zone => zone.score))}%.{' '}
            {healthyZones} zones are healthy, while {moderateZones} zone
            {moderateZones !== 1 ? 's' : ''} require continued monitoring.
          </p>
        </div>
      </div>
    </section>
  )
}