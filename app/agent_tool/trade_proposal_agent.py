import random

from google.adk import Agent


def propose(analyst_data, news_data, risk_data):
    """
   Combines Analyst + News + Risk reports to generate a trade suggestion.
   """
    suggestions = []

    if news_data["sentiment"] == 'positive' and risk_data["risk_score"] <= 0:
        suggestions.append({
            "action": "BUY",
            "quantity": random.randint(10,20),
            "reason": "Positive news + low risk",
            "price": analyst_data["price"]
        })
    elif news_data["sentiment"] == 'negative':
        suggestions.append({
            "action": "SELL",
            "quantity": random.randint(10,15),
            "reason": "Negative sentiment",
            "price": analyst_data["price"]
        })

    return suggestions


trade_proposal_agent = Agent(name="trade_proposal_agent",
                      model="gemini-2.5-flash-lite",
                      description="Returns trade suggestions for the ticker using the propose tool.",
                      instruction=("You are an excellent trade proposal assistant."
                                   "when asked to provide trade suggestion for a ticker, call the 'propose' tool "
                                   "and return the tool's response as result to the user."),
                      tools=[propose])

if __name__ == "__main__":
    tickers=["AAPL", "TSLA", "MSFT"]
    ticker= random.choice(tickers)
    print(ticker)
    news_data={'status': 'Success', 'news': f"Positive outlook expected for {ticker}.",'sentiment': 'positive'}
    analyst_data= { "ticker": {ticker}, "price": random.randint(1,200), "volume": random.randint(100000,200000), "move": "UP"}
    risk_data = {"ticker": ticker,  "risk_score": 0, "sentiment": news_data['sentiment'], "allocation_pct": 30 }
    result= propose(analyst_data,news_data, risk_data)
    print(result)