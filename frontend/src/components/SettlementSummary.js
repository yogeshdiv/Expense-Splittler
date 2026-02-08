function SettlementSummary({ settlement }) {
  return (
    <div className="card">
      <h2>Settlement Summary</h2>
      <div>
        {settlement.length === 0 ? (
          <div className="empty-state">
            {settlement.length === 0
              ? "Everyone is settled up! "
              : 'Add expenses to see settlement details'}
          </div>
        ) : (
          settlement.map((item, index) => (
            <div key={index} className="settlement-item">
              <div className="settlement-text">
                <span className="settlement-name">{item.from_person}</span>{' '}
                owes{' '}
                <span className="settlement-name">{item.to_person}</span>{' '}
                <span className="settlement-amount">
                  Rs {parseFloat(item.amount.toFixed(2)).toString()}
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default SettlementSummary;
