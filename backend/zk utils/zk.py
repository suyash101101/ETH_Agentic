from phi.model.google import Gemini
import os
from phi.agent import Agent, RunResponse
from phi.tools import tool
from dotenv import load_dotenv
load_dotenv()

class ZK_Builder:

    def __init__(self):

        self.logic_agent = Agent(
                model=Gemini(id="gemini-1.5-flash", api_key=os.getenv("GEMINI_API_KEY")),
                description=(
                    "You are a professional logic builder for zero-knowledge circuits."
                    "You will be given a problem statement where something needs to be proved."
                    "Your task is to design a zero-knowledge circuit that satisfies the following: correctness (valid proofs for true statements only), zero-knowledge (reveals nothing beyond the claim’s validity), completeness (always produces valid proofs for true statements), and soundness (prevents proofs for false statements)."
                    "Consider all edge cases, including ambiguous statements, boundary conditions, and security vulnerabilities, while optimizing for efficiency and ensuring consistency."
                ),
                instructions=(  
                    "Create a step-by-step logic for a zero-knowledge circuit."  
                    "You need to build a logic that satisfies correctness, zero-knowledge, completeness, and soundness."  
                    "Ensure the logic handles edge cases like ambiguous statements, boundary conditions, and security vulnerabilities, while optimizing for efficiency and consistency."  
                    "Make sure the output only contains the logic and no irrelevant explanations."
                    "Also keep the output as concise as possible."
                ) ,
                debug_mode=True
            )
        
        self.code_agent = Agent(
                model=Gemini(id="gemini-1.5-flash"),
                description=(
                    "You are an expert in writing and optimizing code for zero-knowledge circuits."
                    "Your task is to take the provided logic and implement it into a well-structured, efficient, and error-free zero-knowledge proof circuit."
                ),
                instructions=(  

                "You need to implement the given logic in Circom."
                "Ensure the code is correct, efficient, and concise."
                "Verify that the implementation is free of bugs."
                "Output only the code without any explanations."
                ) ,
                debug_mode=True
            )
        
    def build_logic(self, user_prompt):
        run: RunResponse = self.logic_agent.run(user_prompt)
        return run.content

    def build_code(self,logic):
        run: RunResponse=self.code_agent.run(logic)
        return run.content
    
    def build(self, user_prompt):
        logic = self.build_logic(user_prompt)
        code = self.build_code(logic)
        return code
            
            
if __name__=='__main__':
    agent = ZK_Builder()
    while True:
        user_prompt=input("Prompt: ")
        agent.build(user_prompt)
