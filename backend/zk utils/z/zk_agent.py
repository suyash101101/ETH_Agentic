from phi.model.google import Gemini
import os
from phi.agent import Agent
from dotenv import load_dotenv
import ast
import re

load_dotenv()

CIRCUITS_DIR='zk_circuits'

CIRCUITS_DICT = {
    "AnonAadhar": {
        "entry_point": "aadhaar-verifier.circom",
        "use_case": "Verifies Aadhaar QR data using RSA signature",
        "inputs": ["qrDataPadded", "qrDataPaddedLength", "delimiterIndices", "signature", "pubKey", "revealAgeAbove18", "revealGender", "revealPinCode", "revealState", "nullifierSeed", "signalHash"]
    },
    "circom-rln": {
        "entry_point": "rln.circom",
        "use_case": "Implements Rate-Limited Nullifier (RLN) for spam prevention",
        "inputs": ["identityCommitment", "merkleProof", "signalHash", "epoch", "rlnIdentifier"]
    },
    "openpassport": {
        "entry_point": "disclose/disclose.circom",
        "use_case": "Verifies and discloses specific attributes from a passport",
        "inputs": ["passportData", "attributeIndices", "signature", "pubKey"]
    },
    "semaphore": {
        "entry_point": "semaphore.circom",
        "use_case": "Anonymous signaling with zero-knowledge proofs",
        "inputs": ["secret", "merkleProofLength", "merkleProofIndices", "merkleProofSiblings", "message", "scope"]
    },
    "tornado": {
        "entry_point": "withdraw.circom",
        "use_case": "Anonymous transactions using zk-SNARKs",
        "inputs": ["nullifierHash", "recipient", "relayer", "fee", "refund", "root", "nullifier", "proof"]
    },
    "zk-email-verify": {
        "entry_point": "email-verifier.circom",
        "use_case": "Verifies email signature as per DKIM standard",
        "inputs": ["emailHeader", "emailHeaderLength", "pubkey", "signature", "emailBody", "emailBodyLength"]
    }
}

import re
import ast

def extract_list(response):
    print("Extracting from: ", response)
    match = re.search(r'\[.*?\]', response, re.DOTALL)
    if match:
        list_str = match.group(0)
        try:
            applications_list = ast.literal_eval(list_str)
            if isinstance(applications_list, list):
                return applications_list
            else:
                raise ValueError("Extracted content is not a list")
        except (ValueError, SyntaxError) as e:
            print(f"Error parsing extracted content: {e}")
            return []
    else:
        print("No Python list found in the response content")
        return []

class ZK_Agent():
    def __init__(self,debug=False):

        self.applications_finder_agent = Agent(
            model=Gemini(id="gemini-1.5-flash", api_key=os.getenv("GEMINI_API_KEY")),
            description=(
                "You are an expert in zero knowledge circuits and are well versed in applying zero knowledge concepts to solve problems."
                "Given a problem statement for you can identify potential applications of zero knowledge circuits specific to them."
                "You do not need to explain the implementation aspect of the zero knowledge circuits."
            ),
            instructions=(
                "Identify potential applications of zero knowledge circuits to solve the given problem statement."
                "Be clear and concise in your response."
                "Only operate on the information provided to you in the problem statement"
                "Make sure the zk applications are relevant to the problem statement."
                "If you cannot find any relevant applications, return an empty list."
                "Make sure the applications are not overlapping in nature"
                "Return a python list of potential applications in the descending order or relevenace like : ['application1', 'application2', 'application3']"
            ),
            debug_mode=False,
            reasoning=True,
        )

        self.zk_finder_agent = Agent(
            model=Gemini(id="gemini-1.5-flash", api_key=os.getenv("GEMINI_API_KEY")),
            description=(
                "You are an expert in zero knowledge circuits and are well versed in applying zero knowledge concepts to solve problems."
                "Given a zk application you can search and identify a pre-defined zk circuit from a given dictionary that exaclty suits the application's needs."
                "You do not need to explain the implementation aspect of the zero knowledge circuits."
                "Dictionary:"+str(CIRCUITS_DICT)
            ),
            instructions=(
                "Identify a pre-defined zero knowledge circuit that can be used to solve the given zk application."
                "Be clear and concise in your response."
                "Only return folders you can see in the base directory. If a folder is not in the base directory do not return it." 
                "Only operate on the information provided to you in the zk application."
                "Make sure the zk circuits you choose is relevant to the zk application."
                "If you cannot find a relevant zk circuit, return an empty list."
                "Return a python list of the zk circuit folders in the descending order of relevance like : ['circuit1', 'circuit2', 'circuit3']. Give this output in a single line."
            ),
            show_tool_calls=debug,
            debug_mode=debug
        )

    def find_zk_applications(self, problem_statement):
        response = self.applications_finder_agent.run(problem_statement)
        applications_list = extract_list(response.content)
        return applications_list
    
    def find_zk_circuits(self, zk_application):
        response = self.zk_finder_agent.run(zk_application)
        zk_circuits_list = extract_list(response.content)
        return zk_circuits_list
    
    def run(self,problem_statement):
        applications=agent.find_zk_applications(problem_statement)
        main_files=set()

        print(applications)
        for application in applications:
            circuits=agent.find_zk_circuits(application)
            for c in circuits:
                if c in CIRCUITS_DICT:
                    main_files.add(CIRCUITS_DIR+"/"+c+"/"+CIRCUITS_DICT[c]['entry_point'])
        
        return main_files
    
if __name__=='__main__':
    agent=ZK_Agent(debug=False)
    problem_statement="I want to build a airplane ticket system where I need to verify the person's passport and aadhar card."
    # problem_statement="I want to build an application where i want to prove that i have 2 factors for a number without revealling them."
    # applications=agent.find_zk_applications(problem_statement)
    # print("Applications:")
    # print(applications)
    # print()
    # circuits=agent.find_zk_circuits(applications[0])
    # print("Circuits:")
    # print(circuits)
    # main_files=set()

    # for application in applications:
    #     circuits=agent.find_zk_circuits(application)
    #     for c in circuits:
    #         if c in CIRCUITS_DICT:
    #             main_files.add(CIRCUITS_DIR+"/"+CIRCUITS_DICT[c]['entry_point'])
    
    # print(main_files)
    print(agent.run(problem_statement))
