import numpy as np
import paddle


class LayerCase(paddle.nn.Layer):
    """
    case名称: conv2d_transpose_6
    api简介: 2维反卷积
    """

    def __init__(self):
        super(LayerCase, self).__init__()

    def forward(self, x, ):
        """
        forward
        """
        out = paddle.nn.functional.conv2d_transpose(x,  weight=paddle.to_tensor(-1 + (1 - -1) * np.random.random([6, 1, 3, 3]).astype('float32'), dtype='float32', stop_gradient=False), stride=2, padding=[1, 0], output_padding=1, dilation=1, groups=3, data_format='NHWC', )
        return out


def create_tensor_inputs():
    """
    paddle tensor
    """
    inputs = (paddle.to_tensor(-1 + (1 - -1) * np.random.random([2, 2, 2, 6]).astype('float32'), dtype='float32', stop_gradient=False), )
    return inputs


def create_numpy_inputs():
    """
    numpy array
    """
    inputs = (-1 + (1 - -1) * np.random.random([2, 2, 2, 6]).astype('float32'), )
    return inputs
