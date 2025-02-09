from dotenv import load_dotenv
from cdp import *
import os
import json
from phi.model.google import Gemini
from phi.agent import Agent, RunResponse
from cdp.errors import UnsupportedAssetError

load_dotenv()

API_KEY_NAME = os.environ.get("CDP_API_KEY_NAME")
PRIVATE_KEY = os.environ.get("CDP_PRIVATE_KEY", "").replace('\\n', '\n')
Cdp.configure(API_KEY_NAME, PRIVATE_KEY)

class OnChainAgents:
    def __init__(self, Wallet_Id=None, functions=None):
        """
        Initializes the OnChainAgents class.

        The constructor checks if a Wallet_Id is provided. If not, it creates a new wallet.
        If a Wallet_Id is given, it attempts to fetch the wallet data associated with that ID.
        
        Parameters:
        Wallet_Id (str): Optional; If provided, attempts to load an existing wallet. 
                         If None, creates a new wallet.
        """
        self.WalletStorage = "wallet_storage"

        if not os.path.exists(self.WalletStorage):
            os.makedirs(self.WalletStorage)
            print(f"Directory '{self.WalletStorage}' created successfully.")

        if Wallet_Id is None:
            self.wallet = Wallet.create()
        else:
            fetched_data = self.fetch(Wallet_Id)
            if fetched_data:
                data = WalletData(wallet_id=fetched_data['wallet_id'], seed=fetched_data['seed'])
                self.wallet = Wallet.import_data(data)
            else:
                raise ValueError(f"Wallet with ID {Wallet_Id} could not be found.")
        self.agent = Agent(
            model=Gemini(model="gemini-2.0-flash-exp", api_key=os.environ.get("GEMINI_API_KEY")),
            tools=functions
        )


    def fetch(self, wallet_id):
        """
        Fetches the wallet data from a JSON file.

        This method constructs the file path for the specified wallet ID and attempts to read
        the corresponding JSON file. If the file exists, it loads the data and returns it as a dictionary.

        Parameters:
        wallet_id (str): The ID of the wallet to fetch.

        Returns:
        dict or None: The wallet data dictionary if found, else None.
        """
        file_path = os.path.join(self.WalletStorage, f"{wallet_id}.json")

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data_dict = json.load(file)
            print(f"Wallet data for {wallet_id} successfully fetched.")
            return data_dict
        else:
            print(f"No wallet data found for ID: {wallet_id}.")
            return None

    def store(self, data_dict):
        """
        Stores the wallet data securely in a JSON file.

        This method takes a dictionary containing wallet data and writes it to a JSON file
        named after the wallet ID. It ensures that the data is saved in a structured format.

        Parameters:
        data_dict (dict): Dictionary containing wallet data.
        """
        wallet_id = data_dict.get("wallet_id")
        file_path = os.path.join(self.WalletStorage, f"{wallet_id}.json")

        with open(file_path, 'w') as file:
            json.dump(data_dict, file)

    def save_wallet(self,data):
        """
        Exports and saves the current wallet's data and seed to files.

        This method exports the current state of the wallet and stores it in JSON format.
        It also saves the seed securely in an encrypted format and logs the wallet ID
        in a separate text file if it does not already exist.

        The process includes checking for existing IDs to prevent duplicates.
        """
        self.store(data.to_dict())
        
        seed_file_path = "my_seed.json"
        self.wallet.save_seed(seed_file_path, encrypt=True)

        wallet_id = data.wallet_id
        id_file_path = "wallet_ids.txt"

        if not self.wallet_id_exists(wallet_id, id_file_path):
            with open(id_file_path, "a") as id_file:
                id_file.write(f"{wallet_id}\n")

    def wallet_id_exists(self, wallet_id, file_path):
        """
        Checks if a given wallet ID exists in the specified text file.

        This method reads through a text file containing existing wallet IDs to determine
        whether the specified ID is present.

        Parameters:
        wallet_id (str): The ID of the wallet to check.
        
        Returns:
        bool: True if the ID exists, False otherwise.
        """
        if os.path.exists(file_path):
            with open(file_path, 'r') as id_file:
                existing_ids = id_file.read().splitlines()
                return wallet_id in existing_ids
        return False

    def run(self, prompt):
        """
        Asks the agent a question and returns the response.
        """
        response: RunResponse = self.agent.run(prompt)
        return response.content

