from web3 import Web3
import json
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv
import time
from requests.exceptions import RequestException

load_dotenv()

# Base Testnet RPC URL
BASE_TESTNET_RPC = os.getenv("ALCHEMY_URL")

# Contract address
CONTRACT_ADDRESS = "0xB9827072944AcE98726A8DdCfD5f52A1ab9D4de5"

# Update contract addresses
CONTRACT_ADDRESSES = {
    'token': '0x8E0837578E2Ceb5E8a26C6381072cF2B8810a868',
    'basicNFT': '0xB9827072944AcE98726A8DdCfD5f52A1ab9D4de5',
    'crowdFunding': '0x06D09AA4e055cBb4f71287F37De70fd632DA02Bb',
    # Dummy addresses for other contracts - to be updated later
    'staking': '0x0000000000000000000000000000000000000001',
    'voting': '0x0000000000000000000000000000000000000002',
    'multiSigWallet': '0x0000000000000000000000000000000000000003',
    'timeLock': '0x0000000000000000000000000000000000000004',
    'simpleDEX': '0x0000000000000000000000000000000000000005',
    'escrow': '0x0000000000000000000000000000000000000006',
    'subscription': '0x0000000000000000000000000000000000000007'
}

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(BASE_TESTNET_RPC))


class SmartContractInteractor:
    def __init__(self, private_key: str = None, max_retries: int = 3):
        self.max_retries = max_retries
        self._initialize_web3()
        self.contract_address = CONTRACT_ADDRESS
        self.private_key = private_key
        self.abis = self._load_abis()
        self.contract = self._initialize_contract()

    def _initialize_web3(self):
        """Try multiple RPC endpoints"""
        try:
            self.w3 = Web3(Web3.HTTPProvider(BASE_TESTNET_RPC))
            # Test connection
            self.w3.eth.block_number
            print(f"Successfully connected to {BASE_TESTNET_RPC}")
            return
        except Exception as e:
            print(f"Failed to connect to {BASE_TESTNET_RPC}: {str(e)}")
            raise Exception("Failed to connect to any RPC endpoint")

    def _load_abis(self) -> Dict[str, Any]:
        """Load all ABI files from the contracts directory"""
        # Get the current file's directory
        current_dir = Path(__file__).resolve().parent
        
        # Navigate to the contracts directory (going up two levels)
        abi_dir = current_dir.parent.parent / 'contracts' / 'abis'
        
        if not abi_dir.exists():
            raise FileNotFoundError(f"Contracts directory not found at {abi_dir}")
            
        abis = {}
        
        # Map contract names to their JSON files
        abi_files = {
            'token': 'token.json',
            'basicNFT': 'nft.json',
            'crowdFunding': 'crowdFunding.json',
            'staking': 'staking.json',
            'voting': 'voting.json',
            'multiSigWallet': 'MultiSigWalet.json',
            'timeLock': 'timeLock.json',
            'simpleDEX': 'simpleDEX.json',
            'escrow': 'escrow.json',
            'subscription': 'subscription.json'
        }
        
        for contract_name, json_file in abi_files.items():
            abi_path = abi_dir / json_file
            try:
                with open(abi_path, 'r') as f:
                    abis[contract_name] = json.load(f)
            except FileNotFoundError:
                print(f"Warning: ABI file {json_file} not found at {abi_path}")
                continue
                
        if not abis:
            raise FileNotFoundError("No ABI files could be loaded")
            
        return abis

    def _initialize_contract(self, contract_name: str = 'token'):
        """Initialize the main contract"""
        return self.w3.eth.contract(address=CONTRACT_ADDRESSES[contract_name], abi=self.abis[contract_name])

    def _get_transaction_params(self, from_address: str, value: int = 0):
        """Get basic transaction parameters with retry logic"""
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                return {
                    'from': from_address,
                    'value': value,
                    'gasPrice': self.w3.eth.gas_price,
                    'nonce': self.w3.eth.get_transaction_count(from_address),
                }
            except Exception as e:
                retry_count += 1
                if retry_count == self.max_retries:
                    raise Exception(f"Failed to get transaction params: {str(e)}")
                print(f"Failed to get transaction params, retrying... (attempt {retry_count}/{self.max_retries})")
                time.sleep(1)

    # Token Functions
    def transfer_tokens(self, to_address: str, amount: int, from_address: str):
        """Transfer tokens to another address"""
        tx_params = self._get_transaction_params(from_address)
        tx = self.contract.functions.transfer(to_address, amount).build_transaction(tx_params)
        return self._send_transaction(tx)

    # NFT Functions
    def mint_nft(self, from_address: str):
        """Mint a new NFT"""
        contract = self._initialize_contract('basicNFT')
        tx_params = self._get_transaction_params(from_address)
        tx = contract.functions.mint().build_transaction(tx_params)
        return self._send_transaction(tx)

    # Crowdfunding Functions
    def contribute_to_campaign(self, amount: int, from_address: str):
        """Contribute to crowdfunding campaign"""
        contract = self._initialize_contract('crowdFunding')
        tx_params = self._get_transaction_params(from_address, amount)
        tx = contract.functions.contribute().build_transaction(tx_params)
        return self._send_transaction(tx)

    # Staking Functions
    def stake_tokens(self, amount: int, from_address: str):
        """Stake tokens"""
        contract = self._initialize_contract('staking')
        tx_params = self._get_transaction_params(from_address, amount)
        tx = contract.functions.stake().build_transaction(tx_params)
        return self._send_transaction(tx)

    def withdraw_stake(self, from_address: str):
        """Withdraw staked tokens"""
        contract = self._initialize_contract('staking')
        tx_params = self._get_transaction_params(from_address)
        tx = contract.functions.withdraw().build_transaction(tx_params)
        return self._send_transaction(tx)

    # Voting Functions
    def cast_vote(self, proposal_id: int, from_address: str):
        """Cast a vote for a proposal"""
        contract = self._initialize_contract('voting')
        tx_params = self._get_transaction_params(from_address)
        tx = contract.functions.vote(proposal_id).build_transaction(tx_params)
        return self._send_transaction(tx)

    # TimeLock Functions
    def deposit_timelock(self, amount: int, from_address: str):
        """Deposit to timelock contract"""
        contract = self._initialize_contract('timeLock')
        tx_params = self._get_transaction_params(from_address, amount)
        tx = contract.functions.deposit().build_transaction(tx_params)
        return self._send_transaction(tx)

    def withdraw_timelock(self, from_address: str):
        """Withdraw from timelock contract"""
        contract = self._initialize_contract('timeLock')
        tx_params = self._get_transaction_params(from_address)
        tx = contract.functions.withdraw().build_transaction(tx_params)
        return self._send_transaction(tx)

    # DEX Functions
    def deposit_to_dex(self, token_address: str, amount: int, from_address: str):
        """Deposit tokens to DEX"""
        contract = self._initialize_contract('simpleDEX')
        tx_params = self._get_transaction_params(from_address)
        tx = contract.functions.deposit(token_address, amount).build_transaction(tx_params)
        return self._send_transaction(tx)

    def withdraw_from_dex(self, token_address: str, amount: int, from_address: str):
        """Withdraw tokens from DEX"""
        contract = self._initialize_contract('simpleDEX')
        tx_params = self._get_transaction_params(from_address)
        tx = contract.functions.withdraw(token_address, amount).build_transaction(tx_params)
        return self._send_transaction(tx)

    # Subscription Functions
    def subscribe(self, from_address: str, amount: int):
        """Subscribe to a service"""
        contract = self._initialize_contract('subscription')
        tx_params = self._get_transaction_params(from_address, amount)
        tx = contract.functions.subscribe().build_transaction(tx_params)
        return self._send_transaction(tx)

    def _send_transaction(self, transaction):
        """Sign and send a transaction"""
        if not self.private_key:
            raise ValueError("Private key not set")
        
        # Add gas estimate to transaction
        transaction['gas'] = self.w3.eth.estimate_gas(transaction)
        
        # Sign transaction
        signed_tx = self.w3.eth.account.sign_transaction(transaction, self.private_key)
        
        # Use raw_transaction instead of rawTransaction
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def debug_paths(self):
        """Print debug information about paths"""
        current_dir = Path(__file__).resolve().parent
        abi_dir = current_dir.parent.parent / 'contracts' / 'abis'
        
        print("Path Debug Information:")
        print(f"Current file location: {current_dir}")
        print(f"Expected ABI directory: {abi_dir}")
        print(f"ABI directory exists: {abi_dir.exists()}")
        
        if abi_dir.exists():
            print("\nAvailable files in ABI directory:")
            for file in abi_dir.glob('*.json'):
                print(f"- {file.name}")

# Example usage
if __name__ == "__main__":
    PRIVATE_KEY = os.getenv("WALLET_PRIVATE_KEY")
    contract_interactor = SmartContractInteractor(PRIVATE_KEY)
    wallet_address = os.getenv("WALLET_ADDRESS")
    
    try:
        # Example: Mint NFT
        tx_receipt = contract_interactor.mint_nft(wallet_address)
        print(f"NFT Minted! Transaction hash: {tx_receipt['transactionHash'].hex()}")
        
        
    except Exception as e:
        print(f"Error: {str(e)}") 