from ransac import ransac2d
import matplotlib.pyplot as plt
import numpy as np
import csv

# Loads example xy-point data from the csv-file
def load_data():
    points = []
    with open('points.csv') as csv_file:
        input_data = csv.reader(csv_file, delimiter=',', quotechar='"')
        x = next(input_data)
        y = next(input_data)
    points = np.array([x, y], np.float)
    return points

if __name__ == "__main__":
    points = load_data()

    # Plot the input data
    plt.scatter(points[0,:], points[1,:], marker='x', color='k')
    plt.xlim((0, 100)); plt.ylim((0, 100))

    # Run RANSAC
    N = 100 # iterations
    t = 3   # distance margin for inliers
    d = 5   # inliers needed for good fit
    m, b = ransac2d(points, t, N, d)

    # Plot the result line
    # +/-15 to make the line look continuous in the plot view
    X = np.linspace(min(points[0,:])-15, max(points[0,:])+15, 100)
    y = m*X+b
    plt.plot(X, y, 'r')
    plt.title('Robust line fitting using RANSAC')
    plt.show()
