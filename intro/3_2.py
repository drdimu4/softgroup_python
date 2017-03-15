import os
def func(dir):
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):
            print (path)
        else:
            func(path)
func("E:\python_projects")