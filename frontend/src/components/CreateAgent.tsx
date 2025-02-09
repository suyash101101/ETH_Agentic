import { useState } from 'react';
import { AgentResponse } from '../types/agent';

interface CreateAgentProps {
  userId: string;
  prompt: string;
  className?: string;
  style?: React.CSSProperties;
}

export const CreateAgent: React.FC<CreateAgentProps> = ({ 
  userId, 
  prompt,
  className,
  style 
}) => {
  const [agents, setAgents] = useState<AgentResponse[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleCreateAgents = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`http://localhost:8000/api/web3_manager/${userId}/create-agents`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });
      console.log(response)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Created Agents:', data);
      
      if (data.success) {
        setAgents(data.agents);
      } else {
        throw new Error(data.message);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred';
      console.error('Error creating agents:', errorMessage);
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={className} style={style}>
      <div style={{ marginBottom: '20px' }}>
        <button 
          onClick={handleCreateAgents}
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
          {loading ? 'Creating Agents...' : 'Create Agents'}
        </button>
      </div>

      {error && (
        <div style={{ color: 'red', marginBottom: '10px' }}>
          Error: {error}
        </div>
      )}

      {agents.length > 0 && (
        <div>
          <h3>Created Agents:</h3>
          {agents.map((agent, index) => (
            <div key={index} style={{ 
              marginBottom: '10px',
              padding: '10px',
              border: '1px solid #ddd',
              borderRadius: '4px'
            }}>
              <p><strong>Name:</strong> {agent.name}</p>
              <p><strong>Wallet Address:</strong> {agent.wallet_address}</p>
              <p><strong>Wallet ID:</strong> {agent.wallet_id}</p>
              <p><strong>Functions:</strong> {agent.functions.join(', ')}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CreateAgent; 