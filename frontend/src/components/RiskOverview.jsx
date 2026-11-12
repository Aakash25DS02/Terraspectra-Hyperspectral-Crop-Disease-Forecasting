const riskLevels = [
  {
    label: 'Healthy',
    value: 72,
    area: '720 acres',
    icon: '🌱'
  },
  {
    label: 'Low Risk',
    value: 13,
    area: '130 acres',
    icon: '🟢'
  },
  {
    label: 'Medium Risk',
    value: 5,
    area: '50 acres',
    icon: '🟡'
  },
  {
    label: 'High Risk',
    value: 10,
    area: '100 acres',
    icon: '🔴'
  }
]

export default function RiskOverview() {
  return (
    <section className="risk-overview">
      <div className="section-heading">
        <div>
          <h3>Disease Risk Overview</h3>
          <p>Current crop health distribution across the farm</p>
        </div>
      </div>

      <div className="risk-grid">
        {riskLevels.map((risk) => (
          <div className="risk-item" key={risk.label}>
            <div className="risk-item-top">
              <span className="risk-icon">{risk.icon}</span>

              <div>
                <h4>{risk.label}</h4>
                <span>{risk.area}</span>
              </div>

              <strong>{risk.value}%</strong>
            </div>

            <div className="risk-progress">
              <div
                className="risk-progress-fill"
                style={{ width: `${risk.value}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}