import { useState, useEffect } from 'react';
import ZKProofGenerator from '../components/ZKProofGenerator';
import type { InputSchema } from '../utils/generateproof';

function MultiplicationCheckDemo() {
  const [schema, setSchema] = useState<InputSchema | null>(null);
  const [circuitName, setCircuitName] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCircuitSchema = async () => {
      try {
        // TODO: Replace with actual API call
        // const response = await fetch('http://localhost:8000/api/circuit/something/schema');
        // const data = await response.json();
        // setSchema(data.schema);

        // Temporary hardcoded schema for demonstration
        setSchema({
          a: { type: 'number', label: 'Value A', description: 'First number to multiply' },
          b: { type: 'number', label: 'Value B', description: 'Second number to multiply' },
          c: { type: 'number', label: 'Expected Product', description: 'Should equal A * B' },
          d: { type: 'number', label: 'Expected Sum', description: 'Should equal A + B' }
        });
        setCircuitName('multiply');

      } catch (err) {
        setError('Failed to load circuit schema');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchCircuitSchema();
  }, []);

  if (loading) return <div>Loading circuit schema...</div>;
  if (error) return <div className="text-red-500">{error}</div>;
  if (!schema || !circuitName) return <div>No schema or circuit name available</div>;

  return (
    <div className="container mx-auto py-8">
      <ZKProofGenerator
        circuitName={circuitName}
        schema={schema}
        title="Multiplication Check ZK Proof"
        description="Generate a zero-knowledge proof that you know two numbers that multiply to a given result"
      />
    </div>
  );
}

export default MultiplicationCheckDemo;

