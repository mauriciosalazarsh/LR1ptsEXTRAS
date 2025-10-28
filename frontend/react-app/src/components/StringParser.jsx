import { useState } from 'react'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001/api'

function StringParser() {
  const [inputString, setInputString] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleParse = async () => {
    setLoading(true)
    try {
      const response = await axios.post(`${API_URL}/parse_string`, {
        string: inputString
      })

      if (response.data.success) {
        setResult(response.data)
      }
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="section">
      <h2>Análisis de Cadenas</h2>
      <div className="input-test">
        <input
          type="text"
          value={inputString}
          onChange={(e) => setInputString(e.target.value)}
          placeholder="Ingrese cadena a analizar (ej: q * a * a * b)"
          onKeyPress={(e) => e.key === 'Enter' && !loading && inputString && handleParse()}
        />
        <button
          className="btn btn-success"
          onClick={handleParse}
          disabled={loading || !inputString}
        >
          {loading ? 'Analizando...' : 'Analizar'}
        </button>
      </div>

      {result && (
        <div style={{ marginTop: '20px' }}>
          <div className={`alert ${result.accepted ? 'alert-success' : 'alert-error'}`}>
            {result.accepted ? (
              <>
                <strong>Cadena ACEPTADA:</strong> "{inputString}"
              </>
            ) : (
              <>
                <strong>Cadena RECHAZADA:</strong> "{inputString}"
                <br /><br />
                <strong>Error:</strong> {result.error}
              </>
            )}
          </div>

          {result.trace && result.trace.length > 0 && (
            <div>
              <h3>Traza de Análisis</h3>
              <table className="trace-table">
                <thead>
                  <tr>
                    <th>Paso</th>
                    <th>Pila</th>
                    <th>Entrada</th>
                    <th>Acción</th>
                  </tr>
                </thead>
                <tbody>
                  {result.trace.map((step, i) => (
                    <tr key={i}>
                      <td>{i + 1}</td>
                      <td>{step.stack || ''}</td>
                      <td>{step.input || ''}</td>
                      <td>{step.action || ''}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default StringParser
