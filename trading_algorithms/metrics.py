def sharpe(history, risk_free_rate=0, yearly=True):
    print("length of history =", len(history))
    # sharpe ratio = (portfolio_return - risk_free_return)/std_dev
    
    # get returns
    returns = []
    prev = history[0]
    for i in range(1, len(history)):
        returns.append(history[i]/prev - 1)
        prev = history[i]
    
    # find mean
    mean = sum(returns)/len(returns)

    # find standard dev
    squared_sum_difference = 0
    for r in returns:
        squared_sum_difference += (r - mean)**2
    
    std_dev = (squared_sum_difference / len(returns))**0.5

    if yearly:
        # return daily sharpe ratio * sqrt(252) -> this annualises the sharpe_ratio (assuming 252 trading days a year)
        return ((mean - risk_free_rate) / std_dev) * 252**0.5
    else:
        # return daily sharpe ratio
        return ((mean - risk_free_rate) / std_dev)


def max_drawdown(history):
    # highest loss between any two points
    running_max = 0

    maximum_drawdown = 0

    for h in history:
        running_max = max(h, running_max)
        drawdown = abs((h - running_max) / running_max)
        maximum_drawdown = max(maximum_drawdown, drawdown)
    
    return maximum_drawdown


def cagr(history):
    # returns framed as compound interest rate
    return (history[-1]/history[0])**(252/len(history)) - 1

def calmar(history):
    return cagr(history) / abs(max_drawdown(history))