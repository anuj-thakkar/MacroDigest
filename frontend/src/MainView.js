
import React, { useState } from 'react';

function MainView() {
  const [email, setEmail] = useState('');
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(false);

  const [userNotFound, setUserNotFound] = useState(false);
  const handleEmailSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setUserNotFound(false);
    try {
      const res = await fetch(`http://127.0.0.1:5000/view_preferences?email=${encodeURIComponent(email)}`);
      const data = await res.json();
      if (data.error) {
        setUserNotFound(true);
        setTopics([]);
      } else {
        setUserNotFound(false);
        setTopics(Array.isArray(data.topics) ? data.topics : []);
      }
    } catch {
      setUserNotFound(true);
      setTopics([]);
    }
    setLoading(false);
  };

  const [sending, setSending] = useState(false);
  const [sendResult, setSendResult] = useState(null);

  const handleSendDigest = async () => {
    setSending(true);
    setSendResult(null);
    try {
      const res = await fetch('http://127.0.0.1:5000/send_digest_now', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });
      const data = await res.json();
      if (res.ok) {
        setSendResult(data.message || 'Digest sent!');
      } else {
        setSendResult(data.error || 'Failed to send digest.');
      }
    } catch {
      setSendResult('Failed to send digest.');
    }
    setSending(false);
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
        ) : userNotFound ? (
          <div style={{ textAlign: 'center', margin: '1rem 0' }}>
            <div style={{ color: '#d32f2f', fontWeight: 500, marginBottom: '0.5rem' }}>No preferences found for this email.</div>
            <div style={{ color: '#555', marginBottom: '1rem' }}>Click below to create your preferences.</div>
            <a
              href={email ? `/settings?email=${encodeURIComponent(email)}` : "/settings"}
              style={{ fontSize: '1.1rem', color: '#1976d2', textDecoration: 'underline', cursor: 'pointer', fontWeight: 500 }}
            >Create Preferences</a>
          </div>
        ) : (
          <ul style={{ listStyle: 'none', padding: 0, textAlign: 'center' }}>
            {topics.map(topic => (
              <li key={topic} style={{ fontSize: '1.15rem', margin: '0.5rem 0', color: '#1976d2', fontWeight: 500 }}>
                <span role="img" aria-label="checked">✅</span> {topic}
              </li>
            ))}
          </ul>
        )}
        {topics.length > 0 && (
          <div style={{ marginTop: '2rem', textAlign: 'center' }}>
            <button
              onClick={handleSendDigest}
              disabled={sending}
              style={{ padding: '0.75rem 1.5rem', fontSize: '1.1rem', borderRadius: '4px', background: '#43a047', color: '#fff', border: 'none', cursor: 'pointer', marginBottom: '1rem' }}
            >
              {sending ? 'Sending...' : 'Send me my digest now!'}
            </button>
            {sendResult && (
              <div style={{ marginTop: '1rem', color: sendResult.includes('success') ? '#43a047' : '#d32f2f', fontWeight: 500 }}>
                {sendResult}
              </div>
            )}
          </div>
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
