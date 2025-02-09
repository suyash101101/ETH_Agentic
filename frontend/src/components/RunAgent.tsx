import { useState } from 'react';

interface RunAgentProps {
  userId: string;
  agentIndex: number;
  walletId: string;
  functions: string[];
  className?: string;
  style?: React.CSSProperties;
}

interface RunAgentResponse {
  success: boolean;
  result: string;
}

export const RunAgent: React.FC<RunAgentProps> = ({
  userId,
  agentIndex,
  walletId,
  functions,
  className,
  style
}) => {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleRunAgent = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`http://localhost:8000/api/web3_manager/${userId}/run-agent`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          agent_index: agentIndex,
          prompt: prompt,
          wallet_id: walletId,
          functions: functions
        }),
      });

      console.log('Run Agent Response:', response);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: RunAgentResponse = await response.json();
      console.log('Run Agent Result:', data);

      if (data.success) {
        setResponse(data.result);
      } else {
        throw new Error('Failed to get response from agent');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred';
      console.error('Error running agent:', errorMessage);
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={className} style={style}>
      <div style={{ marginBottom: '20px' }}>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter your prompt for the agent..."
          style={{
            width: '100%',
            minHeight: '100px',
            padding: '10px',
            marginBottom: '10px',
            borderRadius: '4px',
            border: '1px solid #ddd'
          }}
        />
        <button
          onClick={handleRunAgent}
          disabled={loading}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            cursor: loading ? 'not-allowed' : 'pointer',
            backgroundColor: loading ? '#cccccc' : '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
          }}
        >
          {loading ? 'Running Agent...' : 'Run Agent'}
        </button>
      </div>

      {error && (
        <div style={{ color: 'red', marginBottom: '10px' }}>
          Error: {error}
        </div>
      )}

      {response && (
        <div style={{
          padding: '15px',
          backgroundColor: '#f5f5f5',
          borderRadius: '4px',
          marginTop: '20px'
        }}>
          <h4>Agent Response:</h4>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
};

export default RunAgent; 