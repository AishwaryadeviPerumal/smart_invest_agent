import random

from google.adk.tools import tool_context

options=[True, False]

async def handle_human_approval(ticker,amount,action)-> dict[str,any]:


    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint=f"Do you want to approve the proposed action?",
            payload={"ticker": ticker, "amount": {amount}, "action": {action}})
        return {  # This is sent to the Agent
            "status": 'pending',
            "message": f"Order for {ticker} with amount {amount} for {action} is waiting for human approval",
        }

    if tool_context.tool_confirmation.confirmed:
        return {
            "status": "Approved",
            "ticker": ticker,
            "amount": amount,
            "action": action,
            "message": f"Order for {ticker} with amount {amount} is Approved for {action}",
        }
    else:
        return {
            "status": "Rejected",
            "message": f"Order for {ticker} with amount {amount} is Rejected for {action}",
        }

def get_human_decision():
    is_approved=random.choice(options)
    # approved_rejected= 'Approved' if is_approved else 'Rejected'
    return is_approved