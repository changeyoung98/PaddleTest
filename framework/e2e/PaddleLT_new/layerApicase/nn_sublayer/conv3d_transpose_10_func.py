import numpy as np
import paddle


class LayerCase(paddle.nn.Layer):
    """
    case名称: conv3d_transpose_10
    api简介: 2维反卷积
    """

    def __init__(self):
        super(LayerCase, self).__init__()

    def forward(self, x, ):
        """
        forward
        """
        out = paddle.nn.functional.conv3d_transpose(x,  weight=paddle.to_tensor(-1 + (1 - -1) * np.random.random([3, 1, 5, 5, 5]).astype('float32'), dtype='float32', stop_gradient=False), stride=1, padding=[[0, 0], [1, 2], [3, 4], [0, 0], [0, 0]], data_format='NDHWC', dilation=1, output_padding=0, groups=1, )
        return out



def create_inputspec(): 
    inputspec = ( 
        paddle.static.InputSpec(shape=(-1, -1, -1, -1, 3), dtype=paddle.float32, stop_gradient=False), 
    )
    return inputspec

def create_tensor_inputs():
    """
    paddle tensor
    """
    inputs = (paddle.to_tensor(-1 + (1 - -1) * np.random.random([2, 8, 8, 8, 3]).astype('float32'), dtype='float32', stop_gradient=False), )
    return inputs


def create_numpy_inputs():
    """
    numpy array
    """
    inputs = (-1 + (1 - -1) * np.random.random([2, 8, 8, 8, 3]).astype('float32'), )
    return inputs

