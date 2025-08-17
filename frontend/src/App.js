
import React, { useState } from 'react';
import './App.css';

function App() {
  const [topic, setTopic] = useState('');
  const [digest, setDigest] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setDigest('');
    setError('');
    try {
      const response = await fetch('/digest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic })
      });
      const data = await response.json();
      setDigest(data.digest || 'No digest available.');
    } catch (err) {
      setError('Error fetching digest.');
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Daily Digest</h1>
        <form onSubmit={handleSubmit} className="digest-form">
          <label htmlFor="topic-select">Select a category</label>
          <select
            id="topic-select"
            value={topic}
            onChange={e => setTopic(e.target.value)}
            required
          >
            <option value="" disabled>Select a category</option>
            <option value="sports">Sports</option>
            <option value="entertainment">Entertainment / Pop Culture</option>
            <option value="politics">Politics</option>
            <option value="economics">Economics</option>
            <option value="technology">Technology</option>
          </select>
          <button type="submit" disabled={loading}>
            {loading ? 'Loading...' : 'Get Digest'}
          </button>
        </form>
        {digest && <div className="digest-box">{digest}</div>}
        {error && <div className="error">{error}</div>}
      </header>
    </div>
  );
}

export default App;
