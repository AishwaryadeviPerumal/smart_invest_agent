import random

from google.adk import Agent


def evaluate(ticker: str, news_data: dict, market_data: dict,allocation_pct: float ):
    """
       Parameters:
           ticker (str): Stock symbol
           analyst_data (dict): Output from analyst_agent.get_market_data_for_ticker()
           news_data (dict): Output from news_agent.get_news_for_portfolio()
           allocation_pct (float): % of portfolio in this position

       Returns:
           dict: Full risk evaluation.
       """

    #risk_pref = self.memory.get("risk_tolerance", "medium")


    risk_score = 0
    sentiment = news_data['sentiment']

    move=market_data['move']
    if sentiment == 'positive'and allocation_pct > 20 and move == 'up' :
        risk_score -= 3
    elif sentiment == 'positive'and allocation_pct > 20 and move == 'down' :
        risk_score -= 2
    elif sentiment == 'positive'and allocation_pct < 20:
        risk_score -= 1
    elif sentiment == 'negative' and allocation_pct > 20 and move == 'down':
        risk_score += 5
    elif sentiment == 'negative' and allocation_pct > 20 and move == 'up':
        risk_score += 3
    elif sentiment == 'negative' and allocation_pct < 20:
        risk_score += 2
    else:
        risk_score += 0
    return {
        "ticker": ticker,
        "risk_score": risk_score,
        "sentiment": sentiment,
        "allocation_pct": allocation_pct
    }

risk_assess_agent = Agent(name="risk_assess_agent",
                      model="gemini-2.5-flash-lite",
                      description="Assess risk based on the market data and news data for the ticker using the evaluate tool.",
                      instruction=("You are an excellent Risk Assess assistant."
                                   "when asked to evaluate risk for the given ticker with news_data, market_data and allocation_pct, call the 'evaluate' tool "
                                   "and return the tool's response as result to the user."),
                      tools=[evaluate])

if __name__ == "__main__":
    tickers=["AAPL", "TSLA", "MSFT"]
    ticker= random.choice(tickers)
    print(ticker)
    news_data={'status': 'Success', 'news': f"Positive outlook expected for {ticker}.",'sentiment': 'positive'}
    analyst_data= { "ticker": {ticker}, "price": random.randint(1,200), "volume": random.randint(100000,200000), "move": "UP"}
    result= evaluate(ticker,news_data, analyst_data, 30)
    print(result)