def decorator(function):
    def wrapper(*args, **kwargs):
        try:
            function(*args, **kwargs)
        except ZeroDivisionError as detail:
            print('Exception occurred in func:',detail)
            print('Input args {}'.format(args))
            print('Input kwargs {}'.format(kwargs))
            return None
        else:
            return function(*args,**kwargs)
    return wrapper


@decorator
def func(x, y, **kwargs):
    return x / y

print(func(10,0,op="division"))