import onnxruntime
import numpy as np
from numpy import array
import os

_data_min_ = array([5., -4., 0., -10.], dtype='float32')
_data_max_ = array([85., 3.5, 19., 9.], dtype='float32')
_onnx_model = onnxruntime.InferenceSession(os.path.join(os.path.dirname(__file__), 'static/model.onnx'))

def form_input(data):
    """格式化输入数据"""
    data = np.asarray(data)
    data = (data - _data_min_) / (_data_max_ - _data_min_)
    return data.reshape(1, -1).astype('float32')

def inference(angel: int, wind: float, dx: float, dy: float) -> float:
    """
    调用深度学习模型推理力度
    Call deep learning model to predict strength.
    :param angel: 角度，为 0 - 180 内的整数
    :param wind: 风力，通常为-10 - 10内的一位浮点数，正数为顺风，负数为逆风
    :param dx: 水平屏距
    :param dy: 垂直屏距，即高差，正数为低打高
    :return: 推理得到的力度
    """
    inputs = form_input([angel, wind, dx, dy])
    ort_inputs = {_onnx_model.get_inputs()[0].name: inputs}
    ort_outs = _onnx_model.run(None, ort_inputs)
    return ort_outs[0][0][0]

