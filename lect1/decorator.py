# -*- coding: utf8 -*-

import time

def timer(function):
    def wrapper(*args, **kargs):
        start_time = time.time()
        result = function(*args, **kargs)
        end_time = time.time()
        print( "Execution time: {} ms".format( ( end_time - start_time ) * 1000 ) )
        return result
    return wrapper

def sleeper( delay ):
    def sleeper_(function):
        def wrapper(*args, **kargs):
            time.sleep( delay )
            result = function( *args, **kargs )
            return result
        return wrapper
    return sleeper_

@sleeper(0.5)
@timer
def sum(a,b):
    return a + b

print( sum( 5, 10 ) )

def enum(cls):
    names = getattr( cls, 'names', None )
    for enum, name in enumerate( names ):
        setattr( cls, name, enum )
    return cls

@enum
class Animals():
    names = "cat dog monkey donkey gorilla".split()

animals = Animals()

print( animals.monkey )
print( dir( animals ) )
