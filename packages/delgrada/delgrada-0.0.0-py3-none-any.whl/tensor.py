import numpy as np


def check(val):
    if type(val) is not Tensor:
        val = Tensor(val)
    return val


def _safe_transpose(arr, axes=None):
    '''
    Safe transpose. Defaults to flipping last 2 dimension for >2 dimensional tensors.
    '''
    
    if axes is None and arr.ndim > 2:
        axes = [i for i in range(arr.ndim)]
        axes[-2], axes[-1] = arr.ndim-1, arr.ndim-2
    
    return np.transpose(arr, axes), axes


class Tensor():
    
    def __init__(self,
                 value,
                 op='init',
                 dtype=np.float64,
                 backfunc=lambda x:None,
                 children=[]):
        
        self.value = np.array(value, dtype=dtype)
        self.dtype = dtype
        self.shape = self.value.shape
        self.ndim  = self.value.ndim
        self.grad  = np.zeros_like(value, dtype=np.float64)
        self._zero = np.zeros_like(value, dtype=np.float64)
        self._backfunc = backfunc
        self._children = children
    
    
    def __str__(self):
        return str(self.value)
    
    
    def __repr__(self):
        old = len('array')
        new = len('Tensor')
        padded_repr = '\n'.join([' '*(new-old) + i for i in repr(self.value).split('\n')])[new:]
        return f"Tensor{padded_repr}"
    
    
    def __add__(self, other):
        other = check(other)
        
        def _back(output):
            self.grad += output.grad
            other.grad += output.grad
            
        return Tensor(self.value+other.value,
                      op='+',
                      backfunc=_back,
                      children=[self, other])
    
    
    def __sub__(self, other):
        other = check(other)
        
        def _back(output):
            self.grad += output.grad
            other.grad -= output.grad
            
        return Tensor(self.value-other.value,
                      op='-',
                      backfunc=_back,
                      children=[self, other])
    
    
    def __neg__(self):
        
        def _back(output):
            self.grad -= output.grad
            
        return Tensor(-self.value,
                      op='n',
                      backfunc=_back,
                      children=[self])
    
    
    def __mul__(self, other):
        '''
        Element-wise multiplication
        '''
        other = check(other)
        
        def _back(output):
            self.grad += output.grad * other.value
            other.grad += output.grad * self.value
            
        return Tensor(self.value*other.value,
                      op='*',
                      backfunc=_back,
                      children=[self, other])
    
    
    def __matmul__(self, other):
        '''
        Matrix multiplication
        '''
        other = check(other)
        
        def _back(output):
            if output.ndim == 0:    # dot product
                self.grad += output.grad * other.value
                other.grad += output.grad * self.value
            else:
                self_T, _ = _safe_transpose(self.value)
                other_T, _ = _safe_transpose(other.value)
                self.grad += np.matmul(output.grad, other_T)
                other.grad += np.matmul(self_T, output.grad)
            
        return Tensor(self.value@other.value,
                      op='@',
                      backfunc=_back,
                      children=[self, other])
    
    
    def __truediv__(self, other):
        '''
        Element-wise division
        '''
        other = check(other)
        
        def _back(output):
            self.grad += output.grad / other.value
            other.grad += output.grad * (-np.power(other.value, -2)) * self.value
            
        return Tensor(self.value/other.value,
                      op='/',
                      backfunc=_back,
                      children=[self, other])
    
    
    def _fill(self, val, dtype=None):
        '''
        New tensor filled with `val` in the same shape as `self`
        '''
        val = check(val)
        if dtype is None: dtype = val.dtype
        assert val.ndim == 0, "`shape_fill` only takes in scalar values"
        
        def _back(output):
            val.grad += np.sum(output.grad)
                
        return Tensor(np.full(self.shape, val.value, dtype=dtype),
                      op='f',
                      backfunc=_back,
                      children=[val])
    
    
    def __pow__(self, other):
        '''
        Raise to power element-wise
        '''
        other = check(other)
        power = self._fill(other) if other.ndim == 0 else other
        
        def _back(output):
            self.grad += output.grad * other.value * np.power(self.value, power.value-1)
            other.grad += output.grad * np.log(self.value) * np.power(self.value, power.value)
            
        return Tensor(np.power(self.value, power.value),
                      op='^',
                      backfunc=_back,
                      children=[self])
    
    
    def __getitem__(self, key):
        def _back(output):
            self.grad[key] += output.grad
            
        return Tensor(self.value[key].copy(),
                      op='[',
                      backfunc=_back,
                      children=[self])
    
    
    def transpose(self, axes=None):
        trans, ax = _safe_transpose(self.value, axes)
        
        def _back(output):
            self.grad += np.transpose(output.grad, ax)
        
        return Tensor(trans,
                      op='T',
                      backfunc=_back,
                      children=[self])
    
    
    def copy(self, dtype=None):
        if dtype is None:
            dtype = self.dtype
        
        return Tensor(self.value.copy(), op='$')
    
    
    def __radd__(self, other):
        other = check(other)
        return other + self
    
    def __rsub__(self, other):
        other = check(other)
        return other - self
    
    def __rmul__(self, other):
        other = check(other)
        return other * self
    
    def __rtruediv__(self, other):
        other = check(other)
        return other / self
    
    def __rpow__(self, other):
        other = check(other)
        return other ** self
    
    
    def _build_tree(self):
        visited = []
        
        def dfs_visit(node):
            if node in visited: return
            for child in node._children:
                dfs_visit(child)
            visited.append(node)
        
        dfs_visit(self)
        
        return reversed(visited)
    
    
    def backprop(self):
        self.grad = np.ones_like(self.value, dtype=np.float64)
        tree = self._build_tree()
        for node in tree:
            node._backfunc(node)
    
    
    def _reset(self):
        tree = self._build_tree()
        for node in tree:
            node.grad = node._zero
    
    
    def _collapse(self):
        tree = self._build_tree()
        for node in tree:
            node.grad = node._zero
            node._backfunc = lambda x:None
            node._children = []
