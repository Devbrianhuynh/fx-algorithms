import React from 'react'

// Not available
function Progress({ title, summary }) {
  const getStyle = (summary) => {
      if (summary.includes('sell')) {
        return { color: 'red' };
      } else if (summary.includes('buy')) {
        return { color: 'green' };
      } else {
        return { color: 'grey' };
      }
    };

  return (
    <div className="progress-wrap">

        <div className="progress-text">{title}</div>
        <div style={getStyle(summary)}>{summary}</div>
    </div>
  )
}

export default Progress