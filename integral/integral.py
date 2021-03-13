import matplotlib.pyplot as plt
import numpy as np

PI  = np.pi
PI2 = (2*PI)

# Calculus says:
# 1) integral of sin(x) from  0  to pi   equals  2,
# 2) integral of sin(x) from  pi to 2pi  equals -2,
# 3) integral of cos(x) from  0  to pi/2 equals  1,
# 4) integral of cos(x) from  0  to 2pi  equals  0,
# 5) integral of 2*sin(4x) * cos(x) from 0 to pi equals ~1.067
# We can use these results to verify if the logic below works.
# Since computations are discrete, the result will not be exactly
# the same, but should be still close to the analytical solution...


# dt: step size
# start: first point on x-axle (optional)
# end: last point on x-axle (optional)
# f: frequency (optional)
# A: amplitude (optional)
def createSineWave(dt, start=0.0, end=PI2, f=1, A=1):
    x = np.arange(start, end, dt)
    y = A * np.sin(x * f)
    return y, x

def createCosineWave(dt, start=0.0, end=PI2):
    x = np.arange(start, end, dt)
    y = np.cos(x)
    return y, x

# Computes definite integrals of sin and cos
# y (array of floats): function to integrate
# dt (float): step-size. Smaller step yields better results
def getDefiniteIntegral(y, dt):
    integral = 0.0
    for t in range(len(y)):
        integral += y[t] * dt
    return integral

def test():
    dt = 0.001
    y, x = createSineWave(dt, end=PI)
    ans1 = getDefiniteIntegral(y, dt)
    print("ans1:", ans1)

    y, x = createSineWave(dt, start=PI, end=PI2)
    ans2 = getDefiniteIntegral(y, dt)
    print("ans2:", ans2)

    y, x = createCosineWave(dt, end=PI/2)
    ans3 = getDefiniteIntegral(y, dt)
    print("ans3:", ans3)

    y, x = createCosineWave(dt, end=PI2)
    ans4 = getDefiniteIntegral(y, dt)
    print("ans4:", ans4)

    y1, x = createSineWave(dt, A=2, f=4, end=PI)
    y2, x = createCosineWave(dt, end=PI)
    y = y1 * y2 # y = 2*sin(4t) * cos(t)
    ans5 = getDefiniteIntegral(y, dt)
    print("ans5:", ans5) 

    # Plot the 5th graph
    plt.plot(x, y1, label='2sin(4t)')
    plt.plot(x, y2, label='cos(t)')
    plt.plot(x, y, label='2sin(4t)cos(t)')
    plt.legend(loc='lower left')
    plt.show()

# This function can be used to check whether the given function is sine or cosine
def isCosine(y):
    maximum = max(y) # TODO: optimization, pick first max. No need
    minimum = min(y) # to scan whole array, because its periodic
    middle = (maximum - minimum) / 2 + minimum
    if abs(middle - y[0]) < (abs(maximum - y[0]) or abs(minimum - y[0])):
        return False # Add minus if calculating indefinite integral
    return True


if __name__ == "__main__":
    test()