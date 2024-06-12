import React, { useState } from 'react';
import axios from 'axios';
import QueryForm from './components/QueryForm';
import QueryResults from './components/QueryResults';
import './App.css'; // Add CSS file for styles
import statefarmLogo from './statefarm-logo.png'; // Ensure the logo file is in the src directory
import agentMarketing from './agentMarketing.png'; // Ensure the image file is in the src directory

function App() {
  const [results, setResults] = useState([]);
  const [selectedCustomers, setSelectedCustomers] = useState([]);
  const [showPdf, setShowPdf] = useState(false); // State to show/hide PDF

  const handleQuery = async (query) => {
    console.log("Sending query:", query);  // Debugging log
    try {
      const response = await axios.post('http://127.0.0.1:5000/query', {
        prompt: query
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      console.log("Response data:", response.data);  // Debugging log
      setResults(response.data.results);
    } catch (error) {
      console.error('Error fetching query results', error);
    }
  };

  const handleCustomerSelect = (customerId) => {
    setSelectedCustomers((prevSelected) =>
      prevSelected.includes(customerId)
        ? prevSelected.filter((id) => id !== customerId)
        : [...prevSelected, customerId]
    );
  };

  const handleSendLetter = async () => {
    console.log("Selected customer IDs:", selectedCustomers);  // Debugging log
    try {
      const response = await axios.post('http://127.0.0.1:5000/create_letter', {
        customer_id: selectedCustomers,  // Make sure this matches your backend expectation
        prompt_type: 'marketing'  // Adjust as necessary
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      console.log("Response data:", response.data);  // Debugging log
      alert('Marketing letter generated successfully!');
      setShowPdf(true);  // Show the PDF
    } catch (error) {
      console.error('Error generating marketing letter', error);
      alert('Failed to generate marketing letter.');
    }
  };

  return (
    <div className="app">
      <header className="header">
        <img src={statefarmLogo} alt="State Farm Logo" className="header-logo" />
        <div className="header-content">
          <h1>Agent Marketing Portal</h1>
          <p className="catchy-verb">Maximize Your Reach with Personalized Campaigns</p>
        </div>
      </header>
      <img src={agentMarketing} alt="Agent Marketing" className="side-image" />
      <QueryForm onQuery={handleQuery} />
      {results.length > 0 && (
        <QueryResults results={results} onCustomerSelect={handleCustomerSelect} />
      )}
      {selectedCustomers.length > 0 && (
        <button className="send-letter-button" onClick={handleSendLetter}>Send Marketing Letter</button>
      )}
      {showPdf && (
        <div className="pdf-display">
          <h2>Generated Marketing Letter</h2>
          <iframe src="/hardcoded_marketing_letter.pdf" width="100%" height="600px" title="Marketing Letter"></iframe>
        </div>
      )}
    </div>
  );
}

export default App;
