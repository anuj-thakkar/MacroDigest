
import React, { useState } from 'react';

const TOPICS = [
  { label: 'Sports', value: 'Sports' },
  { label: 'Entertainment / Pop Culture', value: 'Entertainment / Pop Culture' },
  { label: 'Politics', value: 'Politics' },
  { label: 'Economics', value: 'Economics' },
  { label: 'Technology', value: 'Technology' },
];

function PreferencesForm() {
  const [email, setEmail] = useState('');
  const [selectedTopics, setSelectedTopics] = useState([]);

  const handleTopicChange = (e) => {
    const value = e.target.value;
    setSelectedTopics(
      selectedTopics.includes(value)
        ? selectedTopics.filter((t) => t !== value)
        : [...selectedTopics, value]
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await fetch('http://127.0.0.1:5000/preferences', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, topics: selectedTopics }),
    });
    setEmail('');
    setSelectedTopics([]);
    alert('Preferences saved!');
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '40vh' }}>
      <form onSubmit={handleSubmit} style={{ margin: '2rem', maxWidth: 400, width: '100%', background: '#fff', padding: '2rem', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.08)' }}>
        <label style={{ display: 'block', marginBottom: '1rem', fontWeight: 'bold' }}>
          Email:
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{ display: 'block', marginTop: '0.5rem', padding: '0.5rem', fontSize: '1.1rem', width: '100%', borderRadius: '4px', border: '1px solid #ccc' }}
          />
        </label>
        <div style={{ margin: '1rem 0' }}>
          <span style={{ fontWeight: 'bold', marginBottom: '0.5rem', display: 'block' }}>Select topics:</span>
          {TOPICS.map((topic) => (
            <label key={topic.value} style={{ display: 'flex', alignItems: 'center', marginBottom: '0.75rem', fontSize: '1.15rem' }}>
              <input
                type="checkbox"
                value={topic.value}
                checked={selectedTopics.includes(topic.value)}
                onChange={handleTopicChange}
                style={{ width: '1.5em', height: '1.5em', marginRight: '0.75em' }}
              />
              {topic.label}
            </label>
          ))}
        </div>
        <button type="submit" style={{ padding: '0.7rem 1.5rem', fontSize: '1.1rem', borderRadius: '4px', background: '#1976d2', color: '#fff', border: 'none', cursor: 'pointer' }}>Save Preferences</button>
      </form>
    </div>
  );
}

function App() {
  return (
    <div className="App" style={{ background: '#f5f6fa', minHeight: '100vh' }}>
      <header className="App-header" style={{ padding: '2rem 0', textAlign: 'center' }}>
        <h1 style={{ marginBottom: '2rem', textAlign: 'center', fontWeight: 700, fontSize: '2.5rem', letterSpacing: '0.05em' }}>Daily Digest Preferences</h1>
        <PreferencesForm />
      </header>
    </div>
  );
}

export default App;
