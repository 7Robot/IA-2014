# -*- coding: utf-8 -*-
'''
Created on 27 avr. 2012
'''
import os

def class_loader(path):
    path = os.path.relpath(path, os.getcwd())
    path = os.path.normpath(path)
    classes = []
    files = os.listdir(path)
    
    for f in files:
        fpath   = os.path.join(path,f)
        module_name =  fpath.replace("/", ".")[:-3]
        if (os.path.isfile(fpath) and f.endswith('.py') and f != '__init__.py'):
            mod = __import__(module_name, fromlist=[f[:-3]])
            classes.extend([getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type)])

        elif os.path.isdir(fpath):
            classes.extend(class_loader(fpath))

    return classes

