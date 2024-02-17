import numpy as np


def check(val):
    if type(val) is not Tensor:
        val = Tensor(val)
    return val


def _safe_transpose(arr, axes=None):
    '''
    Safe transpose with predictable behaviour.
    - For 0-2 dimensional tensors: use default behaviour.
    - For >2 dimensional tensors: flip last 2 dimensions.
    '''
    
    if axes is None and arr.ndim > 2:
        axes = [i for i in range(arr.ndim-2)] + [arr.ndim-1, arr.ndim-2]
    
    return np.transpose(arr, axes), axes


def _sum_over_broadcasts(output, initial_shape):
    '''
    "De-broadcasts" outputs from numpy's default broadcasting behaviour for safe gradient addition:
    - If output has same shape as initial shape, return output.
    - Otherwise, reshape output to [-1, ...] where ... is the initial shape, and sum over the 1st axis.
    '''
    if output.shape == initial_shape:
        return output
    
    if type(initial_shape) == int:
        reshaped = np.reshape(output, [-1, initial_shape])
        sum = np.sum(reshaped, axis=0)
        if sum.ndim > 0:
            return sum
        return np.squeeze(sum, axis=0)
    
    # now assume `initial_shape` is an iterable type
    initial_shape = list(initial_shape)
    reshaped = np.reshape(output, [-1]+initial_shape)
    return np.sum(reshaped, axis=0)


class Tensor():
    
    def __init__(self,
                 value,
                 dtype=np.float64,
                 op='init',
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
    
    
    def __len__(self):
        return len(self.value)
    
    
    def __add__(self, other):
        other = check(other)
        
        def _back(output):
            self.grad += _sum_over_broadcasts(output.grad, initial_shape=self.shape)
            other.grad += _sum_over_broadcasts(output.grad, initial_shape=other.shape)
            
        return Tensor(self.value+other.value,
                      op='+',
                      backfunc=_back,
                      children=[self, other])
    
    
    def __sub__(self, other):
        other = check(other)
        
        def _back(output):
            self.grad += _sum_over_broadcasts(output.grad, initial_shape=self.shape)
            other.grad -= _sum_over_broadcasts(output.grad, initial_shape=other.shape)
            
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
            self.grad += _sum_over_broadcasts(output.grad * other.value, initial_shape=self.shape)
            other.grad += _sum_over_broadcasts(output.grad * self.value, initial_shape=other.shape)
            
        return Tensor(self.value*other.value,
                      op='*',
                      backfunc=_back,
                      children=[self, other])
    
    
    def __matmul__(self, other):
        '''
        Matrix multiplication. Behaviour follows
        [numpy convention](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html):
        
        > - If both arguments are 2-D they are multiplied like conventional matrices.
        > - If either argument is N-D, N > 2, it is treated as a stack of matrices residing in the last
            two indexes and broadcast accordingly.
        > - If the first argument is 1-D, it is promoted to a matrix by prepending a 1 to its dimensions.
            After matrix multiplication the prepended 1 is removed.
        > - If the second argument is 1-D, it is promoted to a matrix by appending a 1 to its dimensions.
            After matrix multiplication the appended 1 is removed.
        '''
        other = check(other)
        
        def _back(output):
            if output.ndim == 0:
                # dot product
                self.grad  += output.grad * other.value
                other.grad += output.grad * self.value
            
            elif self.ndim == 1:
                # 1st argument 1d (hence 2nd argument is >=2d, otherwise output will be dot product)
                self_T     = np.expand_dims(self.value, axis=-1)  # for transpose of 1st arg, append dim
                other_T, _ = _safe_transpose(other.value)
                _grad      = np.expand_dims(output.grad, axis=0)  # for 1st arg, prepend dim to gradient
                self.grad  += _sum_over_broadcasts(np.matmul(_grad, other_T),
                                                   initial_shape=self.shape)
                other.grad += np.matmul(self_T, _grad)
            
            elif other.ndim == 1:
                # 2nd argument 1d (hence 1st argument is >=2d, otherwise output will be dot product)
                self_T, _   = _safe_transpose(self.value)
                other_T     = np.expand_dims(other.value, axis=0)  # for transpose of 2nd arg, prepend dim
                _grad       = np.expand_dims(output.grad, axis=-1) # for 2nd arg, append dim to gradient
                self.grad   += np.matmul(_grad, other_T)
                other.grad  += _sum_over_broadcasts(np.matmul(self_T, _grad),
                                                    initial_shape=other.shape)
            
            else:
                # both 1st and 2nd arguments are >=2d
                self_T, _ = _safe_transpose(self.value)
                other_T, _ = _safe_transpose(other.value)
                self.grad += _sum_over_broadcasts(np.matmul(output.grad, other_T),
                                                  initial_shape=self.shape)
                other.grad += _sum_over_broadcasts(np.matmul(self_T, output.grad),
                                                   initial_shape=other.shape)
        
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
            self.grad += _sum_over_broadcasts(output.grad / other.value,
                                              initial_shape=self.shape)
            other.grad += _sum_over_broadcasts(output.grad * (-np.power(other.value, -2)) * self.value,
                                               initial_shape=other.shape)
            
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
        assert val.ndim == 0, "`_fill` only takes in scalar values"
        
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
            self.grad += _sum_over_broadcasts(
                output.grad * other.value * np.power(self.value, power.value-1),
                initial_shape=self.shape
            )
            other.grad += _sum_over_broadcasts(
                output.grad * np.log(self.value) * np.power(self.value, power.value),
                initial_shape=other.shape
            )
            
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
    
    
    
    def copy(self, retain_grad=False, dtype=None):
        if dtype is None:
            dtype = self.dtype
        
        if retain_grad:
            _backfunc = self._backfunc
            _children = self._children
            _grad = self.grad.copy()
        else:
            _backfunc = backfunc=lambda x:None
            _children = []
            _grad = self._zero.copy()
        
        duplicate = Tensor(self.value.copy(),
                           dtype=dtype,
                           op='$',
                           backfunc=_backfunc,
                           children=_children)
        duplicate.grad = _grad
        return duplicate
    
    
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
    
    
    def zero_grad(self):
        self.grad = self._zero
    
    
    def zero_tree(self):
        tree = self._build_tree()
        for node in tree:
            node.grad = node._zero.copy()
    
    
    def collapse_tree(self):
        tree = self._build_tree()
        for node in tree:
            node.grad = node._zero.copy()
            node._backfunc = lambda x:None
            node._children = []
