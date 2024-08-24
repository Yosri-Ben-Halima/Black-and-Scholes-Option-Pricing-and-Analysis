import unittest
from EuropeanOption import EuropeanOption  

class TestEuropeanOption(unittest.TestCase):

    def setUp(self):
        """Set up the test case."""
        self.option_call = EuropeanOption(S0=100, K=100, T=1, r=0.05, sigma=0.2, type='call')
        self.option_put = EuropeanOption(S0=100, K=100, T=1, r=0.05, sigma=0.2, type='put')

    def test_initialization(self):
        """Test initialization of EuropeanOption class."""
        self.assertEqual(self.option_call.S0, 100)
        self.assertEqual(self.option_call.K, 100)
        self.assertEqual(self.option_call.T, 1)
        self.assertEqual(self.option_call.r, 0.05)
        self.assertEqual(self.option_call.sigma, 0.2)
        self.assertEqual(self.option_call.type, 'call')
        self.assertAlmostEqual(self.option_call.price, 10.45, places=1)  

    def test_black_and_scholes_call(self):
        """Test Black-Scholes calculation for call option."""
        expected_price = 10.45  
        self.assertAlmostEqual(self.option_call.price, expected_price, places=1)

    def test_black_and_scholes_put(self):
        """Test Black-Scholes calculation for put option."""
        expected_price = 5.57  
        self.assertAlmostEqual(self.option_put.price, expected_price, places=1)

    def test_setters(self):
        """Test setters and the price update."""
        self.option_call.S0 = 110
        self.assertNotEqual(self.option_call.price, 10.45)
        self.option_call.K = 105
        self.assertNotEqual(self.option_call.price, 10.45)
        self.option_call.T = 0.5
        self.assertNotEqual(self.option_call.price, 10.45)
        self.option_call.r = 0.03
        self.assertNotEqual(self.option_call.price, 10.45)
        self.option_call.sigma = 0.3
        self.assertNotEqual(self.option_call.price, 10.45)
        self.option_call.type = 'put'
        self.assertAlmostEqual(self.option_call.price, 6.10, places=1) 

    def test_invalid_option_type(self):
        """Test invalid option type."""
        with self.assertRaises(ValueError):
            self.option_call.type = 'invalid'

    def test_repr(self):
        """Test the __repr__ method."""
        expected_repr = "European call option | S0 = $100 | K = $100 | T = 1 year | r = 5.0% | sigma = 20.0% | C = $10.45"
        self.assertEqual(repr(self.option_call), expected_repr)

if __name__ == '__main__':
    unittest.main()
