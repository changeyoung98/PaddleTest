import numpy as np
import paddle


class LayerCase(paddle.nn.Layer):
    """
    case名称: kthvalue_0
    api简介: Tensor的kthvalue求值
    """

    def __init__(self):
        super(LayerCase, self).__init__()

    def forward(self, x, ):
        """
        forward
        """
        out = paddle.kthvalue(x,  k=4, axis=2, )
        return out


def create_tensor_inputs():
    """
    paddle tensor
    """
    inputs = (paddle.to_tensor(-1 + (1 - -1) * np.random.random([5, 3, 4, 4]).astype('float32'), dtype='float32', stop_gradient=False), )
    return inputs


def create_numpy_inputs():
    """
    numpy array
    """
    inputs = (-1 + (1 - -1) * np.random.random([5, 3, 4, 4]).astype('float32'), )
    return inputs
