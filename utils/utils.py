import time

def timed_loop(countdown=21, repetitions=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(repetitions):
                print(f"pass: {i}")
                result = func(*args, **kwargs)
                
                for remaining in range(countdown, 0, -1):
                    print(f"{remaining} s", end="\r")
                    time.sleep(1)
                
                
            
            return result
        return wrapper
    return decorator
    