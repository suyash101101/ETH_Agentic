from .converter_agent import Web3Converter
from .onchain_agent import OnChainAgents, load_agent, ask_agent
from typing import List, Optional

class Web3AgentManager:
    def __init__(self):
        self.web3_converter = Web3Converter()
        self.agents: List[OnChainAgents] = []
        self._instance_id = id(self)
        print(f"Initialized Web3AgentManager with ID: {self._instance_id}")
        
    def create_agents(self, prompt: str) -> List[OnChainAgents]:
        """Create agents based on the prompt"""
        try:
            print(f"Creating agents with manager {self._instance_id}")
            self.web3_converter.run(prompt)
            agent_counter = 1
            
            # Get the functions from the converter response
            # functions = self.web3_converter.functions
            functions = self.web3_converter.functions
            print(f"\nAvailable functions for manager {self._instance_id}:", functions)
            
            # Clear existing agents
            self.agents = []
            
            for func_list in functions:
                try:
                    # Handle both single function and multiple functions
                    if isinstance(func_list, list):
                        agent_name = f"agent{agent_counter}"
                        
                        if len(func_list) == 1:
                            # Single function case
                            print(f"\nCreating {agent_name} with function: {func_list[0]}")
                            agent = load_agent(functions=func_list)
                            wallet_address = agent._get_wallet_address()
                            agent.function_names = [func_list[0]]
                        else:
                            # Multiple functions case
                            function_names = [f for f in func_list]
                            print(f"\nCreating {agent_name} with functions: {function_names}")
                            agent = load_agent(functions=func_list)
                            wallet_address = agent._get_wallet_address()
                            agent.function_names = function_names
                        
                        print(f"{agent_name} created successfully with wallet address: {wallet_address}")
                        agent_counter += 1
                        self.agents.append(agent)
                            
                except Exception as e:
                    print(f"Error creating agent: {str(e)}")
                    continue
            
            print(f"\nManager {self._instance_id} created {len(self.agents)} agents")
            return self.agents
            
        except Exception as e:
            print(f"Error in create_agents: {str(e)}")
            raise
    
    def run_agent(self, wallet_id: str, agent_index: int, prompt: str) -> str:
        """Run a specific agent with the given prompt"""
        if 0 <= agent_index < len(self.agents):
            print(f"Running agent {agent_index} with prompt: {prompt}")
            print(f"Agent functions: {self.agents[agent_index].function_names}")
            
            return ask_agent(self.agents[agent_index], prompt)
        raise IndexError("Agent index out of range")
    
    def get_agents(self) -> List[OnChainAgents]:
        """Get all created agents"""
        return self.agents