from time import time

def timeN(n:int=10, round_to:int=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            start = time()

            for i in range(n):
                output = func(*args)

            elapsed = time() - start

            if output:
                print(f"-------------- Captured return value from function {func.__name__} --------------\n{output}")
            print(f"{func.__name__} took {round(elapsed*1000, round_to)} milliseconds to run {n} times")
        return wrapper
    return decorator
