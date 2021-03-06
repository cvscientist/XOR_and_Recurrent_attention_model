import tensorflow as tf
from ecbm4040.ram.utils import *


class GlimpseNet(object):
    def __init__(self, config, images_ph):
        """
        :param config: a dictionary
        :param images_ph: a tf.placeholder for raw sample image
                     with shape [batch_size, height, width, num_channels]
        """
        super().__init__()

        self.glimpse_win = config.get("glimpse_win", None)
        self.glimpse_scale = config.get("glimpse_scale", None)
        self.loc_dim = config.get("loc_dim", None)
        self.hg_dim = config.get("hg_dim", None)
        self.hl_dim = config.get("hl_dim", None)
        self.g_dim = config.get("g_dim", None)
        self.num_channels = config.get("num_channels", None)

        self.original_imgs = images_ph

        self.init_weights()

    def init_weights(self):
        ####################################################
        # create tf.Variable for weights in GlimpseNet      #
        ####################################################
        win = self.glimpse_win
        scale = self.glimpse_scale
        num_channels = self.num_channels
        loc_dim = self.loc_dim
        hg_dim = self.hg_dim
        hl_dim = self.hl_dim
        g_dim = self.g_dim

        with tf.variable_scope("glimpse", reuse=None):
            self.w_glimpse = weight_variable([win * win * num_channels * scale, hg_dim])
            self.b_glimpse = bias_variable([hg_dim, ])

        with tf.variable_scope("loc", reuse=None):
            self.w_loc = weight_variable([loc_dim, hl_dim])
            self.b_loc = bias_variable([hl_dim, ])

        with tf.variable_scope("hg", reuse=None):
            self.w_hg = weight_variable([hg_dim, g_dim])
            self.b_hg = bias_variable([g_dim, ])

        with tf.variable_scope("hl", reuse=None):
            self.w_hl = weight_variable([hl_dim, g_dim])
            self.b_hl = bias_variable([g_dim, ])

    def glimpse_sensor(self, loc):
        """
        Hint: use "tf.image.extract_glimpse"

        :param loc: a two-component coordinate (x, y) and unlike paper, value of x and y range
               from (-1, 1) here. And the coordinates (-1.0, -1.0) correspond to the upper 
               left corner, the lower right corner is located at (1.0, 1.0) and the center 
               is at (0, 0).
               
        :return glimpse_patches: (batch_size, glimpse_win, glimpse_win, glimpse_scale*num_channels)
        """
        glimpse_patches = None
        glimpse_scale = self.glimpse_scale
        win = self.glimpse_win
        imgs = self.original_imgs
        #############################################
        # TODO: Retina and location encodings        #
        #############################################
        raise NotImplementedError('Please edit this function')

        ###############################################
        #               End of your code.             #
        ###############################################

    def __call__(self, loc):
        """
        Glimpse Network is shown as B) of Figure 1 in the paper.

        And its structure is like,
        hg = ReLU(Linear(flatten_glimpse_patches))
        hl = ReLU(Linear(loc))
        g = ReLU(Linear(hg) + Linear(hl))
        Side Note: think about using CNN(hg) to replace Linear(hg).

        :param loc: coordinates for glimpse sensor with shape (batch_size, loc_dim)

        :param g: glimpse representation with shape (batch_size, g_dim)
        """
        g = None
        win = self.glimpse_win
        scale = self.glimpse_scale
        num_channels = self.num_channels
        batch_size = tf.shape(loc)[0]
        #############################################
        # TODO: Glimpse network                     #
        #############################################
        raise NotImplementedError('Please edit this function.')

        ###############################################
        #               End of your code.             #
        ###############################################


class LocNet(object):
    def __init__(self, config):
        super().__init__()

        self.input_dim = config.get("cell_dim", None)
        self.loc_dim = config.get("loc_dim", None)
        self.loc_std = config.get("loc_std", None)
        self.use_sample = config.get("use_sample", True)

        self.init_weights()

    def init_weights(self):
        self.w = weight_variable([self.input_dim, self.loc_dim])
        self.b = bias_variable([self.loc_dim, ])

    def __call__(self, x):
        """
        A single-layer fully connected network.
    
        Output the coordinate of next glimpse. And the coordinate is sampled from
        a gaussian distribution with an estimated mean and a fixed std.
        
        Here the estimation of the mean is from the output/hidden_state of the core
        RNN network, that is,
        
        mean_t = Linear(h_t).
        
        Then, the next coordinate is sampled from N(mean_t, std).

        :param x: the output/hidden_state of the core RNN network, with shape (batch_size, cell_dim)

        :return loc_mean: mean coordinate of glimpse, (batch_size, loc_dim)
        :return next_loc: next coordinate (x, y) ranging from (-1, 1). Notice that the output of
                    the coordinate should be from -1 to 1.
        """
        loc_dim = self.loc_dim
        loc_std = self.loc_std
        loc_mean, next_loc = None, None
        #############################################
        # TODO: Location network, fl(h) = Linear(h) #
        #############################################
        raise NotImplementedError('Please edit this function.')

        # Hint:
        # First, loc_mean = Linear(h_t)
        # 
        # You can use "tf.random_normal" to sample the next glimpse location
        # Also, when sampling, remenber to use loc_mean and loc_std
        #
        # Avoid loc's values outside range (-1, 1).
        # You can use "tf.clip_by_value" to do that. 

        ###############################################
        #               End of your code.             #
        ###############################################


#############################################
# Output Network: Action Net                 #
#############################################
class ActionNet(object):
    def __init__(self, config):
        super().__init__()

        self.input_dim = config.get("cell_dim", None)
        self.num_classes = config.get("num_classes", None)

        self.init_weights()

    def init_weights(self):
        self.w = weight_variable([self.input_dim, self.num_classes])
        self.b = bias_variable([self.num_classes, ])

    def __call__(self, x):
        """
        In this experiment, we use MNIST digit classification as
        our task for ram, so the action net is a single-layer softmax network. 
        
        But ram, itself, is not restricted to a classification task.
        And in other tasks, this action net will also change. But it will 
        not affect the structure of the core RNN network.

        :param x: the last output/hidden_state of rnn network, with shape (batch_size, cell_dim)

        :return a: xw+b, with shape (batch_size, num_classes)
        :return softmax_a: softmax(a)
        """
        a, softmax_a = None, None
        ######################################
        # TODO: softmax classification.       #
        ######################################
        raise NotImplementedError('Please edit this function.')

        #######################################
        #            End of your code.        #
        #######################################