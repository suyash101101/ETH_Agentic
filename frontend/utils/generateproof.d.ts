export interface InputSchema {
  [key: string]: {
    type: 'number' | 'text' | 'boolean';
    label?: string;
    description?: string;
  }
}

export interface ProofResult {
  proof: string | null;
  publicSignals: string[] | null;
  isValid: boolean;
  error?: string;
}

export function generateAndVerifyProof(
  circuitName: string, 
  inputs: Record<string, any>
): Promise<ProofResult>; 