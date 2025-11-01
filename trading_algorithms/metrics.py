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
        # return daily sharpe ratio * sqrt(252) -> this annualises the sharpe_ratio
        return ((mean - risk_free_rate) / std_dev) * 252**0.5
    else:
        # return daily sharpe ratio
        return ((mean - risk_free_rate) / std_dev)


