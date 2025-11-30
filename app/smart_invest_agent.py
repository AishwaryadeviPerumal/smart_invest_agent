from google.adk import Agent
from google.adk.tools import FunctionTool, AgentTool
from google.genai import types

from google.adk.agents import LlmAgent
from google.adk.models import Gemini

from app.a2a.news_agent import news_agent
from app.agent_tool.risk_assess_agent import risk_assess_agent
from app.agent_tool.trade_proposal_agent import trade_proposal_agent
from app.human_in_loop.human_approval_agent import handle_human_approval
from app.mcp_local.analyst_agent import analyst_agent
from app.mcp_local.trade_execution_agent import trade_execution_agent

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)


smart_invest_agent = LlmAgent(
    name="smart_invest_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are a smart investment assistant.
  
  When users request to rebalance portfolio:
   1. Use the 'news_agent' tool with the portfolio details to get news data
  """,
    tools=[AgentTool(agent=news_agent),
           AgentTool(agent=analyst_agent),
          # AgentTool(agent=risk_assess_agent),
           # AgentTool(agent=trade_proposal_agent),
           # FunctionTool(func=handle_human_approval),
           # AgentTool(agent=trade_execution_agent)
           ],

)

print("✅ Smart Invest Agent created!")