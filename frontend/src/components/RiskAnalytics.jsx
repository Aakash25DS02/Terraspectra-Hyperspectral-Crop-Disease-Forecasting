const riskData = [
  {
    label: 'Healthy',
    value: 2,
    percentage: 50,
    icon: '🌱'
  },
  {
    label: 'Moderate',
    value: 1,
    percentage: 25,
    icon: '🟡'
  },
  {
    label: 'High',
    value: 1,
    percentage: 25,
    icon: '🔴'
  }
]

const zoneScores = [
  { zone: 'Zone A', score: 18, risk: 'Healthy' },
  { zone: 'Zone B', score: 52, risk: 'Moderate' },
  { zone: 'Zone C', score: 87, risk: 'High' },
  { zone: 'Zone D', score: 22, risk: 'Healthy' }
]

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

          <h4>1 high-risk zone requires immediate attention</h4>

          <p>
            Zone C currently has the highest disease-risk score at 87%. Two
            zones are healthy, while one zone requires continued monitoring.
          </p>
        </div>
      </div>
    </section>
  )
}
