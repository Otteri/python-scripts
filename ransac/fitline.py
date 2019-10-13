from numpy import array
import numpy as np

# Finds eigenvectors and values by doing principal component analysis
# @param data_array: data points (x,y) in column vector
# @return: 2D array of eigenvalues and eigenvectors
def sklearn_pca(data_array):
    from sklearn.decomposition import PCA
    pca = PCA(2)
    pca.fit(data_array)
    eigenvalues = pca.explained_variance_
    eigenvectors = pca.components_.T # .T: to match w/ numpy
    return eigenvalues, eigenvectors

# Does the same as the above function, but without sklearn and PCA
# @param data_array: data points (x,y) in column vector
# @return: 2D array of eigenvalues and eigenvectors
def get_eigenvector(data_array):
    centered_matrix = data_array.T - data_array.T.mean(axis=1)[:, np.newaxis]
    cov = np.dot(centered_matrix, centered_matrix.T)
    eigenvalues, eigenvectors = np.linalg.eig(cov)
    return eigenvalues, eigenvectors

# Often, the eigenvalues and vectors are not given in any particular order,
# because only the magnitudes are intresting. If x is valid eigenvector, so is -x.
# However, the 'sign randomnes' can cause problems with other calculations, so some
# standard representation must be established. This function sorts the eigenvalues
# from the greatest to smallest. The eigenvectors are ordered accordingly too.
def eigen_sort(eigenvalues, eigenvectors):
    idx = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:,idx]
    return eigenvalues, eigenvectors

# Finds a line that fits to given data
# Line is presented in normal form: p = x*cos(theta) + y*sin(theta)
# @param data_array: column vector of data points (x,y)
# @return theta: angle
# @return p: length of perpendicular
def fitline(data_array, pts):
    try:
        _, eigenvectors = eigen_sort(*sklearn_pca(pts))
    except:
        _, eigenvectors = eigen_sort(*get_eigenvector(pts))

    ev1 = np.array(eigenvectors[:,1]) # pick one vector
    theta = -np.arctan2(*ev1)
    ev1_col = np.matrix([*ev1]).T # create column vector
    mean = np.matrix([np.mean(data_array, axis=0)])
    p = mean * ev1_col
    return theta, p

# Note: Instead of finding eigenvectors,
# we could also do fitting by using total least squares (TLS)

