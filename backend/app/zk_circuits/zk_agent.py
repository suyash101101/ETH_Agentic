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
        "inputs" : {
            'qrDataPadded': { 'type': 'text', 'label': 'QR Data Padded', 'description': 'QR data without the signature, padded with 0', 'length': 'maxDataLength' },
            'qrDataPaddedLength': { 'type': 'number', 'label': 'QR Data Padded Length', 'description': 'Length of padded QR data' },
            'delimiterIndices': { 'type': 'text', 'label': 'Delimiter Indices', 'description': 'Indices of delimiters (255) in the QR text data', 'length': 18 },
            'signature': { 'type': 'text', 'label': 'Signature', 'description': 'RSA signature', 'length': 'k' },
            'pubKey': { 'type': 'text', 'label': 'Public Key', 'description': 'RSA public key (of the government)', 'length': 'k' },
            'revealAgeAbove18': { 'type': 'number', 'label': 'Reveal Age Above 18', 'description': 'Flag to reveal age is above 18' },
            'revealGender': { 'type': 'number', 'label': 'Reveal Gender', 'description': 'Flag to reveal extracted gender' },
            'revealPinCode': { 'type': 'number', 'label': 'Reveal Pin Code', 'description': 'Flag to reveal extracted pin code' },
            'revealState': { 'type': 'number', 'label': 'Reveal State', 'description': 'Flag to reveal extracted state' },
            'nullifierSeed': { 'type': 'number', 'label': 'Nullifier Seed', 'description': 'A random value used as an input to compute the nullifier' },
            'signalHash': { 'type': 'number', 'label': 'Signal Hash', 'description': 'Any message to commit to (to make it part of the proof)' }
        },

        "outputs" : {
            'pubkeyHash': { 'type': 'number', 'label': 'Public Key Hash', 'description': 'Poseidon hash of the RSA public key (after merging nearby chunks)' },
            'nullifier': { 'type': 'number', 'label': 'Nullifier', 'description': 'A unique value derived from nullifierSeed and Aadhaar data to nullify the proof/user' },
            'timestamp': { 'type': 'number', 'label': 'Timestamp', 'description': 'Timestamp of when the data was signed - extracted and converted to Unix timestamp' },
            'ageAbove18': { 'type': 'number', 'label': 'Age Above 18', 'description': 'Boolean flag indicating age is above 18; 0 if not revealed' },
            'gender': { 'type': 'number', 'label': 'Gender', 'description': 'Gender 70(F) or 77(M); 0 if not revealed' },
            'pinCode': { 'type': 'number', 'label': 'Pin Code', 'description': 'Pin code of the address as int; 0 if not revealed' },
            'state': { 'type': 'number', 'label': 'State', 'description': 'State packed as int (reverse order); 0 if not revealed' }
        },

        "parameters" : {
            'n': { 'type': 'number', 'label': 'RSA Public Key Size', 'description': 'RSA public key size per chunk' },
            'k': { 'type': 'number', 'label': 'Number of Chunks', 'description': 'Number of chunks the RSA public key is split into' },
            'maxDataLength': { 'type': 'number', 'label': 'Maximum Data Length', 'description': 'Maximum length of the data' }
        }
    },
    "circom-rln": {
        "entry_point": "rln.circom",
        "use_case": "Implements Rate-Limited Nullifier (RLN) for spam prevention",
        "inputs": {
            'identitySecret': { 'type': 'number', 'label': 'Identity Secret', 'description': 'Secret identity of the user' },
            'userMessageLimit': { 'type': 'number', 'label': 'User Message Limit', 'description': 'Limit on the number of messages a user can send' },
            'messageId': { 'type': 'number', 'label': 'Message ID', 'description': 'Identifier for the message' },
            'pathElements': { 'type': 'text', 'label': 'Path Elements', 'description': 'Elements of the Merkle tree path', 'length': 'DEPTH' },
            'identityPathIndex': { 'type': 'text', 'label': 'Identity Path Index', 'description': 'Index of the identity path in the Merkle tree', 'length': 'DEPTH' },
            'x': { 'type': 'number', 'label': 'X', 'description': 'Public input X' },
            'externalNullifier': { 'type': 'number', 'label': 'External Nullifier', 'description': 'External nullifier for the circuit' }
        },

        "outputs" :{
            'y': { 'type': 'number', 'label': 'Y', 'description': 'Output Y' },
            'root': { 'type': 'number', 'label': 'Root', 'description': 'Merkle tree root' },
            'nullifier': { 'type': 'number', 'label': 'Nullifier', 'description': 'Calculated nullifier' }
        },
        "parameters": {
            'DEPTH': { 'type': 'number', 'label': 'Depth', 'description': 'Depth of the Merkle tree' },
            'LIMIT_BIT_SIZE': { 'type': 'number', 'label': 'Limit Bit Size', 'description': 'Bit size limit for the range check' }
        }
    },
    "openpassport": {
        "entry_point": "disclose/vc_and_disclose.circom",
        "use_case": "Verifies and discloses specific attributes from a passport",
        "inputs" : {
            'secret': { 'type': 'number', 'label': 'Secret', 'description': 'Secret of the user — used to reconstruct commitment and generate nullifier' },
            'attestation_id': { 'type': 'number', 'label': 'Attestation ID', 'description': 'Attestation ID of the credential used to generate the commitment' },
            'dg1': { 'type': 'text', 'label': 'DG1', 'description': 'Data group 1 of the passport', 'length': 93 },
            'eContent_shaBytes_packed_hash': { 'type': 'number', 'label': 'eContent SHA Bytes Packed Hash', 'description': 'Hash of the eContent packed' },
            'dsc_tree_leaf': { 'type': 'number', 'label': 'DSC Tree Leaf', 'description': 'Leaf of the DSC tree, to keep a record of the full CSCA and DSC that were used' },
            'merkle_root': { 'type': 'number', 'label': 'Merkle Root', 'description': 'Root of the commitment merkle tree' },
            'leaf_depth': { 'type': 'number', 'label': 'Leaf Depth', 'description': 'Actual size of the merkle tree' },
            'path': { 'type': 'text', 'label': 'Path', 'description': 'Path of the commitment in the merkle tree', 'length': 'nLevels' },
            'siblings': { 'type': 'text', 'label': 'Siblings', 'description': 'Siblings of the commitment in the merkle tree', 'length': 'nLevels' },
            'selector_dg1': { 'type': 'number', 'label': 'Selector DG1', 'description': 'Bitmap used which bytes from the dg1 are revealed' },
            'majority': { 'type': 'number', 'label': 'Majority', 'description': 'Majority user wants to prove he is older than: YY — ASCII' },
            'current_date': { 'type': 'number', 'label': 'Current Date', 'description': 'Current date: YYMMDD — number' },
            'selector_older_than': { 'type': 'number', 'label': 'Selector Older Than', 'description': 'Bitmap used to reveal the majority' },
            'forbidden_countries_list': { 'type': 'text', 'label': 'Forbidden Countries List', 'description': 'Forbidden countries list user wants to prove he is not from', 'length': 'MAX_FORBIDDEN_COUNTRIES_LIST_LENGTH' },
            'smt_leaf_key': { 'type': 'number', 'label': 'SMT Leaf Key', 'description': 'Value of the leaf of the SMT corresponding to his path' },
            'smt_root': { 'type': 'number', 'label': 'SMT Root', 'description': 'Root of the SMT' },
            'smt_siblings': { 'type': 'text', 'label': 'SMT Siblings', 'description': 'Siblings of the SMT', 'length': 'nLevels' },
            'selector_ofac': { 'type': 'number', 'label': 'Selector OFAC', 'description': 'Bitmap used to reveal the OFAC verification result' },
            'scope': { 'type': 'number', 'label': 'Scope', 'description': 'Scope of the application users generates the proof for' },
            'user_identifier': { 'type': 'number', 'label': 'User Identifier', 'description': 'User identifier — address or UUID' }
        },

        "outputs" : {
            'revealedData_packed': { 'type': 'number', 'label': 'Revealed Data Packed', 'description': 'Packed revealed data' },
            'forbidden_countries_list_packed': { 'type': 'number', 'label': 'Forbidden Countries List Packed', 'description': 'Packed forbidden countries list' },
            'nullifier': { 'type': 'number', 'label': 'Nullifier', 'description': 'Scope nullifier - not deterministic on the passport data' }
        },

        "parameters" : {
            'nLevels': { 'type': 'number', 'label': 'Number of Levels', 'description': 'Maximum number of levels in the merkle tree' },
            'MAX_FORBIDDEN_COUNTRIES_LIST_LENGTH': { 'type': 'number', 'label': 'Max Forbidden Countries List Length', 'description': 'Maximum number of countries present in the forbidden countries list' }
        },
    },
    "semaphore": {
        "entry_point": "semaphore.circom",
        "use_case": "Anonymous signaling with zero-knowledge proofs",
        "inputs": ["secret", "merkleProofLength", "merkleProofIndices", "merkleProofSiblings", "message", "scope"]
    },
    "tornado": {
        "entry_point": "withdraw.circom",
        "use_case": "Anonymous transactions using zk-SNARKs",
        "inputs" :{
            'root': { 'type': 'number', 'label': 'Merkle Root', 'description': 'Root of the commitment merkle tree' },
            'nullifierHash': { 'type': 'number', 'label': 'Nullifier Hash', 'description': 'Hash of the nullifier' },
            'recipient': { 'type': 'number', 'label': 'Recipient', 'description': 'Recipient address' },
            'relayer': { 'type': 'number', 'label': 'Relayer', 'description': 'Relayer address' },
            'fee': { 'type': 'number', 'label': 'Fee', 'description': 'Transaction fee' },
            'refund': { 'type': 'number', 'label': 'Refund', 'description': 'Refund amount' },
            'nullifier': { 'type': 'number', 'label': 'Nullifier', 'description': 'Private nullifier input' },
            'secret': { 'type': 'number', 'label': 'Secret', 'description': 'Private secret input' },
            'pathElements': { 'type': 'text', 'label': 'Path Elements', 'description': 'Elements of the Merkle tree path', 'length': 'levels' },
            'pathIndices': { 'type': 'text', 'label': 'Path Indices', 'description': 'Indices of the Merkle tree path', 'length': 'levels' }
        },

        "outputs": {
            'recipientSquare': { 'type': 'number', 'label': 'Recipient Square', 'description': 'Square of the recipient address' },
            'feeSquare': { 'type': 'number', 'label': 'Fee Square', 'description': 'Square of the transaction fee' },
            'relayerSquare': { 'type': 'number', 'label': 'Relayer Square', 'description': 'Square of the relayer address' },
            'refundSquare': { 'type': 'number', 'label': 'Refund Square', 'description': 'Square of the refund amount' }
        },

        "parameters": {
            'levels': { 'type': 'number', 'label': 'Levels', 'description': 'Number of levels in the Merkle tree' }
        }
    },
    "zk-email-verify": {
        "entry_point": "email-verifier.circom",
        "use_case": "Verifies email signature as per DKIM standard",
        "inputs" : {
            'emailHeader': { 'type': 'text', 'label': 'Email Header', 'description': 'Email headers that are signed (ones in `DKIM-Signature` header) as ASCII int[], padded as per SHA-256 block size', 'length': 'maxHeadersLength' },
            'emailHeaderLength': { 'type': 'number', 'label': 'Email Header Length', 'description': 'Length of the email header including the SHA-256 padding' },
            'pubkey': { 'type': 'text', 'label': 'Public Key', 'description': 'RSA public key split into k chunks of n bits each', 'length': 'k' },
            'signature': { 'type': 'text', 'label': 'Signature', 'description': 'RSA signature split into k chunks of n bits each', 'length': 'k' },
            'emailBody': { 'type': 'text', 'label': 'Email Body', 'description': 'Email body after the precomputed SHA as ASCII int[], padded as per SHA-256 block size', 'length': 'maxBodyLength' },
            'emailBodyLength': { 'type': 'number', 'label': 'Email Body Length', 'description': 'Length of the email body including the SHA-256 padding' },
            'bodyHashIndex': { 'type': 'number', 'label': 'Body Hash Index', 'description': 'Index of the body hash `bh` in the emailHeader' },
            'precomputedSHA': { 'type': 'text', 'label': 'Precomputed SHA', 'description': 'Precomputed SHA-256 hash of the email body till the bodyHashIndex', 'length': 32 },
            'decodedEmailBodyIn': { 'type': 'text', 'label': 'Decoded Email Body In', 'description': 'Decoded email body without soft line breaks', 'length': 'maxBodyLength' },
            'mask': { 'type': 'text', 'label': 'Mask', 'description': 'Mask for the email body', 'length': 'maxBodyLength' }
        },

        "outputs" : {
            'pubkeyHash': { 'type': 'number', 'label': 'Public Key Hash', 'description': 'Poseidon hash of the pubkey - Poseidon(n/2)(n/2 chunks of pubkey with k*2 bits per chunk)' },
            'decodedEmailBodyOut': { 'type': 'text', 'label': 'Decoded Email Body Out', 'description': 'Decoded email body with soft line breaks removed', 'length': 'maxBodyLength' },
            'maskedHeader': { 'type': 'text', 'label': 'Masked Header', 'description': 'Masked email header', 'length': 'maxHeadersLength' },
            'maskedBody': { 'type': 'text', 'label': 'Masked Body', 'description': 'Masked email body', 'length': 'maxBodyLength' }
        },

        "parameters" :{
            'maxHeadersLength': { 'type': 'number', 'label': 'Max Headers Length', 'description': 'Maximum length for the email header' },
            'maxBodyLength': { 'type': 'number', 'label': 'Max Body Length', 'description': 'Maximum length for the email body' },
            'n': { 'type': 'number', 'label': 'N', 'description': 'Number of bits per chunk the RSA key is split into. Recommended to be 121' },
            'k': { 'type': 'number', 'label': 'K', 'description': 'Number of chunks the RSA key is split into. Recommended to be 17' },
            'ignoreBodyHashCheck': { 'type': 'number', 'label': 'Ignore Body Hash Check', 'description': 'Set 1 to skip body hash check in case data to prove/extract is only in the headers' },
            'enableHeaderMasking': { 'type': 'number', 'label': 'Enable Header Masking', 'description': 'Set 1 to turn on header masking' },
            'enableBodyMasking': { 'type': 'number', 'label': 'Enable Body Masking', 'description': 'Set 1 to turn on body masking' },
            'removeSoftLineBreaks': { 'type': 'number', 'label': 'Remove Soft Line Breaks', 'description': 'Set 1 to remove soft line breaks from the email body' }
        },
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
            # reasoning=True,
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
                "The application must exactly satify the given problem."
                "Make the sure the circuit returned can be directly used. If it is vaguely related do not return it."
                "Be clear and concise in your response."
                "Only return circuits in the dictionary."
                "Only operate on the information provided to you in the zk application."
                "Make sure the zk circuits you choose is relevant to the zk application."
                "If you cannot find a relevant zk circuit, return an empty list."
                "Return a python list of the zk circuit in the descending order of relevance like : ['circuit1', 'circuit2', 'circuit3']. Give this output in a single line."
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
        final=[]
        for application in applications:
            circuits=agent.find_zk_circuits(application)
            
            for c in circuits:
                circ=CIRCUITS_DICT[c].copy()
                circ['entry_point']=CIRCUITS_DIR+"/"+c+"/"+CIRCUITS_DICT[c]['entry_point']
                final.append(circ)
                # final[-1]
                # if c in CIRCUITS_DICT:
                #     main_files.add(CIRCUITS_DIR+"/"+c+"/"+CIRCUITS_DICT[c]['entry_point'])
        
        return final
    
# if __name__=='__main__':
#     agent=ZK_Agent(debug=False)
#     problem_statement="I want to build a airplane ticket system where I need to verify the person's passport and aadhar card."
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
    # print(agent.run(problem_statement))