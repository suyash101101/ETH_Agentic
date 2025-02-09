from dotenv import load_dotenv
from cdp import *
import os
import json
from phi.model.google import Gemini
from phi.agent import Agent, RunResponse
from cdp.errors import UnsupportedAssetError
from typing import Optional, List, Union
from decimal import Decimal

load_dotenv()

# # Function to get the balance of a specific asset
# def get_balance(asset_id):
#     """
#     Get the balance of a specific asset in the agent's wallet.
    
#     Args:
#         asset_id (str): Asset identifier ("eth", "usdc") or contract address of an ERC-20 token
    
#     Returns:
#         str: A message showing the current balance of the specified asset
#     """
#     balance = agent_wallet.balance(asset_id)
#     return f"Current balance of {asset_id}: {balance}"


def configure_cdp():
    try:
        API_KEY_NAME = os.environ.get("CDP_API_KEY_NAME")
        PRIVATE_KEY = os.environ.get("CDP_PRIVATE_KEY", "")
        
        if not API_KEY_NAME or not PRIVATE_KEY:
            raise ValueError("CDP credentials not found in environment variables")
            
        # Clean up private key - remove any extra quotes and properly handle newlines
        PRIVATE_KEY = PRIVATE_KEY.strip('"').replace('\\n', '\n')
        
        print("Configuring CDP with:")
        print(f"API Key Name: {API_KEY_NAME}")
        print(f"Private Key Length: {len(PRIVATE_KEY)}")
        
        Cdp.configure(API_KEY_NAME, PRIVATE_KEY)
        return True
    except Exception as e:
        print(f"Error configuring CDP: {str(e)}")
        return False

cdp_configured = configure_cdp()    

class OnChainAgents:
    def __init__(self, wallet_id: Optional[str] = None):
        """
        Initialize an OnChainAgent with optional wallet_id.
        If wallet_id is provided, loads existing wallet, else creates new one.
        
        Args:
            wallet_id: Optional ID of existing wallet to load
        """
        if not cdp_configured:
            raise ValueError("CDP configuration failed. Check your credentials.")
        
        self.WalletStorage = "wallet_storage"
        os.makedirs(self.WalletStorage, exist_ok=True)
        
        # Initialize wallet
        self.wallet_id = wallet_id
        self.wallet = self._initialize_wallet(wallet_id)
        
        # Save wallet data after initialization
        if self.wallet:
            wallet_data = self.wallet.export_data()
            self._save_wallet(wallet_data)
    
    def _initialize_wallet(self, wallet_id: Optional[str] = None) -> Wallet:
        """Initialize wallet based on wallet_id or create new one"""
        if wallet_id:
            # Try to load existing wallet
            wallet_data = self._load_wallet(wallet_id)
            if wallet_data:
                try:
                    data = WalletData(
                        wallet_id=wallet_data['wallet_id'],
                        seed=wallet_data['seed']
                    )
                    wallet = Wallet.import_data(data)
                    print(f"Loaded existing wallet: {wallet_id}")
                    return wallet
                except Exception as e:
                    print(f"Error importing wallet data: {str(e)}")
        
        # Create new wallet if no wallet_id or wallet not found
        try:
            wallet = Wallet.create()
            wallet_data = wallet.export_data()
            self.wallet_id = wallet_data.wallet_id
            print(f"Created new wallet: {self.wallet_id}")
            return wallet
        except Exception as e:
            print(f"Error creating new wallet: {str(e)}")
            raise

    def _load_wallet(self, wallet_id: str) -> Optional[dict]:
        """Load wallet data from storage"""
        file_path = os.path.join(self.WalletStorage, f"{wallet_id}.json")
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    print(f"Loaded wallet data for {wallet_id}")
                    return data
            else:
                print(f"No wallet data found for ID: {wallet_id}")
        except Exception as e:
            print(f"Error loading wallet data: {str(e)}")
        return None

    def _save_wallet(self, wallet_data: WalletData):
        """Save wallet data and update registry"""
        try:
            # Save wallet data
            file_path = os.path.join(self.WalletStorage, f"{wallet_data.wallet_id}.json")
            with open(file_path, 'w') as file:
                json.dump(wallet_data.to_dict(), file)
            
            # Save encrypted seed
            seed_file = os.path.join(self.WalletStorage, f"{wallet_data.wallet_id}_seed.json")
            self.wallet.save_seed(seed_file, encrypt=True)
            
            # Update registry
            self._update_wallet_registry(wallet_data.wallet_id)
            print(f"Wallet {wallet_data.wallet_id} saved successfully")
            
        except Exception as e:
            print(f"Error saving wallet data: {str(e)}")
            raise

    def _update_wallet_registry(self, wallet_id: str):
        """Update the registry of wallet IDs"""
        registry_file = os.path.join(self.WalletStorage, "wallet_registry.txt")
        try:
            existing_ids = set()
            if os.path.exists(registry_file):
                with open(registry_file, 'r') as file:
                    existing_ids = set(file.read().splitlines())
            
            if wallet_id not in existing_ids:
                with open(registry_file, 'a') as file:
                    file.write(f"{wallet_id}\n")
                print(f"Added {wallet_id} to registry")
        except Exception as e:
            print(f"Error updating registry: {str(e)}")

def load_agent(wallet_id: Optional[str] = None, functions: Optional[List[str]] = None) -> OnChainAgents:
    """
    Load or create an OnChainAgent and equip it with specified functions.
    
    Args:
        wallet_id: Optional ID of existing wallet to load
        functions: List of function names to equip the agent with
    
    Returns:
        OnChainAgents: Initialized agent with specified functions
    """
    try:
        # Create/load the agent
        agent = OnChainAgents(wallet_id=wallet_id)

        def get_balance(asset_id) -> str:
            """
            Get the balance of a specific asset in the agent's wallet.
            
            Parameters:
            asset_id (str): Asset identifier ("eth", "usdc") or contract address of an ERC-20 token
            
            Returns:
            str: A message showing the current balance of the specified asset.
            """
            balance = agent.wallet.balance(asset_id)
            return f"Current balance of {asset_id}: {balance}"
        
        # Define available tools
        available_tools = {
            'get_balance': get_balance,
            # Add other tools as needed
        }
        
        # Get the requested functions
        if functions:
            tool_list = []
            for func_name in functions:
                if func_name in available_tools:
                    tool_list.append(available_tools[func_name])
                else:
                    print(f"Warning: Function {func_name} not found")
            
            # Create the agent with the tools
            agent.function_names = functions
            agent.agent = Agent(
                model=Gemini(
                    model="gemini-2.0-flash-exp",
                    api_key=os.environ.get("GEMINI_API_KEY")
                ),
                tools=tool_list
            )
            print(f"Agent equipped with functions: {functions}")
        
        return agent
        
    except Exception as e:
        print(f"Error loading agent: {str(e)}")
        raise

def ask_agent(agent: OnChainAgents, prompt: str) -> str:
    """
    Run an agent with a prompt
    
    Args:
        agent: The OnChainAgent to run
        prompt: The prompt to run the agent with
    
    Returns:
        str: The agent's response
    """
    try:
        if not hasattr(agent, 'agent'):
            raise ValueError("Agent not initialized with functions")
        response: RunResponse = agent.agent.run(prompt)
        return response.content
    except Exception as e:
        return f"Error running agent: {str(e)}"
    
# agent = load_agent(functions=["get_balance"])
# print(run_agent(agent, "What is the balance of eth in my wallet?"))