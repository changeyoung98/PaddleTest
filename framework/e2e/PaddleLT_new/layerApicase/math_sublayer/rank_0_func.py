import numpy as np
import paddle


class LayerCase(paddle.nn.Layer):
    """
    case名称: rank_0
    api简介: 计算输入Tensor的维度（秩）
    """

    def __init__(self):
        super(LayerCase, self).__init__()

    def forward(self, input, ):
        """
        forward
        """
        out = paddle.rank(input,  )
        return out



def create_inputspec(): 
    inputspec = ( 
        paddle.static.InputSpec(shape=(-1, -1), dtype=paddle.int32, stop_gradient=True), 
    )
    return inputspec

def create_tensor_inputs():
    """
    paddle tensor
    """
    inputs = (paddle.to_tensor([[6, 4], [0, 0]], dtype='int32', stop_gradient=False), )
    return inputs


def create_numpy_inputs():
    """
    numpy array
    """
    inputs = (np.array([[6, 4], [0, 0]]).astype('int32'), )
    return inputs

