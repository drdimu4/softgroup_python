import html

def writer(s:str):

    def my_decorator(func_to_dec):

        def wrapper(func_arg):
            for char in s:
                if char == 'b':
                    func_arg = html_b(func_arg)
                if char == 'p':
                    func_arg = html_p(func_arg)
                if char == 'i':
                    func_arg = html_i(func_arg)
                if char == 'u':
                    func_arg = html_u(func_arg)

            return func_to_dec(func_arg)

        return wrapper

    return my_decorator

def html_p(s: str) -> str:
    new_s = '<p>{}<p>'.format(s)
    return new_s
def html_b(s: str) -> str:
    new_s = '<b>{}<b>'.format(s)
    return new_s
def html_i(s: str) -> str:
    new_s = '<i>{}<i>'.format(s)
    return new_s
def html_u(s: str) -> str:
    new_s = '<u>{}<u>'.format(s)
    return new_s

@writer('bpx')
def html_printer(s: str) -> str:
    return html.escape(s)

s="I'll give you +++ cash for this -> stuff."
print(html_printer(s))


