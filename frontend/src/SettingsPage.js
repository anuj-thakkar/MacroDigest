
import React, { useState, useEffect } from 'react';

const TOPICS = [
  { label: 'Market Volatility & Options', value: 'Market Volatility & Options' },
  { label: 'Equities and Indexes', value: 'Equities and Indexes' },
  { label: 'Macroeconomics', value: 'Macroeconomics' },
  { label: 'Regulatory & Compliance News', value: 'Regulatory & Compliance News' },
  { label: 'Alternative Assets & Innovation', value: 'Alternative Assets & Innovation' },
];

function SettingsPage() {
  const [email, setEmail] = useState('');
  // Auto-populate email from query param
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const emailParam = params.get('email');
    if (emailParam) setEmail(emailParam);
  }, []);
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [saveDisabled, setSaveDisabled] = useState(true);
  const [successMsg, setSuccessMsg] = useState('');

  const handleEmailSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccessMsg('');
    try {
      const res = await fetch(`http://127.0.0.1:5000/view_preferences?email=${encodeURIComponent(email)}`);
      const data = await res.json();
      setTopics(Array.isArray(data.topics) ? data.topics : []);
      setSaveDisabled(true); // Disable Save after loading
    } catch {
      setTopics([]);
      setError('Could not load preferences.');
    }
    setLoading(false);
  };

  const handleTopicToggle = (topic) => {
    setTopics((prev) => {
      const newTopics = prev.includes(topic)
        ? prev.filter((t) => t !== topic)
        : [...prev, topic];
      setSaveDisabled(false); // Enable Save when topics change
      setSuccessMsg(''); // Clear success message on change
      return newTopics;
    });
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    setSuccessMsg('');
    try {
      const res = await fetch('http://127.0.0.1:5000/preferences', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, topics }),
      });
      if (!res.ok) throw new Error('Save failed');
      setSuccessMsg('Preferences saved successfully!');
      setSaveDisabled(true); // Disable Save after saving
    } catch {
      setError('Could not save preferences.');
    }
    setSaving(false);
  };

  return (
    <div className="App" style={{ background: '#f5f6fa', minHeight: '100vh' }}>
      <header className="App-header" style={{ padding: '2rem 0', textAlign: 'center', position: 'relative' }}>
        <h1 style={{ marginBottom: '2rem', textAlign: 'center', fontWeight: 700, fontSize: '2.5rem', letterSpacing: '0.05em' }}>Edit Preferences</h1>
        <form onSubmit={handleEmailSubmit} style={{ marginBottom: '1rem', textAlign: 'center' }}>
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            placeholder="Enter your email"
            required
            style={{ padding: '0.5rem', fontSize: '1rem', borderRadius: '4px', border: '1px solid #ccc', width: '320px', maxWidth: '90%' }}
          />
          <button type="submit" style={{ marginLeft: '0.5rem', padding: '0.5rem 1rem', fontSize: '1rem', borderRadius: '4px', background: '#1976d2', color: '#fff', border: 'none', cursor: 'pointer' }}>Load</button>
        </form>
        {loading ? (
          <div style={{ textAlign: 'center', margin: '1rem 0' }}>Loading...</div>
        ) : null}
        <form onSubmit={handleSave} style={{ marginBottom: '1rem', textAlign: 'center' }}>
          <div style={{ margin: '1rem 0 2.5rem 0', textAlign: 'left', display: 'inline-block' }}>
            {TOPICS.map(topic => (
              <label key={topic.value} style={{ display: 'block', fontSize: '1.15rem', margin: '0.5rem 0', cursor: 'pointer' }}>
                <input
                  type="checkbox"
                  checked={topics.includes(topic.value)}
                  onChange={() => handleTopicToggle(topic.value)}
                  style={{ width: 22, height: 22, marginRight: 10 }}
                />
                {topic.label}
              </label>
            ))}
          </div>
          <div style={{ height: '1rem' }}></div>
            <button type="submit" disabled={saving || saveDisabled} style={{ marginTop: '0.5rem', padding: '0.5rem 1rem', fontSize: '1rem', borderRadius: '4px', background: saveDisabled ? '#bdbdbd' : '#1976d2', color: '#fff', border: 'none', cursor: saveDisabled ? 'not-allowed' : 'pointer' }}>Save</button>
        </form>
        {successMsg && <div style={{ color: '#43a047', textAlign: 'center', marginBottom: '1rem', fontWeight: 500 }}>{successMsg}</div>}
        {error && <div style={{ color: 'red', textAlign: 'center', marginBottom: '1rem' }}>{error}</div>}
        <div style={{ textAlign: 'center', marginTop: '2rem' }}>
          <a href="/" style={{ fontSize: '1.2rem', color: '#1976d2', textDecoration: 'underline', cursor: 'pointer' }}>Back to Main</a>
        </div>
      </header>
    </div>
  );
}

export default SettingsPage;
