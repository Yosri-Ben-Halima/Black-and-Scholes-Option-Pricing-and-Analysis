### **Black-Scholes Formula - Brief Summary**

The Black-Scholes formula is a mathematical model used for pricing European call and put options. It was developed by Fischer Black, Myron Scholes, and Robert Merton in 1973.

#### **Formula for a European Call Option:**

$$
C = S_0 N(d_1) - K e^{-rT} N(d_2)
$$

#### **Formula for a European Put Option:**

$$
P = K e^{-rT} N(-d_2) - S_0 N(-d_1)
$$

#### **Where:**

- $C$ = Price of the European call option
- $P$ = Price of the European put option
- $S_0$ = Current price of the underlying asset (e.g., stock)
- $K$ = Strike price of the option
- $T$ = Time to expiration (in years)
- $r$ = Risk-free interest rate (continuously compounded)
- $\sigma$ = Volatility of the underlying asset (standard deviation of the asset's returns)
- $N(\cdot)$ = Cumulative distribution function of the standard normal distribution (i.e., the probability that a standard normal variable is less than or equal to the argument)
- $d_1$ and $d_2$ are intermediate calculations defined as:

$$
d_1 = \frac{\ln\left(\frac{S_0}{K}\right) + \left(r + \frac{\sigma^2}{2}\right)T}{\sigma \sqrt{T}}
$$

$$
d_2 = d_1 - \sigma \sqrt{T}
$$

#### **Key Insights:**

- The formula provides a theoretical estimate of the price of European options, assuming the underlying asset follows a geometric Brownian motion with constant volatility and interest rates.
- **No Arbitrage:** The model is built on the assumption that there are no arbitrage opportunities in the market.
- **Hedging:** The delta of the option (i.e., $N(d_1)$) is used to hedge the option by maintaining a risk-free portfolio.
- **Limitations:** The Black-Scholes model assumes constant volatility and interest rates, which may not hold in real-world markets, leading to model inaccuracies for some options.

The Black-Scholes formula revolutionized financial markets by providing a simple and widely accepted method for option pricing, and it remains a foundational tool in quantitative finance.
