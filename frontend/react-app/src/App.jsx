import { useState } from 'react'
import './App.css'
import GrammarEditor from './components/GrammarEditor'
import AutomatonInfo from './components/AutomatonInfo'
import VisualizationTabs from './components/VisualizationTabs'
import StringParser from './components/StringParser'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001/api'

function App() {
  const [parserBuilt, setParserBuilt] = useState(false)
  const [automatonInfo, setAutomatonInfo] = useState(null)
  const [parserDetails, setParserDetails] = useState(null)
  const [parserType, setParserType] = useState('LR1')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const buildParser = async (grammar, selectedParserType) => {
    setLoading(true)
    setError(null)

    try {
      const response = await axios.post(`${API_URL}/build_parser`, {
        grammar,
        parser_type: selectedParserType
      })

      if (response.data.success) {
        setAutomatonInfo(response.data.info)
        setParserDetails({
          first_sets: response.data.first_sets,
          follow_sets: response.data.follow_sets,
          productions: response.data.productions
        })
        setParserType(response.data.parser_type || selectedParserType)
        setParserBuilt(true)
      } else {
        setError(response.data.error)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        <header className="app-header">
          <h1>Visualizador de Autómata {parserBuilt ? parserType : 'LR(1) / LALR(1)'}</h1>
          <p>Compiladores - UTEC - Puntos Extras Examen 2</p>
        </header>

        <main className="app-main">
          <GrammarEditor onBuild={buildParser} loading={loading} error={error} />

          {parserBuilt && (
            <>
              <AutomatonInfo info={automatonInfo} />
              <VisualizationTabs details={parserDetails} />
              <StringParser />
            </>
          )}
        </main>
      </div>
    </div>
  )
}

export default App
