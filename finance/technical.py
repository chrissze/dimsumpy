
# STANDARD LIBS
from typing import List, Optional
from statistics import mean



def convert_to_changes(n: int, list_x: List[float]) -> List[float]:
    """
    convert a list of closing prices to a list of 'changes in n days' 
    """
    if len(list_x) < n + 1:
        return []
    else:
        xs = list_x
        result = []
        while len(xs) > n:
            change_in_n_periods = (xs[0] - xs[n]) / xs[n]
            result.append(change_in_n_periods)
            xs = xs[1:]
        return result


def ema(n: int, list_x: List[float]) -> float:
    """
    USED BY: steep
    
    test: listx = [22.17, 22.4, 23.1, 22.68, 23.33, 23.1, 23.19, 23.65, 23.87, 23.82
                  , 23.63, 23.95, 23.83, 23.75, 24.05, 23.36, 22.61, 22.38, 22.39, 22.15
                  , 22.29, 22.24, 22.43, 22.23, 22.13, 22.18, 22.17, 22.08, 22.19, 22.27]
    https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:moving_averages """
    m = n * 3  # can be changed to n*2
    list_m = list_x[:m]   # safe
    length = len(list_m)
    if m != length:
        return 0.0
    else:
        def f(em_, x_): return (x_ - em_) * weight + em_
        weight = 2.0 / (n + 1)
        first_ma = sma(n, list_m[-n:])
        em = first_ma
        xs = list_m[:-n]   # safe
        while xs:
            x = xs[-1]  # safe because list is not empty
            em = f(em, x)
            xs = xs[:-1]  # safe
        return em


def emas(n: int, list_x: List[float]) -> List[float]:
    """
    USED BY: steep
    """
    min_length = 3 * n - 1
    result_list = []  # mutate
    xs = list_x  # mutate
    while len(xs) > min_length:
        em = ema(n, xs)
        result_list.append(em)
        xs = xs[1:]
    return result_list


def quantile(q: float, xs: List[float]) -> float:
    length = len(xs)
    n = length + 1
    i = int(q * n - 1.0)
    if not xs or q < 0.0 or q > 1.0:
        return 0.0
    elif length > i > 0:
        return sorted(xs)[i]
    else:
        return 0.0


def deltas(n: int, list_x: List[float]) -> List[float]:
    """
    USED BY: calculate_rsi()
    """

    if len(list_x) < n + 1:
        return []
    else:
        xs = list_x
        result = []
        while len(xs) > n:
            diff = xs[0] - xs[n]
            result.append(diff)
            xs = xs[1:]
        return result



def calculate_rsi(n: int, xs: List[float]) -> Optional[float]:
    """
    DEPENDS ON: deltas() 
    calculate_rsi(listb * 100)
    
    typical RSI input list needs to be at least 14 * 14 + 1 days, that is 197 trading days.
    Weekly RSI requires 197 * 5, approximately 1000 trading days (4 years)

    """
    minimum_length = 14 * n + 1
    if len(xs) < minimum_length:
        return None
    else:
        def f(x_, avg): return (avg * (n - 1) + x_) / n
        init_list = xs[: 13 * n + 1]
        tail_list = xs[13 * n:]    # length is n + 1
        tail_diff = deltas(1, tail_list)
        first_avg_gain = sum(filter(lambda a: a > 0.0, tail_diff)) / n
        first_avg_loss = -(sum(filter(lambda a: a < 0.0, tail_diff))) / n  # mypy error using abs
        init_diff = deltas(1, init_list)
        gain_list = list(map(lambda a: a if a > 0.0 else 0.0, init_diff))
        loss_list = list(map(lambda a: abs(a) if a < 0.0 else 0.0, init_diff))
        avg_gain = first_avg_gain  # mutate
        g_list = gain_list         # mutate
        while g_list:
            x = g_list[-1]
            avg_gain = f(x, avg_gain)
            g_list = g_list[:-1]
        avg_loss = first_avg_loss   # mutate
        l_list = loss_list         # mutate
        while l_list:
            x = l_list[-1]
            avg_loss = f(x, avg_loss)
            l_list = l_list[:-1]
        rs = avg_gain / avg_loss if avg_loss != 0 else 0.0
        rs_index = 100.0 - (100.0 / (1.0 + rs))
        return rs_index


def sma(n: int, xs: List[float]) -> Optional[float]:
    """
    IMPORTS: mean()

    Simple Moving Average
    """
    if n > len(xs):
        return None
    else:
        return mean(xs[:n])


def smas(n: int, list_x: List[float]) -> List[float]:
    """
    List of Simple Moving Averages
    mu is greek letter mu which denotes mean

    """
    result_list = []
    xs = list_x
    while len(xs) > (n - 1):
        mu = sma(n, xs)
        result_list.append(mu)
        xs = xs[1:]
    return result_list


def steep(n: int, xs: List[float]) -> Optional[float]:
    """
    DEPENDS ON: ema, emas

    steep20 requires minimum length of list_x = 20 * 3 + 5 = 65
    steep50 requires minimum length of list_x = 50 * 3 + 5 = 155

    em_list needs to skip the first value because first value is already calculated as em_value, which is a base for delta() function.
    """
    def delta(x): 
        return (em_value - x) / em_value + 1
    minimum_length = n * 3 + 5
    if len(xs) >= minimum_length:
        short_list = xs[:minimum_length]  # do not use list as variable name
        em_value = ema(n, short_list)
        em_list = emas(n, short_list[1:])
        delta_list = list(map(delta, em_list))
        steepness = mean(delta_list)
        return steepness
    else:
        return None






if __name__ == '__main__':
    listzzz = [12, 12, 13, 14, 12, 13, 14, 13, 12, 11, 11, 10, 12, 11, 13, 15, 13, 14, 12, 13, 14]

    listbbb = [22.17, 22.4, 23.1, 22.68, 23.33, 23.1, 23.19, 23.65, 23.87, 23.82
                  , 23.63, 23.95, 23.83, 23.75, 24.05, 23.36, 22.61, 22.38, 22.39, 22.15
                  , 22.29, 22.24, 22.43, 22.23, 22.13, 22.18, 22.17, 22.08, 22.19, 22.27]
    print(rsi_calc(14, listbbb*100))
