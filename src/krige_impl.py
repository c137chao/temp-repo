import numpy as np
import scipy.linalg
from scipy.spatial.distance import cdist

import util

# from P.K. Kitanidis, Introduction to Geostatistics: Applications in Hydrogeology, 
# (Cambridge University Press, 1997
def linear_variogram_model(m, d):
    """Linear model, m is [slope, nugget]"""
    slope = float(m[0])
    nugget = float(m[1])
    return slope * d / 2 + nugget


def power_variogram_model(m, d):
    """Power model, m is [scale, exponent, nugget]"""
    scale = float(m[0])
    exponent = float(m[1])
    nugget = float(m[2])
    return scale * d**exponent + nugget


def gaussian_variogram_model(m, d):
    """Gaussian model, m is [psill, range, nugget]"""
    psill = float(m[0])
    range_ = float(m[1])
    nugget = float(m[2])
    return psill * (1.0 - np.exp(-(d**2.0) / (range_ * 4.0 / 7.0) ** 2.0)) + nugget


def exponential_variogram_model(m, d):
    """Exponential model, m is [psill, range, nugget]"""
    psill = float(m[0])
    range_ = float(m[1])
    nugget = float(m[2])
    return psill * (1.0 - np.exp(-d / (range_ / 3.0))) + nugget


def spherical_variogram_model(m, d):
    """Spherical model, m is [psill, range, nugget]"""
    psill = float(m[0])
    range_ = float(m[1])
    nugget = float(m[2])
    return np.piecewise(
        d,
        [d <= range_, d > range_],
        [
            lambda x: psill
            * ((3.0 * x) / (2.0 * range_) - (x**3.0) / (2.0 * range_**3.0))
            + nugget,
            psill + nugget,
        ],
    )

# custom function
# bubble image ? or predo?

# wave
def wave_variogram_model(m, d):
    
    return None

# shut flow
def slug_variogram_model(m, d):
    psill = float(m[0])
    range_ = float(m[1])
    nugget = float(m[2])

    # TODO
    return None

def hole_effect_variogram_model(m, d):
    """Hole Effect model, m is [psill, range, nugget]"""
    psill = float(m[0])
    range_ = float(m[1])
    nugget = float(m[2])
    return (
        psill * (1.0 - (1.0 - d / (range_ / 3.0)) * np.exp(-d / (range_ / 3.0)))
        + nugget
    )

class Kriging:
    # static member
    eps = 1.0e-10  # Cutoff for comparison to zero
    variogram_dict = {
        "linear": linear_variogram_model,
        "power": power_variogram_model,
        "gaussian": gaussian_variogram_model,
        "spherical": spherical_variogram_model,
        "exponential": exponential_variogram_model,
        "hole-effect": hole_effect_variogram_model,
    }

    def __init__(
            self, 
            x, 
            y, 
            z, 
            model='linear',  # linear gaussian, power, ... or custom
            parameters=None,  # such as sill, range and so on
            custom_function=None,
            coordinates_type='euclidean',
            nlags=6, # number of iterators for get matrix
            ):
        self.pseudo_inv = False
        self.pseudo_inv_type = str("pinv")
        if self.pseudo_inv_type not in util.P_INV:
            raise ValueError("err on piv type")

        if model not in self.variogram_dict:
            raise ValueError("undefined model")
        
        self.model = model
        self.exact_values = True
        self.coordinates_type = coordinates_type

        variogram_function = custom_function
        
        if self.model != 'custom':
            variogram_function = self.variogram_dict[self.model]

        if variogram_function is None:
            raise ValueError("un-valid variogram function")
        
        self.variogram_function = variogram_function

        # init x, y, z array for krige
        # x, y, z must like a 1d np arrays
        self.x_data = np.atleast_1d(np.squeeze(np.array(x, copy=True, dtype=np.float64)))
        self.y_data = np.atleast_1d(np.squeeze(np.array(y, copy=True, dtype=np.float64)))
        self.z_data = np.atleast_1d(np.squeeze(np.array(z, copy=True, dtype=np.float64)))

        # cacu distance
        self.x_center = (np.amax(self.x_data) + np.amin(self.x_data)) / 2.0
        self.y_center = (np.amax(self.y_data) + np.amin(self.y_data)) / 2.0
        self.X_ADJUSTED, self.Y_ADJUSTED = util._adjust_for_anisotropy(
            np.vstack((self.x_data, self.y_data)).T, [self.x_center, self.y_center], [1.0], [0],
        ).T


        # TODO: some init else?
        para_list = util._make_variogram_parameter_list(model, parameters)
        nd =  np.vstack((self.X_ADJUSTED, self.Y_ADJUSTED)).T

        (self.lags, self.semivariance, self.parameters) = \
            util._initialize_variogram_model(
                nd, self.z_data, model, para_list, variogram_function, nlags, False, coordinates_type
            )


    def display_variogram_model(self):
        """Displays variogram model with the actual binned data."""
        import matplotlib.pyplot as plt

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(self.lags, self.semivariance, "r*")
        ax.plot(
            self.lags,
            self.variogram_function(self.variogram_model_parameters, self.lags),
            "k-",
        )
        plt.show()
        
    def get_kriging_matrix(self, n):

        xy = np.concatenate(
            (self.X_ADJUSTED[:, np.newaxis]*2, self.Y_ADJUSTED[:, np.newaxis]), axis=1
        )
        d = cdist(xy, xy, "euclidean")
        # d = util.custom_dist(xy, xy, self.z_data)

        a = np.zeros((n + 1, n + 1))
        a[:n, :n] = -self.variogram_function(self.parameters, d)

        np.fill_diagonal(a, 0.0)
        a[n, :] = 1.0
        a[:, n] = 1.0
        a[n, n] = 0.0
        return a

    def execute(
        self,
        style,     # grid, mask or points
        xpoints,   # x_range on grid, such as 250 (125 * 2), 125 is d of pipe
        ypoints,   # y_range on grid, such as 250 (125 * 2)
        mask=None, # specify valid area range, such as circle, not use now
        dist='euclidean', # 
        n_closest_points=None, # size for windows, not use now
    ):

        if style != "grid" and style != "masked" and style != "points":                             
            raise ValueError("style argument must be 'grid', 'points', or 'masked'")

        if n_closest_points is not None and n_closest_points <= 1:
            raise ValueError("n_closest_points has to be at least two!")

        xpts = np.atleast_1d(np.squeeze(np.array(xpoints, copy=True)))
        ypts = np.atleast_1d(np.squeeze(np.array(ypoints, copy=True)))
        n = self.X_ADJUSTED.shape[0]
        nx = xpts.size
        ny = ypts.size
        a = self.get_kriging_matrix(n)

        # if mask is not None:
        #     mask = mask.flatten()

        npt = ny * nx
        grid_x, grid_y = np.meshgrid(xpts, ypts)
        xpts = grid_x.flatten()
        ypts = grid_y.flatten()


        xy_data = np.concatenate((self.X_ADJUSTED[:, np.newaxis], self.Y_ADJUSTED[:, np.newaxis]*1.5), axis=1)
        xy_points = np.concatenate((xpts[:, np.newaxis], ypts[:, np.newaxis]*1.5), axis=1)


        bd = cdist(xy_points, xy_data, dist)
        # bd = cdist(xy_points, xy_data, lambda u, v: print('u:', u, 'v:', v))
        # bd = util.custom_dist(xy_points, xy_data, self.z_data)



        npt = bd.shape[0]
        n = self.X_ADJUSTED.shape[0]
        zero_index = None
        zero_value = False

        # use the desired method to invert the kriging matrix
        if self.pseudo_inv:
            a_inv = util.P_INV[self.pseudo_inv_type](a)
        else:
            a_inv = scipy.linalg.inv(a)

        if np.any(np.absolute(bd) <= self.eps):
            zero_value = True
            zero_index = np.where(np.absolute(bd) <= self.eps)

        b = np.zeros((npt, n + 1, 1))
        b[:, :n, 0] = -self.variogram_function(self.parameters, bd)
        if zero_value and self.exact_values:
            b[zero_index[0], zero_index[1], 0] = 0.0
        b[:, n, 0] = 1.0
        
        # if mask is not None:
        #     mask_b = np.repeat(mask[:, np.newaxis, np.newaxis], n+1, axis=1)
        #     b = np.ma.array(b, mask=mask_b)

        x = np.dot(a_inv, b.reshape((npt, n + 1)).T).reshape((1, n + 1, npt)).T
        zvalues = np.sum(x[:, :n, 0] * self.z_data, axis=1)
        sigmasq = np.sum(x[:, :, 0] * -b[:, :, 0], axis=1)


        zvalues = zvalues.reshape((ny, nx))
        sigmasq = sigmasq.reshape((ny, nx))

        zvalues = np.where(zvalues  > 120, 255, 0)

        # print("total pix:", total_px, ", gas pix:", gas_px)
        return zvalues, sigmasq

