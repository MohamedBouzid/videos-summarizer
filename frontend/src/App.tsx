import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

interface JobResult {
  summary: string;
  transcript: string;
  captions: string[];
}

interface JobStatus {
  status: string;
  message: string;
  result: JobResult | null;
}

function App() {
  const [youtubeUrl, setYoutubeUrl] = useState<string>('');
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [result, setResult] = useState<JobResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const pollingRef = useRef<NodeJS.Timeout | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setResult(null);
    setIsLoading(true);

    try {
      const response = await axios.post('/api/summarize', {
        youtube_url: youtubeUrl
      });
      console.log("Received summarize response: " + JSON.stringify(response.data));
      setJobId(response.data.job_id);
      setStatus(response.data.status);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to start video processing');
      setIsLoading(false);
    }
  };

  useEffect(() => {
    console.log("Polling for job status: " + jobId + ", current status: " + status);
    if (jobId && (status === 'queued' || status === 'processing')) {
      pollingRef.current = setInterval(async () => {
        try {
          const response = await axios.get(`/api/status/${jobId}`);
          setStatus(response.data.status);
          console.log("Job " + jobId + " status: " + response.data.status);
          if (response.data.status === 'completed') {
            setResult(response.data.result);
            setIsLoading(false);
            if (pollingRef.current) {
              clearInterval(pollingRef.current);
            }
          } else if (response.data.status === 'failed') {
            setError(response.data.message);
            setIsLoading(false);
            if (pollingRef.current) {
              clearInterval(pollingRef.current);
            }
          }
        } catch (err) {
          setError('Failed to get job status');
          setIsLoading(false);
          if (pollingRef.current) {
            clearInterval(pollingRef.current);
          }
        }
      }, 2000);
    }

    return () => {
      if (pollingRef.current) {
        clearInterval(pollingRef.current);
      }
    };
  }, [jobId, status]);

  const handleReset = () => {
    setYoutubeUrl('');
    setJobId(null);
    setStatus(null);
    setResult(null);
    setError(null);
    setIsLoading(false);
    if (pollingRef.current) {
      clearInterval(pollingRef.current);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Video Summarizer</h1>
        <p>Summarize YouTube videos using AI</p>
      </header>

      <main className="App-main">
        <form onSubmit={handleSubmit} className="summarize-form">
          <div className="input-group">
            <label htmlFor="youtube-url">YouTube Video URL</label>
            <input
              type="text"
              id="youtube-url"
              value={youtubeUrl}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setYoutubeUrl(e.target.value)}
              placeholder="https://www.youtube.com/watch?v=..."
              disabled={isLoading}
              required
            />
          </div>
          <button type="submit" disabled={isLoading || !youtubeUrl}>
            {isLoading ? 'Processing...' : 'Summarize Video'}
          </button>
        </form>

        {error && (
          <div className="error-message">
            <h3>Error</h3>
            <p>{error}</p>
            <button onClick={handleReset}>Try Again</button>
          </div>
        )}

        {status && status !== 'completed' && status !== 'failed' && (
          <div className="status-card">
            <h3>Processing Video</h3>
            <div className="status-indicator">
              <div className="spinner"></div>
              <p>{status === 'queued' ? 'Queued...' : 'Processing...'}</p>
            </div>
            <p className="status-message">{status}</p>
          </div>
        )}

        {result && (
          <div className="result-card">
            <h2>Video Summary</h2>
            <div className="summary-content">
              <p>{result.summary}</p>
            </div>

            <div className="details-section">
              <h3>Transcript</h3>
              <div className="transcript-content">
                <p>{result.transcript}</p>
              </div>
            </div>

            <div className="details-section">
              <h3>Frame Captions</h3>
              <div className="captions-content">
                
                  {result.captions}
                
              </div>
            </div>

            <button onClick={handleReset} className="reset-button">
              Summarize Another Video
            </button>
          </div>
        )}
      </main>

      <footer className="App-footer">
        <p>Powered by AI - Video Summarizer</p>
      </footer>
    </div>
  );
}

export default App;
