import random

from google.adk.tools import tool_context

options=['Yes', 'No']

async def get_human_approval(ticker,amount,action)-> dict[str,any]:
    is_approved=random.choice(options)
    approved_rejected= 'Approved' if is_approved else 'Rejected'

    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint=f"Do you want to approve the proposed action?",
            payload={"ticker": ticker, "amount": {amount}, "action": {action}})
        return {  # This is sent to the Agent
            "status": is_approved,
            "message": f"Order for {ticker} with amount {amount} is {approved_rejected} for {action}",
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

