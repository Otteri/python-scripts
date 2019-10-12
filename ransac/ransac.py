import numpy as np
from random import randint
from fitline import fitline

def ransac2d(points, distance_threshold, N, inlier_threshold):
    '''
    RANSAC fits a line to given points. The method is robust and tolerates faulty points.
    @param points: array of data points to be fitted.
    @param distance_threshold: point must be within this threshold to be counted as a inlier
    @param N: number of iterations to be done.
    @param inlier_threshold: amount of inliers needed for fit to be concidered good enough.
    @return m,b: fitted line coefficients (y = mx+b).
    '''
    pts = np.array(points)
    point_count = len(pts[0])
    if N < 1 or point_count < 2:
        raise ValueError("Bad function arguments")
    inlier_counts = np.zeros((N))
    theta_values = np.zeros((N))
    p_values = np.zeros((N))

    for i in range(N):

        # 1) Select two random points
        r1 = np.array(pts[:,randint(0, point_count-1)])
        r2 = np.array(pts[:,randint(0, point_count-1)])
        norm_vec = np.linalg.norm(r2 - r1)
        if norm_vec == 0:
            continue # Unfortunate edge case (selected the same point twice)

        # 2) Hypothesize a model
        direction_vec = (r2 - r1) / norm_vec
        normal_vec = np.column_stack((direction_vec[0], direction_vec[1]))

        # 3) Compute error function (point to line distances)
        r1_pts = np.tile(np.array([r1]).T, (1, point_count))
        distances = np.dot(normal_vec, (pts - r1_pts)).flatten()

        # 4) Select and count the number of inliers
        inlier_idxs = np.argwhere(abs(distances) < distance_threshold)
        inlier_counts[i] = inlier_count = len(inlier_idxs)

        # 5) If count > threshold, then refit, otherwise repeat
        if inlier_count > inlier_threshold:
            inliers = pts[:, inlier_idxs].squeeze().T
            theta_values[i], p_values[i] = fitline(inliers, pts.T) # TODO: SHOULD BE INLIERS INSTEAD OF ALL PTS

    # Get the best coefficients
    max_inlier_idx = np.argmax(inlier_counts)
    theta = theta_values[max_inlier_idx]
    p = p_values[max_inlier_idx]

    # Convert line's normal form to slope-intercept form
    m, b = normal_to_slope_intercept(theta, p)
    return m, b


# Converts line's normal form coefficients to slope-intercept form
# Normal form: p = x*cos(theta) + y*sin(theta)
# Slope–intercept form: y = m*x+b
def normal_to_slope_intercept(theta, p):
    m = np.tan(theta)
    b = p / np.cos(theta)
    return m, b