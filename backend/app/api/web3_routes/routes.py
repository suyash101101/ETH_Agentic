from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
# from ...web_3_agents.state import agent_state
from ...web_3_agents.main import Web3AgentManager

router = APIRouter(prefix="/web3", tags=["web3"])

agent_manager = Web3AgentManager()
# 
# Request/Response Models
class PromptRequest(BaseModel):
    prompt: str

class AgentRunRequest(BaseModel):
    agent_index: int = 0
    prompt: str
    wallet_id: str
class AgentResponse(BaseModel):
    name: str
    functions: List[str]
    wallet_address: str
    wallet_id: str

class CreateAgentsResponse(BaseModel):
    success: bool
    message: str
    agent_count: int
    agents: List[AgentResponse]

class RunAgentResponse(BaseModel):
    success: bool
    result: str

# Routes
@router.post("/create-agents", response_model=CreateAgentsResponse)
async def create_agents(
    request: PromptRequest,
):
    try:
        agents = agent_manager.create_agents(request.prompt)
        print(f"Created {len(agents)} agents with manager {id(agent_manager)}")
        
        agent_responses = [
            AgentResponse(
                name=f"agent{i+1}",
                functions=agent.function_names,
                wallet_address=agent._get_wallet_address(),
                wallet_id=agent.wallet_id # Always send the wallet_id back to the frontend
            )
            for i, agent in enumerate(agents)
        ]
        
        return CreateAgentsResponse(
            success=True,
            message=f"Created {len(agents)} agents",
            agent_count=len(agents),
            agents=agent_responses
        )
    except Exception as e:
        print(f"Error in create_agents route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents", response_model=List[AgentResponse])
async def get_agents():
    try:
        agents = agent_manager.get_agents()
        print(f"Getting agents from manager {id(agent_manager)}: {len(agents)} agents")
        
        responses = [
            AgentResponse(
                name=f"agent{i+1}",
                functions=agent.function_names,
                wallet_address=agent._get_wallet_address(),
                wallet_id=agent.wallet_id # Always send the wallet_id back to the frontend
            )
            for i, agent in enumerate(agents)
        ]
        print(f"Returning {len(responses)} agent responses")
        return responses
        
    except Exception as e:
        print(f"Error in get_agents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/run-agent", response_model=RunAgentResponse)
async def run_agent(
    request: AgentRunRequest
):
    try:
        result = agent_manager.run_agent(request.wallet_id, request.agent_index, request.prompt)
        return RunAgentResponse(
            success=True,
            result=result
        )
    except IndexError as e:
        raise HTTPException(status_code=404, detail=f"Agent {request.agent_index} not found")
    except Exception as e:
        print(f"Error running agent: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
