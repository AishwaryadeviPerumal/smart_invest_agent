from google.adk import Agent


async def execute_trade(self, ticker: str, action: str, amount: str)-> dict[str, any]:
    """
    ADK-exposed tool that takes a ticker, action and amount and returns status of order execution.
    ADK tools typically return a JSON-serializable result (dict).
    """
    print(str.format(f'[MCP Tool] Executing {action} {amount} shares of {ticker}'))
    return {'status': 'Success','message': str.format(f'[MCP Tool] Execution to {action} {amount} shares of {ticker} is success!')}


news_agent = Agent(name="trade_execution_agent",
                       model="gemini-2.5-flash-lite",
                       description="Executes sell/buy order for the given ticker with the amount using the execute_trade tool.",
                       instruction=("You are an excellent Trade Executor assistant."
                                    "when asked to execute trade for a ticker with the amount and action, call the 'execute_trade'tool "
                                    "and return the tool's message field as result to the user."),
                       tools=[execute_trade])