# -*- coding: utf-8 -*-

from collections import namedtuple
try:
    from functools import wraps
except ImportError:
    def wraps(wrapped, assigned=('__module__', '__name__', '__doc__'),
              updated=('__dict__',)):
        def inner(wrapper):
            for attr in assigned:
                setattr(wrapper, attr, getattr(wrapped, attr))
            for attr in updated:
                getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
            return wrapper
        return inner

__all__ = ['route','UrlConf']

UrlConf = namedtuple('UrlConf',['url','name'])

def route(url=None,name=None):
    def resolver(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            return func(*args,**kwargs)
        wrapper._auto_urlconf = UrlConf(url,name)
        return wrapper
    return resolver
