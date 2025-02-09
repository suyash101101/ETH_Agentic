from converter_agent import Web3Converter
from onchain_agent import OnChainAgents

def main():
    web3_converter = Web3Converter()
    prompt = input("Enter the prompt: ")
    web3_converter.run(prompt)

    agents = []
    
    agent_counter = 1  # Initialize a counter for agent naming

    for func in web3_converter.functions:
        if len(func) > 1:  # Check if there are multiple functions
            agent_name = f"agent{agent_counter}"  # Create a unique agent name
            agent = OnChainAgents(functions=func)
            print(f"{agent_name} created with functions: {func}")  # Print the agent name and its functions
            agent_counter += 1  # Increment the counter for the next agent
            agents.append(agent)
    print(agents[0].run("Hi"))
    return agents




if __name__ == "__main__":
    main()