function AutomatonInfo({ info }) {
  if (!info) return null

  return (
    <div className="section">
      <h2>Información del Autómata</h2>
      <div className="info-grid">
        <div className="info-card">
          <h3>Estados</h3>
          <p>{info.num_states}</p>
        </div>
        <div className="info-card">
          <h3>Transiciones</h3>
          <p>{info.num_transitions}</p>
        </div>
        <div className="info-card">
          <h3>Terminales</h3>
          <p>{info.terminals.length}</p>
        </div>
        <div className="info-card">
          <h3>No Terminales</h3>
          <p>{info.non_terminals.length}</p>
        </div>
      </div>
    </div>
  )
}

export default AutomatonInfo
