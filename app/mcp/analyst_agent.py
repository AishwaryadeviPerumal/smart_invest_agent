import random
from google.adk.agents import Agent

market_data={ 'AAPL': {"ticker": 'AAPL', "price": 100.0, "volume": 120000},
              'TSLA': {"ticker": 'TSLA', "price": 150.0, "volume": 13000},
              'MSFT': {"ticker": 'MSFT', "price": 200.0, "volume": 140000}}

def get_market_data_for_ticker(ticker: str)-> dict[str,any]:
    if ticker in market_data.keys():
        current_market_date=market_data.get(ticker)
        current_market_date['price']=current_market_date['price']+(random.randint(1,10))
        current_market_date['volume']= current_market_date['volume']+(random.randint(100,200))
        return current_market_date
    return { "ticker": {ticker}, "price": random.randint(1,200), "volume": random.randint(100000,200000) }


analyst_agent = Agent(name="analyst_agent",
                   model="gemini-2.5-flash-lite",
                   description="Returns market data for the ticker using the get_market_data_for_ticker tool.",
                   instruction=("You are an excellent market data analyst assistant."
                                "when asked to provide market data for a ticker, call the 'get_market_data_for_ticker' tool "
                                "and return the tool's response as result to the user."),
                   tools=[get_market_data_for_ticker])

if __name__ == "__main__":
    tickers=["AAPL", "TSLA", "MSFT"]
    ticker= random.choice(tickers)
    print(ticker)
    result= get_market_data_for_ticker(ticker)
    print(result)