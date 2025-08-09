
import { useState } from 'react';
import './App.css';
import { testData } from '../testdata';
import { useNavigate } from 'react-router-dom';


function SearchPage() {
  const [postcode, setPostcode] = useState('');
  const [suburb, setSuburb] = useState('');
  const [street, setStreet] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);
  const navigate = useNavigate();

  /*const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);
    const queryURL = 'http://localhost:5000?suburb_name' + encodeURIComponent(suburb) + '&postcode=' + encodeURIComponent(postcode) + '&street_name=' + encodeURIComponent(street); 
    try {
      const response = await fetch(queryURL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
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
  };*/

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);
    try {
      await new Promise(res => setTimeout(res, 500));
      setResult(testData);
      navigate('/results', { state: { data: testData } });
    } catch (err: any) {
      setError('Failed to load test data');
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
          <label htmlFor="suburb">Suburb name</label>
          <input
            id="suburb"
            type="text"
            placeholder="Enter suburb name"
            value={suburb}
            onChange={e => setSuburb(e.target.value)}
            autoComplete="suburb-name"
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

export default SearchPage;
