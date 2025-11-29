import random
from google.adk.agents import Agent
#from app.authentication.authentication import google_api_key


def get_news_for_ticker(ticker: str)-> str:
    news_events = [
        f"Positive outlook expected for {ticker}.",
        f"Negative sentiment detected around {ticker}.",
        f"The CEO of {ticker} has resigned.",
        f"{ticker} just announced a major product launch.",
        f"{ticker} is facing regulatory scrutiny.",
        f"{ticker} reports record quarterly earnings.",
        f"{ticker} announces unexpected layoffs.",
        f"Market analysts upgraded {ticker}'s stock rating.",
        f"Market analysts downgraded {ticker}'s stock rating.",
        f"{ticker} involved in a major partnership deal."
    ]
    return random.choice(news_events)

def get_news_for_portfolio(portfolio: list[str])-> dict[str,any]:
    """
    ADK-exposed tool that takes a list of tickers and returns random news for each.
    ADK tools typically return a JSON-serializable result (dict).
    """
    news_report={}
    for ticker in portfolio:
        ticker_news = get_news_for_ticker(ticker)
        news_report[ticker] = ticker_news
    return {'status': 'Success', 'news':news_report}

news_agent = Agent(name="news_agent",
                   model="gemini-2.5-flash-lite",
                   description="Returns randomized news headlines for portfolio tickers using the get_news_for_portfolio tool.",
                   instruction=("You are an excellent news generator assistant."
                                "when asked to provide news for a portfolio, call the 'get_news_for_portfolio'tool "
                                "when response received, fetch the news field and evaluate the sentiment of the news, whether it is positive or negative"
                                "then add a new field called 'sentiment' with value being positive or negative based on your sentiment analysis"
                                "now return the tool's news field and sentiment fields as a result to the user."),
                   tools=[get_news_for_portfolio])

if __name__ == "__main__":
    result=get_news_for_portfolio(["AAPL", "TSLA", "MSFT"])
    print(result)