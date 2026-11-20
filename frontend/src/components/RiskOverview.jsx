import { farmZones } from '../data/farmData'

const totalArea = farmZones.reduce(
  (total, zone) => total + zone.area,
  0
)

const riskLevels = [
  {
    label: 'Healthy',
    risk: 'healthy',
    icon: '🌱'
  },
  {
    label: 'Moderate Risk',
    risk: 'moderate',
    icon: '🟡'
  },
  {
    label: 'High Risk',
    risk: 'high',
    icon: '🔴'
  }
]

export default function RiskOverview () {
  return (
    <section className='risk-overview'>
      <div className='section-heading'>
        <div>
          <h3>Disease Risk Overview</h3>
          <p>Current crop health distribution across the farm</p>
        </div>
      </div>

      <div className='risk-grid'>
        {riskLevels.map(riskLevel => {
          const zones = farmZones.filter(
            zone => zone.risk === riskLevel.risk
          )

          const area = zones.reduce(
            (total, zone) => total + zone.area,
            0
          )

          const percentage = Math.round(
            (area / totalArea) * 100
          )

          return (
            <div
              className='risk-item'
              key={riskLevel.risk}
            >
              <div className='risk-item-top'>
                <span className='risk-icon'>
                  {riskLevel.icon}
                </span>

                <div>
                  <h4>{riskLevel.label}</h4>
                  <span>{area} acres</span>
                </div>

                <strong>{percentage}%</strong>
              </div>

              <div className='risk-progress'>
                <div
                  className='risk-progress-fill'
                  style={{
                    width: `${percentage}%`
                  }}
                ></div>
              </div>
            </div>
          )
        })}
      </div>
    </section>
  )
}