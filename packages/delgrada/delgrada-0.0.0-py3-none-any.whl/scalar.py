'''
Inspired by Andrej Karpathy's [micrograd](https://github.com/karpathy/micrograd)
'''


import math


def check(val):
    if type(val) is not Scalar:
        val = Scalar(val)
    return val


class Scalar():
    
    def __init__(self,
                 value,
                 op='init',
                 dtype=float,
                 backfunc=lambda x:None,
                 children=[]):
        
        self.value = dtype(value)
        self.dtype = dtype
        self.grad = 0.0
        self._backfunc = backfunc
        self._children = children
    
    
    def __str__(self):
        return str(self.value)
    
    
    def __repr__(self):
        return f'Scalar({repr(self.value)})'
    
    
    def __add__(self, other):
        other = check(other)
        
        def _back(output):
            self.grad += output.grad
            other.grad += output.grad
            
        return Scalar(self.value+other.value,
                      op='+',
                      backfunc=_back,
                      children=[self, other])
    
    
    def __sub__(self, other):
        other = check(other)
        
        def _back(output):
            self.grad += output.grad
            other.grad -= output.grad
            
        return Scalar(self.value-other.value,
                      op='-',
                      backfunc=_back,
                      children=[self, other])
    
    
    def __neg__(self):
        
        def _back(output):
            self.grad -= output.grad
            
        return Scalar(-self.value,
                      op='n',
                      backfunc=_back,
                      children=[self])
    
    
    def __mul__(self, other):
        other = check(other)
        
        def _back(output):
            self.grad += output.grad * other.value
            other.grad += output.grad * self.value
            
        return Scalar(self.value*other.value,
                      op='*',
                      backfunc=_back,
                      children=[self, other])
    
    
    def __truediv__(self, other):
        other = check(other)
        
        def _back(output):
            self.grad += output.grad / other.value
            other.grad += output.grad * (-math.pow(other.value, -2)) * self.value
            
        return Scalar(self.value/other.value,
                      op='/',
                      backfunc=_back,
                      children=[self, other])
    
    
    def __pow__(self, other):
        other = check(other)
        
        def _back(output):
            self.grad += output.grad * other.value * math.pow(self.value, other.value-1)
            other.grad += output.grad * math.log(self.value) * math.pow(self.value, other.value)
            
        return Scalar(math.pow(self.value, other.value),
                      op='^',
                      backfunc=_back,
                      children=[self])
    
    
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
        self.grad = 1
        tree = self._build_tree()
        for node in tree:
            node._backfunc(node)
    
    
    def _reset(self):
        tree = self._build_tree()
        for node in tree:
            node.grad = 0
    
    
    def _burn(self):
        tree = self._build_tree()
        for node in tree:
            node.grad = 0
            node._backfunc = lambda x:None
            node._children = []



def exp(s: Scalar):
    def _back(output):
        s.grad += output.grad * math.exp(s.value)
            
    return Scalar(math.exp(s.value),
                  op='e',
                  backfunc=_back,
                  children=[s])


def log(s: Scalar):
    def _back(output):
        s.grad += output.grad / s.value
            
    return Scalar(math.log(s.value),
                  op='l',
                  backfunc=_back,
                  children=[s])


def sin(s: Scalar):
    def _back(output):
        s.grad += output.grad * math.cos(s.value)
            
    return Scalar(math.sin(s.value),
                  op='s',
                  backfunc=_back,
                  children=[s])


def cos(s: Scalar):
    def _back(output):
        s.grad += output.grad * -math.sin(s.value)
            
    return Scalar(math.cos(s.value),
                  op='c',
                  backfunc=_back,
                  children=[s])
