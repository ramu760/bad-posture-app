import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [video, setVideo] = useState(null);
  const [postureType, setPostureType] = useState('squat');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleVideoChange = (e) => {
    setVideo(e.target.files[0]);
  };

  const handlePostureChange = (e) => {
    setPostureType(e.target.value);
  };

  const handleUpload = async () => {
    if (!video) {
      alert('Please select a video file first!');
      return;
    }

    const formData = new FormData();
    formData.append('video', video);
    formData.append('posture_type', postureType);

    try {
      setLoading(true);
      const response = await axios.post('http://127.0.0.1:5000/analyze', formData);
      setResult(response.data);
    } catch (error) {
      alert('Error analyzing video!');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>🧍‍♂️ Bad Posture Detection App</h2>

      <label>Choose Posture Type:</label>
      <select value={postureType} onChange={handlePostureChange}>
        <option value="squat">Squat</option>
        <option value="desk">Desk Sitting</option>
      </select>

      <br /><br />

      <input type="file" accept="video/*" onChange={handleVideoChange} />
      <br /><br />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? 'Analyzing...' : 'Upload & Analyze'}
      </button>

      <br /><br />
      {result && (
        <div style={{ backgroundColor: '#f0f0f0', padding: '10px' }}>
          <h3>📊 Result:</h3>
          <p><strong>Posture Type:</strong> {result.posture_type}</p>
          <p><strong>Total Frames:</strong> {result.total_frames}</p>
          <p><strong>Bad Posture Frames:</strong> {result.bad_posture_frames}</p>
          <p><strong>Bad Posture %:</strong> {result.bad_posture_percent}%</p>
        </div>
      )}
    </div>
  );
}

export default App;