
from functools import reduce

from typing import Any, List, Optional
  
def dot(*func):
    def compose(f, g):
        return lambda x : f(g(x))
    return reduce(compose, func, lambda x : x)
    


def mapm(f, xs):
    """ mapm(print, [1,2,3])  """
    for x in xs:
        f(x)
    return True


def maplist(f, xs):
    """ newlist =  maplist(abs, [-1,-2])  """
    return [f(x) for x in xs]




class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)


# print( [1,2,3,4] |z| -4)
z = Infix(lambda xs,i: xs[i] if abs(i) < (l := len(xs)) or -i == l else None)





# xs can be list or tuple
def grab(xs, i:int) -> Optional[Any]:
    if abs(i) < (l := len(xs)) or -i == l :
        return xs[i]
    else:
        return None

def first(lst: List[Any]) -> Optional[Any]:
    if lst:
        return lst[0]
    else:
        return None

def second(lst: List[Any]) -> Optional[Any]:
    if len(lst) > 1:
        return lst[1]
    else:
        return None

def third(lst: List[Any]) -> Optional[Any]:
    if len(lst) > 2:
        return lst[2]
    else:
        return None

def fourth(lst: List[Any]) -> Optional[Any]:
    if len(lst) > 3:
        return lst[3]
    else:
        return None

def fifth(lst: List[Any]) -> Optional[Any]:
    if len(lst) > 4:
        return lst[4]
    else:
        return None


def last(lst: List[Any]) -> Optional[Any]:
    if lst:
        return lst[-1]
    else:
        return None
    
def drop (drop: int, lst: List[Any]) -> List[Any]:
    return lst[drop:]

def drop_take (drop: int, take: int, lst: List[Any]) -> List[Any]:
    list1 = lst[drop:]
    list2 = list1[:take]
    return list2


def take (take: int, lst: List[Any]) -> List[Any]:
    return lst[:take]


