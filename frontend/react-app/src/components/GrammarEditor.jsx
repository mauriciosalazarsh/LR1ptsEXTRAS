import { useState } from 'react'

const DEFAULT_GRAMMAR = `S -> q * A * B * C
A -> a
A -> b * b * D
B -> a
B -> ε
C -> b
C -> ε
D -> C
D -> ε`

function GrammarEditor({ onBuild, loading, error }) {
  const [grammar, setGrammar] = useState(DEFAULT_GRAMMAR)
  const [parserType, setParserType] = useState('LR1')

  const handleBuild = () => {
    onBuild(grammar, parserType)
  }

  const handleLoadExample = () => {
    setGrammar(DEFAULT_GRAMMAR)
  }

  return (
    <div className="section">
      <h2>Gramática</h2>
      <textarea
        className="grammar-input"
        value={grammar}
        onChange={(e) => setGrammar(e.target.value)}
        placeholder="Ingrese la gramática..."
        rows={10}
      />

      <div className="parser-type-selector">
        <label htmlFor="parser-type">Tipo de Parser:</label>
        <select
          id="parser-type"
          value={parserType}
          onChange={(e) => setParserType(e.target.value)}
          className="parser-select"
        >
          <option value="LR1">LR(1)</option>
          <option value="LALR1">LALR(1)</option>
        </select>
      </div>

      <div className="button-group">
        <button
          className="btn btn-primary"
          onClick={handleBuild}
          disabled={loading}
        >
          {loading ? 'Construyendo...' : `Construir Parser ${parserType === 'LR1' ? 'LR(1)' : 'LALR(1)'}`}
        </button>
        <button
          className="btn btn-info"
          onClick={handleLoadExample}
        >
          Cargar Ejemplo
        </button>
      </div>
      {error && (
        <div className="alert alert-error">
          Error: {error}
        </div>
      )}
    </div>
  )
}

export default GrammarEditor
