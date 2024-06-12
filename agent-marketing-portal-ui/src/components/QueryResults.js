import React from 'react';
import './QueryResults.css'; // Add CSS file for styles

function QueryResults({ results, onCustomerSelect }) {
  if (results.length === 0) {
    return <p>No results found</p>;
  }

  const headers = Object.keys(results[0]);

  return (
    <div className="query-results">
      <h2>Potential Insurance Customers List</h2>
      <table>
        <thead>
          <tr>
            <th>Select</th>
            {headers.map((header) => (
              <th key={header}>{header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {results.map((customer) => (
            <tr key={customer.CustomerId}>
              <td>
                <input
                  type="checkbox"
                  onChange={() => onCustomerSelect(customer.CustomerId)}
                />
              </td>
              {headers.map((header) => (
                <td key={header}>{customer[header]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default QueryResults;
