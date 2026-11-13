import { useState } from 'react'

export default function AIAssistant() {
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
      setAnswer(
        `Based on the available TerraSpectra data, ${question}. The selected zone currently shows elevated disease risk and should be monitored closely.`
      )

      setLoading(false)
    }, 800)
  }

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleAskAI()
    }
  }

  return (
    <main className="dashboard">

      <div className="page-heading">
        <div>
          <span className="page-label">
            TERRASPECTRA AI
          </span>

          <h2>AI Crop Health Assistant</h2>

          <p>
            Ask questions about crop health, disease risk, and
            hyperspectral analysis.
          </p>
        </div>
      </div>

      <section className="ai-chat-container">

        <div className="ai-welcome">

          <div className="ai-large-icon">
            🤖
          </div>

          <h3>
            Welcome to TerraSpectra AI
          </h3>

          <p>
            I can help you understand crop health and disease-risk
            information from the hyperspectral analysis.
          </p>

        </div>

        {answer && (
          <div className="ai-response">
            <div className="ai-response-icon">
              🤖
            </div>

            <div>
              <strong>TerraSpectra AI</strong>

              <p>{answer}</p>
            </div>
          </div>
        )}

        <div className="ai-input-area">

          <input
            type="text"
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            onKeyDown={handleKeyDown}
            placeholder="Ask about crop health or disease risk..."
          />

          <button
            type="button"
            onClick={handleAskAI}
            disabled={loading}
          >
            {loading ? 'Analyzing...' : 'Ask AI →'}
          </button>

        </div>

      </section>

    </main>
  )
}