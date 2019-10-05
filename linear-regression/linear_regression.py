import numpy as np
import pandas as pd

# It is beforehandedly known that the downtown location is
TOWN_CENTER = [1.43, 0.63] # x = 1.43 km and y = 0.63 km

# Script estimates house prices by first creating a linear regression model
# by using the data in input_data file and then it uses the learnt model to given params
# @params: [ area, construction year, room number, floor amount, x-coord., y-coord. ]
# @return: price estimate
def estimate_price(params):
    # Create model from the Excel data.
    df = pd.read_excel("input_data.xlsx", sheet_name="Sheet1")
    y  = df['Price']             # price (€)
    x1 = df['Area']              # living space (m2)
    x2 = df['Construction Year'] # construction year
    x3 = df['Number of Rooms']   # room count (int)
    x4 = df['Floor']             # floor number
    x5 = df['X coordinate']      # x-location of the house
    x6 = df['Y coordinate']      # y-location of the house
    x7 = np.sqrt((x5-TOWN_CENTER[0])**2 + (x6-TOWN_CENTER[1])**2) # distance to downtown

    ones = np.ones(len(x1))
    X_T = np.matrix([ones, x1, x2, x3, x4, x7])
    X = X_T.T # feature rows to columns like they should be...
    b = np.linalg.inv(X_T @ X) @ X_T @ y # inv(X'*X)*X'*y;

    distance_to_downtown = np.sqrt((params[4]-TOWN_CENTER[0])**2 + (params[5]-TOWN_CENTER[1])**2)
    parameters = [1, params[0], params[1], params[2], params[3], distance_to_downtown]
    estimate = parameters @ b # y = b0 + b1*x1 + b2*x2 ...
    return estimate


params = [69, 2010, 4, 10, 1.38727463782683, 0.522109940800501]
estimate = estimate_price(params)
print("price estimate: {:.2f}€".format(estimate))


