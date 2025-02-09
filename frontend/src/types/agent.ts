export interface AgentResponse {
  name: string;
  functions: string[];
  wallet_address: string;
  wallet_id?: string;
  user_id: string;
}

export interface CreateAgentsResponse {
  success: boolean;
  message: string;
  agent_count: number;
  agents: AgentResponse[];
} 