import numpy as np
from delgrada.tensor import Tensor
from delgrada.tensor import check, _safe_transpose


def shape(t: Tensor):
    return np.shape(t.value)


def transpose(t: Tensor, axes=None):
    trans, ax = _safe_transpose(t.value, axes)
    
    def _back(output):
        t.grad += np.transpose(output.grad, ax)
    
    return Tensor(trans,
                    op='T',
                    backfunc=_back,
                    children=[t])


def full(shape, val, dtype=np.float64):
    val = check(val)
    if dtype is None: dtype = val.dtype
    assert val.ndim == 0, "`full` only takes in scalar values"
    
    def _back(output):
        val.grad += np.sum(output.grad)
            
    return Tensor(np.full(shape, val.value, dtype=dtype),
                  op='f',
                  backfunc=_back,
                  children=[val])


def exp(t: Tensor):
    '''
    Element-wise exponentiation
    '''
    def _back(output):
        t.grad += output.grad * np.exp(t.value)
            
    return Tensor(np.exp(t.value),
                  op='e',
                  backfunc=_back,
                  children=[t])


def log(t: Tensor):
    '''
    Element-wise natural log
    '''
    def _back(output):
        t.grad += output.grad / t.value
            
    return Tensor(np.log(t.value),
                  op='l',
                  backfunc=_back,
                  children=[t])


def sin(t: Tensor):
    '''
    Element-wise sine
    '''
    def _back(output):
        t.grad += output.grad * np.cos(t.value)
            
    return Tensor(np.sin(t.value),
                  op='s',
                  backfunc=_back,
                  children=[t])


def cos(t: Tensor):
    '''
    Element-wise cosine
    '''
    def _back(output):
        t.grad += output.grad * -np.sin(t.value)
            
    return Tensor(np.cos(t.value),
                  op='c',
                  backfunc=_back,
                  children=[t])
