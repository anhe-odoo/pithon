def override( interface_class ) :
    def overrider(method) :
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider

class constant( object ) :
    def __init__(self, func) :
        self.func = func
    def __get__(self, obj, cls) :
        if obj is None :
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value
    def __set__(*args) :
        raise AttributeError("Changing the value of a constant is forbidden")

def abstractmethod( method ) :
    def default_method(*args) :
        raise NotImplementedError('call to abstract method ' + repr(method))
    default_method.__name__ = method.__name__
    return default_method

def accepts(*types):
    def check_accepts(f):
        assert len(types) == f.func_code.co_argcount
        def new_f(*args, **kwds):
            for (a, t) in zip(args, types):
                assert isinstance(a, t), "arg %r does not match %s" % (a,t)
            return f(*args, **kwds)
        new_f.func_name = f.func_name
        return new_f
    return check_accepts

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

class infix_operator( object ) :
    def __init__(self, other = None) :
        self.other = other
    def __or__(self, other) :
        return self(self.other, other)
    def __rshift__(self, other):
        return self(self.other, other)
    def __ror__(self, other) :
        return self.__class__(other)
    def __rlshift__(self, other) :
        return self.__class__(other)

class dot( infix_operator ) :
    @staticmethod
    def __call__(a, b) :
        try : return a.dot(b)
        except :
            try : return b.dot(a)
            except : return sum(x*y for (x,y) in zip(a,b))
    __array_priority__ = 1000

class cross( infix_operator ) :
    @staticmethod
    def __call__(a, b) :
        assert (len(a) == len(b) and len(a) in [2,3])
        return [
            0 if len(a) == 2 else a[1]*b[2]-a[2]*b[1],
            0 if len(a) == 2 else a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0]
        ]
    __array_priority__ = 1000