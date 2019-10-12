from numpy import array
import numpy as np

# @param data_array: column vector of data points (x,y)
# @return pca_components_: eigenvectors (positives first)
def sklearn_pca(data_array):
  from sklearn.decomposition import PCA
  pca = PCA(2)
  pca.fit(data_array)
  eigenvectors = pca.components_
  return eigenvectors

def get_eigenvector(data_array):
  centered_matrix = data_array.T - data_array.T.mean(axis=1)[:, np.newaxis]
  cov = np.dot(centered_matrix, centered_matrix.T)
  eigenvalues, eigenvectors = np.linalg.eig(cov)

  # linalg gives the eigenvectors in random order, thus the
  # output must be sorted, so the trignometric calculations work
  # TODO: return sorted eigenvector
  return eigenvectors


# Finds a line that fits to the given data points
# p = x*cos(theta) + y*sin(theta)
# @param data_array: column vector of data points (x,y)
# @return theta: angle
# @return p: length of perpendicular
def fitline(data_array, pts): # pts unnecessary?

  #try:
  #  eigenvectors = sklearn_pca(pts)
  #except:
  #  eigenvectors = get_eigenvector(data_array)

  eigenvectors = get_eigenvector(data_array)

  ev1 = np.array(eigenvectors[:,0]) # magnitudes are same, just pick 1st
  #ev1 = ev1[::-1] # flip order
  theta = -np.arctan2(*ev1)
  ev1_c = np.matrix([*ev1]).T # create column vector
  mean = np.matrix([np.mean(data_array, axis=0)])
  p = mean * ev1_c
  return theta, p


# Note: Instead of PCA we could also do fitting by using Total least squares (TLS)

