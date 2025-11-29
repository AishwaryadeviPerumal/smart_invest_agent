import random
from google.adk.agents import Agent

market_data={ 'AAPL': {"ticker": 'AAPL', "price": 100.0, "volume": 120000, "move": "UP"},
              'TSLA': {"ticker": 'TSLA', "price": 150.0, "volume": 13000, "move": "DOWN"},
              'MSFT': {"ticker": 'MSFT', "price": 200.0, "volume": 140000, "move": "UP"}}

def get_market_data_for_ticker(ticker: str)-> dict[str,any]:
    if ticker in market_data.keys():
        current_market_date=market_data.get(ticker)
        current_market_date['price']=current_market_date['price']+(random.randint(1,10))
        current_market_date['volume']= current_market_date['volume']+(random.randint(100,200))
        return current_market_date
    return { "ticker": {ticker}, "price": random.randint(1,200), "volume": random.randint(100000,200000), "move": "UP"}


def get_market_data_for_portfolio(portfolio: list[str])-> dict[str,any]:
    """
    ADK-exposed tool that takes a list of tickers and returns random market data for each.
    ADK tools typically return a JSON-serializable result (dict).
    """
    market_data={}
    for ticker in portfolio:
        ticker_market_data = get_market_data_for_ticker(ticker)
        market_data[ticker] = ticker_market_data
    return {'status': 'Success', 'market_data':market_data}

analyst_agent = Agent(name="analyst_agent",
                   model="gemini-2.5-flash-lite",
                   description="Returns market data for the tickers in portfolio using the get_market_data_for_portfolio tool.",
                   instruction=("You are an excellent market data analyst assistant."
                                "when asked to provide market data for a portfolio, call the 'get_market_data_for_portfolio' tool "
                                "and return the tool's response as result to the user."),
                   tools=[get_market_data_for_portfolio])

if __name__ == "__main__":
    tickers=["AAPL", "TSLA", "MSFT"]
    ticker= random.choice(tickers)
    print(ticker)
    result= get_market_data_for_ticker(ticker)
    print(result)