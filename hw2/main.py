import numpy as np
from scipy.stats import truncnorm

rng = np.random.Generator(np.random.PCG64())

debug = False


class Meals:
    def __init__(self, mean: int, std: int):
        self.mean = mean
        self.std = std

    def roll_meals_sold(self, size: int = 1):
        return rng.normal(self.mean, self.std, size).round(0)


class Labor:
    def __init__(self, min: int, max: int):
        self.min = min
        self.max = max

    def roll_cost(self, size: int = 1):
        return rng.uniform(self.min, self.max, size)


class Market:
    def __init__(self, meal_prices: list[float], market_probability: list[float]):
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
        return rng.choice(self.meal_price, size, p=self.market_probability)

class Partnership:
    def __init__(self, min: int, max: int, share: float):
        self.min = min
        self.max = max
        self.share = share


class Restaurant:
    def __init__(
        self,
        labor: Labor,
        market: Market,
        meals: Meals,
        cost_per_meal: int,
        non_labor_cost_per_month: int,
        partnership: Partnership,
    ):
        self.labor = labor
        self.market = market
        self.meals = meals
        self.cost_per_meal = cost_per_meal
        self.non_labor_cost_per_month = non_labor_cost_per_month
        self.partnership = partnership

    def simulate(self, months: int = 1, partnership: bool = False):
        # generate numbers for all months at once with roll functions
        meals_sold = self.meals.roll_meals_sold(months)
        labor_costs = self.labor.roll_cost(months)
        market_prices = self.market.roll_market(months)
        # go over each month and calculate profit
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
                elif rev > self.partnership.max:
                    rev = self.partnership.share * self.partnership.max + (1 - self.partnership.share) * rev
            profit.append(rev)
            if debug:
                print(f"Month {i+1}:")
                print(f"Meals sold: {meals_sold[i]}")
                print(f"Market price: ${market_prices[i]}")
                print(f"Labor cost: ${labor_costs[i]}")
                print(f"Profit: ${profit[i]:.2f}\n")
        return profit


def main():
    meals = Meals(mean=3000, std=1000)
    labor = Labor(min=5040, max=6860)
    market = Market(
        meal_prices=[20.00, 18.50, 16.50, 15.00],
        market_probability=[0.25, 0.35, 0.30, 0.10],
    )
    cost_per_meal = 11
    non_labor_cost_per_month = 3995
    partnership = Partnership(min=3500, max=9000, share=0.9)
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
