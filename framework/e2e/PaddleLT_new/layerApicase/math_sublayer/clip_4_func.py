import numpy as np
import paddle


class LayerCase(paddle.nn.Layer):
    """
    case名称: clip_4
    api简介: 向上取整运算函数
    """

    def __init__(self):
        super(LayerCase, self).__init__()

    def forward(self, x, ):
        """
        forward
        """
        out = paddle.clip(x,  min=2.0, max=2.0, )
        return out


def create_tensor_inputs():
    """
    paddle tensor
    """
    inputs = ()
    return inputs


def create_numpy_inputs():
    """
    numpy array
    """
    inputs = (paddle.to_tensor([-10, 3, 0], dtype='float32', stop_gradient=False), )
    return inputs
