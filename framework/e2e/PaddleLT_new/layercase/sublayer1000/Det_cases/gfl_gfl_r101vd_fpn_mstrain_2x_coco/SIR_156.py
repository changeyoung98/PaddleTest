# method:__rmul__||method:__mul__||method:sum||method:__truediv__
import paddle
import unittest
import numpy as np


class LayerCase(paddle.nn.Layer):
    def __init__(self):
        super().__init__()
    def forward(
        self,
        var_0,    # (shape: [551], dtype: paddle.float32, stop_gradient: False)
        var_1,    # (shape: [551], dtype: paddle.float32, stop_gradient: True)
        var_2,    # (shape: [], dtype: paddle.int64, stop_gradient: True)
    ):
        var_3 = var_0.__rmul__(1.0)
        var_4 = var_3.__mul__(var_1)
        var_5 = var_4.sum()
        var_6 = var_5.__truediv__(var_2)
        return var_6



def create_inputspec(): 
    inputspec = ( 
        paddle.static.InputSpec(shape=(-1,), dtype=paddle.float32, stop_gradient=False), 
        paddle.static.InputSpec(shape=(-1,), dtype=paddle.float32, stop_gradient=False), 
        paddle.static.InputSpec(shape=(-1,), dtype=paddle.int64, stop_gradient=False), 
    )
    return inputspec

def create_tensor_inputs():
    inputs = (
        paddle.rand(shape=[551], dtype=paddle.float32),
        paddle.rand(shape=[551], dtype=paddle.float32),
        paddle.randint(low=0, high=10, shape=[1], dtype=paddle.int64),
    )
    return inputs


def create_numpy_inputs():
    inputs = (
        np.random.random(size=[551]).astype('float32'),
        np.random.random(size=[551]).astype('float32'),
        np.random.randint(low=0, high=10, size=[1], dtype='int64'),
    )
    return inputs


class TestLayer(unittest.TestCase):
    def setUp(self):
        self.inputs = create_tensor_inputs()
        self.net = LayerCase()
    def train(self, net, to_static, with_prim=False, with_cinn=False):
        if to_static:
            paddle.set_flags({'FLAGS_prim_all': with_prim})
            if with_cinn:
                build_strategy = paddle.static.BuildStrategy()
                build_strategy.build_cinn_pass = True
                net = paddle.jit.to_static(net, build_strategy=build_strategy, full_graph=True)
            else:
                net = paddle.jit.to_static(net, full_graph=True)
        paddle.seed(123)
        outs = net(*self.inputs)
        return outs
    def test_ast_prim_cinn(self):
        st_out = self.train(self.net, to_static=True)
        cinn_out = self.train(self.net, to_static=True, with_prim=True, with_cinn=True)
        for st, cinn in zip(paddle.utils.flatten(st_out), paddle.utils.flatten(cinn_out)):
            np.testing.assert_allclose(st.numpy(), cinn.numpy(), atol=1e-8)


if __name__ == '__main__':
    unittest.main()