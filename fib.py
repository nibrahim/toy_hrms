def memoize(fn):
    fn.cache = {}
    def cached_fn(n):
        if n in fn.cache:
            print (f"Returning {n} from cache")
            return fn.cache[n]
        else:
            ret = fn(n)
            fn.cache[n] = ret
            return ret
    return cached_fn

# cache = {}
# def fib(n):
#     if n in cache:
#         print (f"returning {n} from cache")
#         return cache[n]
#     if n <= 1:
#         cache[n] = 1
#         return 1
#     else:
#         ret = fib(n-1) + fib(n-2)
#         cache[n] = ret
#         return ret

@memoize(size=50)
def fib(n):
    if n <= 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

@memoize
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)


# fib = memoize(fib)    
# factorial = memoize(factorial)    
    
@timeout

@retry
def call_api():
    resp = requests.get(...)
    return resp
        
            
import click

parser = click.Parser()

@parser.argument("--init")
def handle_init(args):
    ....

    



