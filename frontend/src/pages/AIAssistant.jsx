import { useState } from 'react'

export default function AIAssistant ({ selectedZone }) {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)

  const handleAskAI = () => {
    if (!question.trim()) {
      return
    }

    setLoading(true)
    setAnswer('')

    setTimeout(() => {
      if (selectedZone) {
        setAnswer(
          `You are asking about ${selectedZone.zone}.

Risk Score: ${selectedZone.score}%
Risk Level: ${selectedZone.risk.toUpperCase()}
Disease Risk: ${selectedZone.disease}
Status: ${selectedZone.status}

Based on the current TerraSpectra analysis, ${selectedZone.zone} has a ${
            selectedZone.risk
          } disease-risk level. The zone should be monitored according to the current risk assessment.`
        )
      } else {
        setAnswer(
          `Based on the available TerraSpectra data, I can help you understand crop health, disease risk, and hyperspectral analysis.`
        )
      }

      setLoading(false)
    }, 800)
  }

  const handleKeyDown = event => {
    if (event.key === 'Enter') {
      handleAskAI()
    }
  }

  return (
    <main className='dashboard'>
      <div className='page-heading'>
        <div>
          <span className='page-label'>TERRASPECTRA AI</span>

          <h2>AI Crop Health Assistant</h2>

          <p>
            Ask questions about crop health, disease risk, and hyperspectral
            analysis.
          </p>
        </div>
      </div>

      <section className='ai-chat-container'>
        <div className='ai-welcome'>
          <div className='ai-large-icon'>🤖</div>

          <h3>Welcome to TerraSpectra AI</h3>

          <p>
            I can help you understand crop health and disease-risk information
            from the hyperspectral analysis.
          </p>
        </div>

        {selectedZone && (
          <div className='selected-zone-context'>
            <strong>📍 {selectedZone.zone} selected</strong>

            <span>
              Risk: {selectedZone.score}% • {selectedZone.risk.toUpperCase()}
            </span>
          </div>
        )}

        {answer && (
          <div className='ai-response'>
            <div className='ai-response-icon'>🤖</div>

            <div>
              <strong>TerraSpectra AI</strong>

              <p>{answer}</p>
            </div>
          </div>
        )}

        <div className='ai-input-area'>
          <input
            type='text'
            value={question}
            onChange={event => setQuestion(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={
              selectedZone
                ? `Ask about ${selectedZone.zone}...`
                : 'Ask about crop health or disease risk...'
            }
          />

          <button type='button' onClick={handleAskAI} disabled={loading}>
            {loading ? 'Analyzing...' : 'Ask AI →'}
          </button>
        </div>
      </section>
    </main>
  )
}
