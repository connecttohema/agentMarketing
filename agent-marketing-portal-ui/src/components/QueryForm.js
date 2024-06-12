import React, { useState } from 'react';
import './QueryForm.css'; // Add CSS file for styles

function QueryForm({ onQuery }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    onQuery(query);
  };

  return (
    <form className="query-form" onSubmit={handleSubmit}>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Type your query here..."
        className="query-input"
      />
      <button type="submit" className="query-button">Submit</button>
    </form>
  );
}

export default QueryForm;
