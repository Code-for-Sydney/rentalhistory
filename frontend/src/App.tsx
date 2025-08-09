
import { useState } from 'react';
import './App.css';


function App() {
  const [postcode, setPostcode] = useState('');
  const [street, setStreet] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const response = await fetch('http://localhost:5000/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ postcode, street })
      });
      if (!response.ok) {
        throw new Error('Server error');
      }
      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modern-container">
      <h1>Rental History Search</h1>
      <form className="search-form" onSubmit={handleSearch}>
        <div className="form-group">
          <label htmlFor="postcode">Postcode</label>
          <input
            id="postcode"
            type="text"
            placeholder="Enter postcode"
            value={postcode}
            onChange={e => setPostcode(e.target.value)}
            autoComplete="postal-code"
          />
        </div>
        <div className="form-group">
          <label htmlFor="street">Street Address</label>
          <input
            id="street"
            type="text"
            placeholder="Enter street address"
            value={street}
            onChange={e => setStreet(e.target.value)}
            autoComplete="street-address"
          />
        </div>
        <button type="submit" className="search-btn" disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>
      {error && <div style={{ color: 'red', marginTop: '1rem' }}>{error}</div>}
      {result && (
        <div style={{ marginTop: '1.5rem', background: '#f1f5f9', padding: '1rem', borderRadius: '0.5rem' }}>
          <pre style={{ margin: 0 }}>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
