import { groth16 } from 'snarkjs';

const API_BASE_URL = 'http://localhost:8000'; // Update with your backend URL

export const generateAndVerifyProof = async (circuitName, inputs) => {
  try {
    console.log("Inputs received:", inputs);
    const formattedInputs = Object.fromEntries(
      Object.entries(inputs).map(([key, value]) => [key, value.toString()])
    );

    // Use API endpoints
    console.log("Circuit name:", circuitName);
    console.log("Formatted inputs:", formattedInputs);
    console.log("API base URL:", API_BASE_URL);

    const wasmPath = `${API_BASE_URL}/zkproof/circuit/${circuitName}/wasm`;
    const zkeyPath = `${API_BASE_URL}/zkproof/circuit/${circuitName}/zkey`;
    const vkeyPath = `${API_BASE_URL}/zkproof/circuit/${circuitName}/vkey`;

    // Generate and verify proof
    try {
      const { proof, publicSignals } = await groth16.fullProve(
        formattedInputs,
        wasmPath,
        zkeyPath
      );

      const vkeyResponse = await fetch(vkeyPath);
      const vkey = await vkeyResponse.json();
      const isValid = await groth16.verify(vkey, publicSignals, proof);

      return {
        proof: JSON.stringify(proof),
        publicSignals,
        isValid
      };
    } catch (error) {
      // Handle specific assertion errors from the circuit
      if (error.message.includes('Assert Failed')) {
        return {
          proof: null,
          publicSignals: null,
          isValid: false,
          error: 'Proof generation failed: The inputs do not satisfy the circuit constraints'
        };
      }
      throw error;
    }
  } catch (error) {
    console.error(`ZKP Error for ${circuitName}:`, error);
    throw new Error(error.message || 'Failed to generate or verify proof');
  }
};