"""Numpy for scientific computing"""
import numpy as np

# set seed generator
rng = np.random.Generator(np.random.PCG64())

# boolean to toggle console output
debug = False

class Meals:
    """
    A class to store the state of meals sold per month.
    Follows a normal distribution with mean and standard deviation.
    
    Attributes
    ----------
    mean : int
        mean number of meals sold per month
    std : int
        standard deviation of meals sold per month
        
    Methods
    -------
    roll_meals_sold(size: int = 1)
        Returns an array of meals sold each month
    """
    def __init__(self, mean: int, std: int):
        """
        Constructs all the necessary attributes for the Meals object.

        Parameters
        ----------
        mean : int
            mean number of meals sold per month
        std : int
            standard deviation of meals sold per month
        """
        self.mean = mean
        self.std = std

    def roll_meals_sold(self, size: int = 1):
        """
        Returns an array of meals sold each month

        Returns a single value if size is not specified.

        Parameters
        ----------
        size : int, optional
            number of months to simulate, by default 1

        Returnsper
        -------
        np.ndarray
        """
        return rng.normal(self.mean, self.std, size).round(0)


class Labor:
    """
    A class to store the state of labor costs per month.
    Follows a uniform distribution with min and max values.

    Attributes
    ----------
    min : int
        minimum labor cost per month
    max : int
        maximum labor cost per month

    Methods
    -------
    roll_cost(size: int = 1)
        Returns an array of labor costs each month
    """
    def __init__(self, min: int, max: int):
        """
        Constructs all the necessary attributes for the Labor object.

        Parameters
        ----------
        min : int
            minimum labor cost per month
        max : int
            maximum labor cost per month
        """
        self.min = min
        self.max = max

    def roll_cost(self, size: int = 1):
        """
        Returns an array of labor costs each month

        Returns a single value if size is not specified.

        Parameters
        ----------
        size : int, optional
            number of months to simulate, by default 1

        Returns
        -------
        np.ndarray
        """
        return rng.uniform(self.min, self.max, size)


class Market:
    """
    A class to store the state of market prices per month.
    Follows a discrete distribution with meal_prices and market_probability.

    Attributes
    ----------
    meal_prices : list[float]
        list of meal prices
    market_probability : list[float]
        list of probabilities for each meal price
        
    Methods
    -------
    roll_market(size: int = 1)
        Returns an array of market prices each month
    """
    def __init__(self, meal_prices: list[float], market_probability: list[float]):
        """
        Constructs all the necessary attributes for the Market object.

        Parameters
        ----------
        meal_prices : list[float]
            list of meal prices
        market_probability : list[float]
            list of probabilities for each meal price

        Raises
        ------
        ValueError
            if meal_prices and market_probability have different lengths
        ValueError
            if market_probability is not between 0 and 1
        """
        if len(meal_prices) != len(market_probability):
            raise ValueError(
                "meal_prices and market_probability must have the same length."
            )
        for prob in market_probability:
            if prob < 0 or prob > 1:
                raise ValueError("market_probability must be between 0 and 1.")
        self.meal_price = meal_prices
        self.market_probability = market_probability

    def roll_market(self, size: int = 1):
        """
        Returns an array of market prices each month

        Returns a single value if size is not specified.

        Parameters
        ----------
        size : int, optional
            number of months to simulate, by default 1

        Returns
        -------
        np.ndarray
        """
        return rng.choice(self.meal_price, size, p=self.market_probability)

class Partnership:
    """
    A class(struct) to store the values for the partnership deal.

    Attributes
    ----------
    min : int
        minimum profit per month
    threshold : int
        threshold for shares
    share : float
        share of profit above max
    """
    def __init__(self, min: int, threshold: int, share: float):
        """
        Constructs all the necessary attributes for the Partnership object.

        Parameters
        ----------
        min : int
            minimum profit per month
        threshold : int
            threshold for shares
        share : float  
            share of profit above max
        """
        self.min = min
        self.threshold = threshold
        self.share = share


class Restaurant:
    """
    A class to store the state of the restaurant.

    Attributes
    ----------
    labor : Labor
        Labor object to store labor cost state
    market : Market
        Market object to store market price state
    meals : Meals
        Meals object to store meals selling state
    cost_per_meal : int
        cost per meal
    non_labor_cost_per_month : int
        non-labor cost per month
    partnership : Partnership
        Partnership object to store partnership deal details

    Methods
    -------
    simulate(months: int = 1, partnership: bool = False)
        Returns an array of profits each month
    """
    def __init__(
        self,
        labor: Labor,
        market: Market,
        meals: Meals,
        cost_per_meal: int,
        non_labor_cost_per_month: int,
        partnership: Partnership,
    ):
        """
        Constructs all the necessary attributes for the Restaurant object.

        Parameters
        ----------
        labor : Labor
            Labor object to store labor cost state
        market : Market
            Market object to store market price state
        meals : Meals
            Meals object to store meals selling state
        cost_per_meal : int
            cost per meal
        non_labor_cost_per_month : int
            non-labor cost per month
        partnership : Partnership
            Partnership object to store partnership deal details
        """
        self.labor = labor
        self.market = market
        self.meals = meals
        self.cost_per_meal = cost_per_meal
        self.non_labor_cost_per_month = non_labor_cost_per_month
        self.partnership = partnership

    def simulate(self, months: int = 1, partnership: bool = False):
        """
        Returns an array of profits each month

        Returns a single value if months is not specified.
        Pass partnership=True to calculate for partnership deal.
        Prints debug information if global variable debug is True.

        Parameters
        ----------
        months : int, optional
            number of months to simulate, by default 1
        partnership : bool, optional
            whether to calculate for partnership deal, by default False

        Returns
        -------
        np.ndarray
        """
        meals_sold = self.meals.roll_meals_sold(months)
        labor_costs = self.labor.roll_cost(months)
        market_prices = self.market.roll_market(months)
        profit = []
        for i in range(months):
            rev = (
                meals_sold[i] * (market_prices[i] - self.cost_per_meal)
                - self.non_labor_cost_per_month
                - labor_costs[i]
            )
            if partnership:
                if rev < self.partnership.min:
                    rev = self.partnership.min
                elif rev > self.partnership.threshold:
                    rev = self.partnership.share * self.partnership.threshold + (1 - self.partnership.share) * rev
            profit.append(rev)
            if debug:
                print(f"Month {i+1}:")
                print(f"Meals sold: {meals_sold[i]}")
                print(f"Market price: ${market_prices[i]}")
                print(f"Labor cost: ${labor_costs[i]}")
                print(f"Profit: ${profit[i]:.2f}\n")
        return profit


def main():
    """
    Main function to run the simulation.
    
    Asks for user input for number of simulations, debug mode, and partnership deal.
    Prints average profit.
    """
    meals = Meals(mean=3000, std=1000)
    labor = Labor(min=5040, max=6860)
    market = Market(
        meal_prices=[20.00, 18.50, 16.50, 15.00],
        market_probability=[0.25, 0.35, 0.30, 0.10],
    )
    cost_per_meal = 11
    non_labor_cost_per_month = 3995
    partnership = Partnership(min=3500, threshold=9000, share=0.9)
    restaurant = Restaurant(
        labor, market, meals, cost_per_meal, non_labor_cost_per_month, partnership
    )
    global debug
    debug = input("Debug mode? (y/n): ").lower() == "y"
    partnership = input("Partnership? (y/n): ").lower() == "y"
    n = int(input("Enter number of simulations: "))
    profit = restaurant.simulate(n, partnership=partnership)
    print(f"Average profit: ${np.mean(profit):.2f}")


if __name__ == "__main__":
    main()
