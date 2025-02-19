import numpy as np
import paddle


class LayerCase(paddle.nn.Layer):
    """
    case名称: ReLU_base
    api简介: ReLU激活层
    """

    def __init__(self):
        super(LayerCase, self).__init__()
        self.func = paddle.nn.ReLU()

    def forward(self, data, ):
        """
        forward
        """
        out = self.func(data, )
        return out


def create_tensor_inputs():
    """
    paddle tensor
    """
    inputs = (paddle.to_tensor(-10 + (10 - -10) * np.random.random([3, 10, 3, 3]).astype('float32'), dtype='float32', stop_gradient=False), )
    return inputs


def create_numpy_inputs():
    """
    numpy array
    """
    inputs = (-10 + (10 - -10) * np.random.random([3, 10, 3, 3]).astype('float32'), )
    return inputs

