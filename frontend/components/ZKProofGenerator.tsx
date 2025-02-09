import React, { useState } from 'react';
import { generateAndVerifyProof } from '../utils/generateproof';
import type { InputSchema, ProofResult } from '../utils/generateproof';

interface ZKProofGeneratorProps {
  circuitName: string;
  schema: InputSchema;
  title?: string;
  description?: string;
}

const ZKProofGenerator: React.FC<ZKProofGeneratorProps> = ({
  circuitName,
  schema,
  title,
  description
}) => {
  // Initialize inputs based on schema
  const initialInputs = Object.entries(schema).reduce((acc, [key, def]) => ({
    ...acc,
    [key]: def.type === 'number' ? 0 : def.type === 'boolean' ? false : ''
  }), {});

  const [inputs, setInputs] = useState<Record<string, any>>(initialInputs);
  const [proofResult, setProofResult] = useState<ProofResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (name: string, value: string) => {
    const inputType = schema[name].type;
    let processedValue: any = value;

    switch (inputType) {
      case 'number':
        processedValue = value === '' ? 0 : Number(value);
        break;
      case 'boolean':
        processedValue = Boolean(value);
        break;
      default:
        processedValue = value;
    }

    setInputs(prev => ({
      ...prev,
      [name]: processedValue
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const result = await generateAndVerifyProof(circuitName, inputs);
      console.log("Result:", result);
      setProofResult(result);
      if (result.error) {
        setError(result.error);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate proof');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-lg">
      {title && <h2 className="text-2xl font-bold mb-2">{title}</h2>}
      {description && <p className="text-gray-600 mb-4">{description}</p>}
      
      <form onSubmit={handleSubmit} className="space-y-4">
        {Object.entries(schema).map(([name, definition]) => (
          <div key={name}>
            <label className="block text-sm font-medium text-gray-700">
              {definition.label || name}:
              {definition.description && (
                <span className="text-xs text-gray-500 ml-1">
                  ({definition.description})
                </span>
              )}
              <input
                type={definition.type === 'number' ? 'number' : 'text'}
                name={name}
                value={inputs[name]}
                onChange={(e) => handleInputChange(name, e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                required
              />
            </label>
          </div>
        ))}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 disabled:bg-gray-400"
        >
          {loading ? 'Generating Proof...' : 'Generate Proof'}
        </button>
      </form>

      {error && (
        <div className="mt-4 p-3 bg-red-100 text-red-700 rounded-md">
          {error}
        </div>
      )}

      {proofResult && error && (
        <div className="mt-4 p-4 bg-gray-50 rounded-md">
          <h3 className="font-bold text-lg mb-2">Proof Result</h3>
          <p className="text-green-600 font-semibold">
            Proof is {proofResult.isValid ? 'Valid' : 'Invalid'}
          </p>
          <details className="mt-2">
            <summary className="cursor-pointer text-sm text-gray-600">
              View Proof Details
            </summary>
            <pre className="mt-2 text-xs overflow-auto max-h-40 bg-gray-100 p-2 rounded">
              {JSON.stringify(proofResult, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
};

export default ZKProofGenerator; 