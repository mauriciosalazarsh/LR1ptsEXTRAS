import { useState } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:5001/api'

function VisualizationTabs({ details }) {
  const [activeTab, setActiveTab] = useState('graphviz')
  const [graphvizSvg, setGraphvizSvg] = useState(null)
  const [parsingTable, setParsingTable] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const generateGraphviz = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.post(`${API_URL}/generate_graphviz`)
      if (response.data.success) {
        setGraphvizSvg(response.data.svg)
      } else {
        setError(response.data.error)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }


  const loadParsingTable = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.get(`${API_URL}/get_parsing_table`)
      if (response.data.success) {
        setParsingTable(response.data)
      } else {
        setError(response.data.error)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const renderParsingTable = () => {
    if (!parsingTable) {
      return (
        <div className="visualization-area">
          <p className="loading">Haz clic en "Cargar Tabla de Parsing" para visualizar la tabla ACTION/GOTO</p>
        </div>
      )
    }

    return (
      <div style={{ marginTop: '20px', overflowX: 'auto' }}>
        <table className="parsing-table">
          <thead>
            <tr>
              <th className="state-header" rowSpan={2}>Estado</th>
              <th className="action-header" colSpan={parsingTable.terminals.length}>ACTION</th>
              <th className="goto-header" colSpan={parsingTable.non_terminals.length}>GOTO</th>
            </tr>
            <tr>
              {parsingTable.terminals.map(t => (
                <th key={t} className="action-header">{t}</th>
              ))}
              {parsingTable.non_terminals.map(nt => (
                <th key={nt} className="goto-header">{nt}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {Array.from({ length: parsingTable.num_states }).map((_, i) => (
              <tr key={i}>
                <td className="state-header"><strong>I{i}</strong></td>
                {parsingTable.terminals.map(t => {
                  const action = parsingTable.action[i][t] || ''
                  let className = 'empty'
                  let content = action

                  if (action.startsWith('s')) className = 'shift'
                  else if (action.startsWith('r')) className = 'reduce'
                  else if (action === 'accept') {
                    className = 'accept'
                    content = 'ACC'
                  }

                  return <td key={t} className={className}>{content}</td>
                })}
                {parsingTable.non_terminals.map(nt => {
                  const goto = parsingTable.goto[i][nt] || ''
                  return <td key={nt} className={goto ? 'goto' : 'empty'}>{goto}</td>
                })}
              </tr>
            ))}
          </tbody>
        </table>

        <div style={{ marginTop: '20px', padding: '15px', background: '#f8f9fa', borderRadius: '8px' }}>
          <h4>Leyenda:</h4>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '10px', marginTop: '10px' }}>
            <div><strong style={{ color: '#155724' }}>sN</strong> = Shift (desplazar) al estado N</div>
            <div><strong style={{ color: '#856404' }}>rN</strong> = Reduce (reducir) con producción N</div>
            <div><strong style={{ color: '#0c5460' }}>ACC</strong> = Aceptar cadena</div>
            <div><strong style={{ color: '#084298' }}>N</strong> = GOTO estado N</div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="section">
      <h2>Visualizaciones</h2>

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'graphviz' ? 'active' : ''}`}
          onClick={() => setActiveTab('graphviz')}
        >
          Graphviz (Items LR(1))
        </button>
        <button
          className={`tab ${activeTab === 'table' ? 'active' : ''}`}
          onClick={() => setActiveTab('table')}
        >
          Tabla ACTION/GOTO
        </button>
        <button
          className={`tab ${activeTab === 'details' ? 'active' : ''}`}
          onClick={() => setActiveTab('details')}
        >
          Detalles
        </button>
      </div>

      {activeTab === 'graphviz' && (
        <div className="tab-content active">
          <button className="btn btn-success" onClick={generateGraphviz} disabled={loading}>
            {loading ? 'Generando...' : 'Generar con Graphviz'}
          </button>
          {error && <div className="alert alert-error">{error}</div>}
          <div className="visualization-area">
            {graphvizSvg ? (
              <div dangerouslySetInnerHTML={{ __html: graphvizSvg }} />
            ) : (
              <p className="loading">Haz clic en "Generar con Graphviz" para visualizar el autómata</p>
            )}
          </div>
        </div>
      )}

      {activeTab === 'table' && (
        <div className="tab-content active">
          <button className="btn btn-success" onClick={loadParsingTable} disabled={loading}>
            {loading ? 'Cargando...' : 'Cargar Tabla de Parsing'}
          </button>
          {error && <div className="alert alert-error">{error}</div>}
          {renderParsingTable()}
        </div>
      )}

      {activeTab === 'details' && details && (
        <div className="tab-content active">
          <h3>Producciones</h3>
          <div className="production-list">
            {details.productions.map(p => (
              <div key={p.number} className="production-item">
                {p.number}: {p.text}
              </div>
            ))}
          </div>

          <h3 style={{ marginTop: '20px' }}>Conjuntos FIRST</h3>
          <div className="sets-display">
            {Object.entries(details.first_sets).map(([nt, set]) => (
              <div key={nt} className="set-item">
                FIRST({nt}) = {'{'}{set.join(', ')}{'}'}
              </div>
            ))}
          </div>

          <h3 style={{ marginTop: '20px' }}>Conjuntos FOLLOW</h3>
          <div className="sets-display">
            {Object.entries(details.follow_sets).map(([nt, set]) => (
              <div key={nt} className="set-item">
                FOLLOW({nt}) = {'{'}{set.join(', ')}{'}'}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default VisualizationTabs
