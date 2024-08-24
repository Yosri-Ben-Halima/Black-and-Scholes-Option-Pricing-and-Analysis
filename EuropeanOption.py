from typing import Literal
import numpy as np
from scipy.stats import norm
from scipy.optimize import least_squares
from math import log, exp 

class EuropeanOption:

    def __init__(self, S0: float, K: float, T: float, r: float, sigma: float, type:Literal['call', 'put']) -> None:
        """
        Initiate an Instance of the EuropeanOption class.

        ## Parameters:
        - S0: Current price of the underlying asset (e.g., stock)
        - K: Strike price of the option
        - T: Time to expiration (in years)
        - r: Risk-free interest rate (continuously compounded)
        - sigma: Volatility of the underlying asset (standard deviation of the asset's returns)
        - type: Option type (Call or Put)
        """
        
        self._S0 = S0
        self._K = K
        self._T = T
        self._r = r
        self._sigma = sigma
        self._type = type
        self._price = self.black_and_scholes()

    def black_and_scholes(self) -> float:
        
        """
        Calculate the price of European options.

        ## Parameters:
        - self: Instance of the EuropeanOption.

        ## Returns:
        - float: The theoretical price of the European option according to a Black, Scholes & Merton model.
        """

        d1, d2 = self._d1_d2()
        N = lambda x: norm.cdf(x)

        if self._type.lower() == 'call':
            price = self._S0 * N(d1) - self._K * exp(-self._r * self._T) * N(d2)
        elif self._type.lower() == 'put':
            price = self._K * exp(-self._r * self._T) * N(-d2) - self._S0 * N(-d1)
        else:
            raise ValueError("Option type can only be a Call or a Put.") 
        
        return price
    
    def _d1_d2(self) -> tuple:
        d1 = (log(self._S0 / self._K) + (self._r + self._sigma**2 / 2) * self._T) / (self._sigma * np.sqrt(self._T))
        return d1, d1 - self._sigma * np.sqrt(self._T)
    
    def delta(self) -> float:
        N = norm.cdf
        d1, _ = self._d1_d2()
        if self._type == 'call':
            return N(d1)
        if self._type == 'put':
            return N(d1)-1

    def gamma(self) -> float:
        n = norm.pdf
        d1, _ = self._d1_d2()
        return n(d1)/(self._S0*self._sigma*self._sigma*np.sqrt(self._T))
    
    def vega(self) -> float:
        n = norm.pdf
        d1, _ = self._d1_d2()
        return self._S0*self._sigma*np.sqrt(self._T)*n(d1)     
    
    def theta(self) -> float:
        d1, d2 = self._d1_d2()
        N, n = norm.cdf, norm.pdf
        if self._type == 'call':
            return -self._S0*self._sigma*n(d1)/(2*np.sqrt(self._T)) - self._r*self._K*exp(-self._r*self._T)*N(d2)
        if self._type == 'put':
            return -self._S0*self._sigma*n(d1)/(2*np.sqrt(self._T)) + self._r*self._K*exp(-self._r*self._T)*N(-d2)
        
    def rho(self) -> float:
        _, d2 = self._d1_d2()
        N = norm.cdf
        if self._type == 'call':
            return self._K*self._T*exp(-self._r*self._T)*N(d2)
        if self._type == 'put':
            return -self._K*self._T*exp(-self._r*self._T)*N(-d2)

    @property
    def S0(self) -> float:
        return self._S0

    @property
    def K(self) -> float:
        return self._K

    @property
    def T(self) -> float:
        return self._T

    @property
    def r(self) -> float:
        return self._r

    @property
    def sigma(self) -> float:
        return self._sigma

    @property
    def type(self) -> str:
        return self._type

    @property
    def price(self) -> float:
        return self._price

    @S0.setter
    def S0(self, value: float) -> None:
        self._S0 = value
        self._price = self.black_and_scholes()

    @K.setter
    def K(self, value: float) -> None:
        self._K = value
        self._price = self.black_and_scholes()

    @T.setter
    def T(self, value: float) -> None:
        self._T = value
        self._price = self.black_and_scholes()

    @r.setter
    def r(self, value: float) -> None:
        self._r = value
        self._price = self.black_and_scholes()

    @sigma.setter
    def sigma(self, value: float) -> None:
        self._sigma = value
        self._price = self.black_and_scholes()

    @type.setter
    def type(self, value: Literal['call', 'put']) -> None:
        if value.lower() not in ['call', 'put']:
            raise ValueError("Option type can only be a Call or a Put.")
        self._type = value.lower()
        self._price = self.black_and_scholes()
    
    def __repr__(self) -> str:
        return f"""European {self.type.lower()} option | S0 = ${self.S0} | K = ${self.K} | T = {self.T} {'year' if self.T==1 else 'years'} | r = {self.r*100}% | sigma = {self.sigma*100}% | C = ${self.price:.2f}"""


def implied_volatility(market_price: float, S0: float, K: float, T: float, r: float, type: Literal['call', 'put']) -> float:
    """
    Calculate the implied volatility of an European option using the market price.

    The implied volatility is the volatility value that, when input into the Black-Scholes model, 
    yields the market price of the option. This function uses numerical optimization to find the 
    implied volatility by minimizing the difference between the market price and the option price 
    calculated by the Black-Scholes model.

    ## Parameters:
    - market_price (float): The market price of the European option.
    - S0 (float): Current price of the underlying asset (e.g., stock).
    - K (float): Strike price of the option.
    - T (float): Time to expiration (in years).
    - r (float): Risk-free interest rate (continuously compounded).
    - type (Literal['call', 'put']): Option type ('call' or 'put').

    ## Returns:
    - float: The implied volatility of the European option.

    ## Method:
    The function defines an objective function that calculates the absolute difference between the 
    market price and the price of the European option calculated using the Black-Scholes formula. 
    The `least_squares` function from `scipy.optimize` is then used to minimize this difference by 
    varying the volatility. The optimized volatility is returned as the implied volatility.

    ## Example:
    >>> implied_volatility(market_price=10, S0=100, K=100, T=1, r=0.05, type='call')
    0.252
    """
    obj = lambda sigma: np.abs(market_price - EuropeanOption(S0, K, T, r, sigma, type).price)
    return least_squares(obj, [0.1]).x[0]


