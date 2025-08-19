
import React, { useState } from 'react';

function MainView() {
  const [email, setEmail] = useState('');
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleEmailSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
  const res = await fetch(`http://127.0.0.1:5000/view_preferences?email=${encodeURIComponent(email)}`);
      const data = await res.json();
      setTopics(Array.isArray(data.topics) ? data.topics : []);
    } catch {
      setTopics([]);
    }
    setLoading(false);
  };

  return (
    <div className="App" style={{ background: '#f5f6fa', minHeight: '100vh' }}>
      <header className="App-header" style={{ padding: '2rem 0', textAlign: 'center', position: 'relative' }}>
        <h1 style={{ marginBottom: '2rem', textAlign: 'center', fontWeight: 700, fontSize: '2.5rem', letterSpacing: '0.05em' }}>Daily Digest Preferences</h1>
        <form onSubmit={handleEmailSubmit} style={{ marginBottom: '1rem', textAlign: 'center' }}>
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            placeholder="Enter your email to view subscriptions"
            required
            style={{ padding: '0.5rem', fontSize: '1rem', borderRadius: '4px', border: '1px solid #ccc', width: '320px', maxWidth: '90%' }}
          />
          <button type="submit" style={{ marginLeft: '0.5rem', padding: '0.5rem 1rem', fontSize: '1rem', borderRadius: '4px', background: '#1976d2', color: '#fff', border: 'none', cursor: 'pointer' }}>View</button>
        </form>
        {loading ? (
          <div style={{ textAlign: 'center', margin: '1rem 0' }}>Loading...</div>
        ) : (
          <ul style={{ listStyle: 'none', padding: 0, textAlign: 'center' }}>
            {topics.length === 0 ? (
              <li style={{ color: '#888' }}>No topics selected.</li>
            ) : (
              topics.map(topic => (
                <li key={topic} style={{ fontSize: '1.15rem', margin: '0.5rem 0', color: '#1976d2', fontWeight: 500 }}>
                  <span role="img" aria-label="checked">✅</span> {topic}
                </li>
              ))
            )}
          </ul>
        )}
      </header>
      <div style={{ textAlign: 'center', marginTop: '2rem' }}>
        <a
          href={email ? `/settings?email=${encodeURIComponent(email)}` : "/settings"}
          style={{ fontSize: '1.2rem', color: '#1976d2', textDecoration: 'underline', cursor: 'pointer' }}
        >Go to Settings</a>
      </div>
    </div>
  );
}

export default MainView;
