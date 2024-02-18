from enum import Enum
import matplotlib.pyplot as plt
from .lpStateVar import LPStateVar

def plot_sum(var1:LPStateVar,var2:LPStateVar,name=''):
    if var1.result is None or var2.result is None:
        print('Es muss zunächst die Optimierung durchgeführt werden')
        return
    summe = var1.result - var2.result
    plt.plot(summe)
    plt.title(name)
    plt.ylabel(var1.unit)
    plt.xlabel('steps')
    plt.show()