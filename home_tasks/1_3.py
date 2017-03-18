def decorator_maker():
    def decorator(function):
        def wrapper(*args, **kwargs):
            try:
                function(*args, **kwargs)
            except ZeroDivisionError as detail:
                print('Exception occurred in func:',detail)
                print('Input args:',*args)
                print('Input kwargs {}'.format(kwargs))
                return None
            except Exception as det:
                print(det)
            else:
                return function(*args,**kwargs)
        return wrapper
    return decorator

@decorator_maker()
def func(x, y, **kwargs):
    return x / y

print(func(10,0,op="division"))