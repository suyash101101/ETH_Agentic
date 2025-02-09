from phi.model.google import Gemini
from phi.agent import Agent, RunResponse
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import os
from typing import List, Union
from cdp import *
from cdp.errors import UnsupportedAssetError
from decimal import Decimal
from web3 import Web3


load_dotenv()

class Function(BaseModel):

    task: str = Field(..., description="The task that needs to be done.")
    flow: str = Field(..., description="How the functions will be used to accomplish the task.")
    function: List[str] = Field(..., description="The functions needed to accomplish the task.")


class Functions(BaseModel):
    functions: List[Function] = Field(..., description="The functions that should be added to the web3 application.")

# Function to create a new ERC-20 token
def create_token(name, symbol, initial_supply):
    """
    Create a new ERC-20 token.
    
    Args:
        name (str): The name of the token
        symbol (str): The symbol of the token
        initial_supply (int): The initial supply of tokens
    
    Returns:
        str: A message confirming the token creation with details
    """
    deployed_contract = agent_wallet.deploy_token(name, symbol, initial_supply)
    deployed_contract.wait()
    return f"Token {name} ({symbol}) created with initial supply of {initial_supply} and contract address {deployed_contract.contract_address}"


# Function to transfer assets
def transfer_asset(amount, asset_id, destination_address):
    """
    Transfer an asset to a specific address.
    
    Args:
        amount (Union[int, float, Decimal]): Amount to transfer
        asset_id (str): Asset identifier ("eth", "usdc") or contract address of an ERC-20 token
        destination_address (str): Recipient's address
    
    Returns:
        str: A message confirming the transfer or describing an error
    """
    try:
        # Check if we're on Base Mainnet and the asset is USDC for gasless transfer
        is_mainnet = agent_wallet.network_id == "base-mainnet"
        is_usdc = asset_id.lower() == "usdc"
        gasless = is_mainnet and is_usdc

        # For ETH and USDC, we can transfer directly without checking balance
        if asset_id.lower() in ["eth", "usdc"]:
            transfer = agent_wallet.transfer(amount,
                                             asset_id,
                                             destination_address,
                                             gasless=gasless)
            transfer.wait()
            gasless_msg = " (gasless)" if gasless else ""
            return f"Transferred {amount} {asset_id}{gasless_msg} to {destination_address}"

        # For other assets, check balance first
        try:
            balance = agent_wallet.balance(asset_id)
        except UnsupportedAssetError:
            return f"Error: The asset {asset_id} is not supported on this network. It may have been recently deployed. Please try again in about 30 minutes."

        if balance < amount:
            return f"Insufficient balance. You have {balance} {asset_id}, but tried to transfer {amount}."

        transfer = agent_wallet.transfer(amount, asset_id, destination_address)
        transfer.wait()
        return f"Transferred {amount} {asset_id} to {destination_address}"
    except Exception as e:
        return f"Error transferring asset: {str(e)}. If this is a custom token, it may have been recently deployed. Please try again in about 30 minutes, as it needs to be indexed by CDP first."


# Function to get the balance of a specific asset
def get_balance(asset_id):
    """
    Get the balance of a specific asset in the agent's wallet.
    
    Args:
        asset_id (str): Asset identifier ("eth", "usdc") or contract address of an ERC-20 token
    
    Returns:
        str: A message showing the current balance of the specified asset
    """
    balance = agent_wallet.balance(asset_id)
    return f"Current balance of {asset_id}: {balance}"


# Function to request ETH from the faucet (testnet only)
def request_eth_from_faucet():
    """
    Request ETH from the Base Sepolia testnet faucet.
    
    Returns:
        str: Status message about the faucet request
    """
    if agent_wallet.network_id == "base-mainnet":
        return "Error: The faucet is only available on Base Sepolia testnet."

    faucet_tx = agent_wallet.faucet()
    return f"Requested ETH from faucet. Transaction: {faucet_tx}"


# Function to generate art using DALL-E (requires separate OpenAI API key)
def generate_art(prompt):
    """
    Generate art using DALL-E based on a text prompt.
    
    Args:
        prompt (str): Text description of the desired artwork
    
    Returns:
        str: Status message about the art generation, including the image URL if successful
    """
    try:
        client = OpenAI()
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        return f"Generated artwork available at: {image_url}"

    except Exception as e:
        return f"Error generating artwork: {str(e)}"


# Function to deploy an ERC-721 NFT contract
def deploy_nft(name, symbol, base_uri):
    """
    Deploy an ERC-721 NFT contract.
    
    Args:
        name (str): Name of the NFT collection
        symbol (str): Symbol of the NFT collection
        base_uri (str): Base URI for token metadata
    
    Returns:
        str: Status message about the NFT deployment, including the contract address
    """
    try:
        deployed_nft = agent_wallet.deploy_nft(name, symbol, base_uri)
        deployed_nft.wait()
        contract_address = deployed_nft.contract_address

        return f"Successfully deployed NFT contract '{name}' ({symbol}) at address {contract_address} with base URI: {base_uri}"

    except Exception as e:
        return f"Error deploying NFT contract: {str(e)}"


# Function to mint an NFT
def mint_nft(contract_address, mint_to):
    """
    Mint an NFT to a specified address.
    
    Args:
        contract_address (str): Address of the NFT contract
        mint_to (str): Address to mint NFT to
    
    Returns:
        str: Status message about the NFT minting
    """
    try:
        mint_args = {"to": mint_to, "quantity": "1"}

        mint_invocation = agent_wallet.invoke_contract(
            contract_address=contract_address, method="mint", args=mint_args)
        mint_invocation.wait()

        return f"Successfully minted NFT to {mint_to}"

    except Exception as e:
        return f"Error minting NFT: {str(e)}"


# Function to swap assets (only works on Base Mainnet)
def swap_assets(amount: Union[int, float, Decimal], from_asset_id: str,
                to_asset_id: str):
    """
    Swap one asset for another using the trade function.
    This function only works on Base Mainnet.

    Args:
        amount (Union[int, float, Decimal]): Amount of the source asset to swap
        from_asset_id (str): Source asset identifier
        to_asset_id (str): Destination asset identifier

    Returns:
        str: Status message about the swap
    """
    if agent_wallet.network_id != "base-mainnet":
        return "Error: Asset swaps are only available on Base Mainnet. Current network is not Base Mainnet."

    try:
        trade = agent_wallet.trade(amount, from_asset_id, to_asset_id)
        trade.wait()
        return f"Successfully swapped {amount} {from_asset_id} for {to_asset_id}"
    except Exception as e:
        return f"Error swapping assets: {str(e)}"


# Contract addresses for Basenames
BASENAMES_REGISTRAR_CONTROLLER_ADDRESS_MAINNET = "0x4cCb0BB02FCABA27e82a56646E81d8c5bC4119a5"
BASENAMES_REGISTRAR_CONTROLLER_ADDRESS_TESTNET = "0x49aE3cC2e3AA768B1e5654f5D3C6002144A59581"
L2_RESOLVER_ADDRESS_MAINNET = "0xC6d566A56A1aFf6508b41f6c90ff131615583BCD"
L2_RESOLVER_ADDRESS_TESTNET = "0x6533C94869D28fAA8dF77cc63f9e2b2D6Cf77eBA"


# Function to create registration arguments for Basenames
def create_register_contract_method_args(base_name: str, address_id: str,
                                         is_mainnet: bool) -> dict:
    """
    Create registration arguments for Basenames.
    
    Args:
        base_name (str): The Basename (e.g., "example.base.eth" or "example.basetest.eth")
        address_id (str): The Ethereum address
        is_mainnet (bool): True if on mainnet, False if on testnet
    
    Returns:
        dict: Formatted arguments for the register contract method
    """
    w3 = Web3()

    resolver_contract = w3.eth.contract(abi=l2_resolver_abi)

    name_hash = w3.ens.namehash(base_name)

    address_data = resolver_contract.encode_abi("setAddr",
                                                args=[name_hash, address_id])

    name_data = resolver_contract.encode_abi("setName",
                                             args=[name_hash, base_name])

    register_args = {
        "request": [
            base_name.replace(".base.eth" if is_mainnet else ".basetest.eth",
                              ""),
            address_id,
            "31557600",  # 1 year in seconds
            L2_RESOLVER_ADDRESS_MAINNET
            if is_mainnet else L2_RESOLVER_ADDRESS_TESTNET,
            [address_data, name_data],
            True
        ]
    }

    return register_args


# Function to register a basename
def register_basename(basename: str, amount: float = 0.002):
    """
    Register a basename for the agent's wallet.
    
    Args:
        basename (str): The basename to register (e.g. "myname.base.eth" or "myname.basetest.eth")
        amount (float): Amount of ETH to pay for registration (default 0.002)
    
    Returns:
        str: Status message about the basename registration
    """
    address_id = agent_wallet.default_address.address_id
    is_mainnet = agent_wallet.network_id == "base-mainnet"

    suffix = ".base.eth" if is_mainnet else ".basetest.eth"
    if not basename.endswith(suffix):
        basename += suffix

    register_args = create_register_contract_method_args(
        basename, address_id, is_mainnet)

    try:
        contract_address = (BASENAMES_REGISTRAR_CONTROLLER_ADDRESS_MAINNET
                            if is_mainnet else
                            BASENAMES_REGISTRAR_CONTROLLER_ADDRESS_TESTNET)

        invocation = agent_wallet.invoke_contract(
            contract_address=contract_address,
            method="register",
            args=register_args,
            abi=registrar_abi,
            amount=amount,
            asset_id="eth",
        )
        invocation.wait()
        return f"Successfully registered basename {basename} for address {address_id}"
    except ContractLogicError as e:
        return f"Error registering basename: {str(e)}"
    except Exception as e:
        return f"Unexpected error registering basename: {str(e)}"

class Web3Converter:
    def __init__(self):
        self.functions = {
            # "create_token": "Create a new ERC-20 token with a specified name, symbol, and initial supply.",
            # "transfer_asset": "Transfer an asset to a specific address, checking balances and handling gasless transfers.",
            "get_balance": "Get the balance of a specific asset in the agent's wallet."
            # "request_eth_from_faucet": "Request ETH from the Base Sepolia testnet faucet.",
            # "generate_art": "Generate art using DALL-E based on a text prompt.",
            # "deploy_nft": "Deploy an ERC-721 NFT contract with a specified name, symbol, and base URI.",
            # "mint_nft": "Mint an NFT to a specified address from a given contract.",
            # "swap_assets": "Swap one asset for another using the trade function, available only on Base Mainnet.",
            # "create_register_contract_method_args": "Create registration arguments for Basenames.",
            # "register_basename": "Register a basename for the agent's wallet."
        }
        self.toolkit = {
            "create_token": create_token,
            "transfer_asset": transfer_asset,
            "get_balance": get_balance,
            "request_eth_from_faucet": request_eth_from_faucet,
            "generate_art": generate_art,
            "deploy_nft": deploy_nft,
            "mint_nft": mint_nft,
            "swap_assets": swap_assets,
            "create_register_contract_method_args": create_register_contract_method_args,
            "register_basename": register_basename
        }
        self.converter = Agent(
            model=Gemini(model='gemini-2.0-flash-exp', api_key=os.getenv("GEMINI_API_KEY")),
            description=(
                "You are a highly skilled web3 developer with expertise in transitioning web2 applications to web3."
                "Your role is to critically assess the web2 application and recommend essential web3 functionalities only when they are truly needed."
            ),
            instructions=[
                "You will receive a detailed description of a web2 application.",
                f"The current functionalities you can provide are:\n{self.functions}",
                "Evaluate the provided functions and select only those that are necessary for enhancing the web2 application with web3 capabilities.",
                "Keep in mind that you need to give different tasks which can be implemented to bring web3 and the list should contain all the funtions needed to do the task."
                "For each task, list the necessary functions required to accomplish it.",
                "If a task requires only one function, provide just that function's name in the list.",
                "For each recommended function, provide a clear justification for its necessity and explain how it can be effectively integrated into the web3 application.",
            ],
            response_model=Functions,
            debug_mode=True
        )


    def run(self, user_prompt):
        run: RunResponse = self.converter.run(user_prompt)
        self.functions = []
        for funcs in run.content.functions:
            tool = []
            for func in funcs.function:
                tool.append(func)
        #         if func in self.toolkit:
        #             tool.append(self.toolkit[func])
        #         else:
        #             print(f"Warning: Function '{func}' not found in toolkit.")
            self.functions.append(tool)

# if __name__ == "__main__":
#     web3_converter = Web3Converter()
#     response = web3_converter.run(
        # """
        # EventSync - Smart Event Management Platform
        # Description:
        # EventSync is a cloud-based event management platform designed to simplify event planning, ticketing, and attendee engagement. It helps event organizers, businesses, and communities manage in-person and virtual events with ease.



        # Key Features:
        # Event Creation & Scheduling: Create and publish events with customizable details like time, location, and guest limits.
        # Online Ticketing & Registration: Sell tickets, generate QR codes for entry, and manage guest lists seamlessly.
        # Automated Reminders & Notifications: Send personalized email and SMS reminders to attendees.
        # Live Polls & Q&A: Engage attendees with real-time interactions during events.
        # AI-Powered Recommendations: Suggest events to users based on their interests and past attendance.
        # Post-Event Analytics: Track attendee engagement, feedback, and event success metrics.
        # Social Media Integration: Easily promote events across social media platforms.
        # """
#         )

#     print(web3_converter.functions)