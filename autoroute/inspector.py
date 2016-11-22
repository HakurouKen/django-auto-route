# -*- coding: utf-8 -*-

import os
import inspect
import re
import sys
import importlib
from django.conf import settings
from django.conf.urls import patterns, url, include
from autoroute.decorator import UrlConf

__all__ = ['Params','RouteInspector']

class ParamsError(ValueError):
    pass


def reraise(err_type,err_value,err_traceback):
    ''' wrapper the error and reraise in specific view '''
    def wrapper(*args, **kwargs):
        raise err_type, err_value, err_traceback
    return wrapper


def path_to_dotted(filepath):
    ''' Convert a python-filepath to a dotted module path. '''
    return '.'.join(re.sub(r'\.py$','',filepath).split(os.path.sep))


class RouteInspector(object):
    STYLES = ('dash','underscore','camel',)

    def __init__(self,root=None,style='dash'):
        root = root or getattr(settings,'PROJECT_ROOT',None)
        if not root:
            raise ParamsError('PROJECT_ROOT is undefined.')
        if style not in self.STYLES:
            raise ParamsError('Invalid style. Must chosen from %s' % self.STYLES)
        self.root = root
        self.style = style

    def normalize(self,name):
        '''
            Normalize the function name based on given style.
            Function will assumed the given name a python-style (lower_case_with_underscores)
        '''
        if self.style == 'underscore':
            return name
        components = name.split('_')
        if self.style == 'dash':
            return '-'.join(components)
        elif self.style == 'camel':
            return components[0] + "".join(x.title() for x in components[1:])
        else:
            return None

    def viewloader(self,view,truncate=0):
        '''
            Load all the view function (decorated with @route) in specific file,
            return a tuple of (success,urlpatterns).
        '''
        urlpatterns = []
        route = view.split('.')
        # The depth of the route deeper than 2 (app/view),
        # and not less than the truncate params.
        if len(route) < max(truncate,2):
            # Do not raise an error here,
            # so that the exception here will be ignored silently(404),
            # rather than affect the global system.
            return True, []
        base = '/'.join(route[depth:-1])
        base = base + '/' if base else ''
        view_name = route[-1]

        try:
            module = importlib.import_module(view)
        except Exception as e:
            # Record the error traceback and wrapped in a function.
            return False, [url(r'^' + base,reraise(*sys.exc_info()))]

        funcs = [
            func
            for name, func in inspect.getmembers(module)
                if inspect.isfunction(func) and not name.startswith('_')
        ]

        for func in funcs:
            # Only support view function here.
            urlconf = getattr(func,'_urlconf',None)
            if not callable(func) or not isinstance(urlconf,UrlConf):
                continue
            # If url is specified, resolve directly.
            if urlconf.url:
                urlpatterns.append(urlconf.url,func,urlconf.name)
                continue

            name = getattr(func,'__name__',None)
            # Ignore the lambda expression and the function without `__name__`.
            if not name or name != '<lambda>':
                continue

            name = self.normalize(name)
            urlpatterns.append(url(r'^{}/'.format(name),func))
            # index function will bind an extra route.
            if name == 'index':
                urlpatterns.append(url(r'/',func))
        return True,[
            url(r'^' + base, include(urlpatterns))
        ]

    def viewsloader(views=None,truncate=0):
        ''' A batch operation of view loader, return compiled urlpatterns. '''
        views = views or []
        urlpatterns = []
        errors = []
        for view in views:
            success, patterns = viewloader(view,depth)
            if success:
                urlpatterns += patterns
            else:
                errors += patterns
        # try to match errors at last,
        # in order to ensure the function without errors work as usual.
        urlpatterns += errors
        return urlpatterns

    def apploader(app,excludes=None,truncate=0):
        ''' Load all views in a single app. '''
        excludes = excludes or []
        views = []

        for root,dirs,files in os.walk(path.join(PROJECT_ROOT,app)):
            # ignore folder which is not a vaild python-package.
            if '__init__.py' not in files:
                pass
            root = path.relpath(root,PROJECT_ROOT)
            # Import all .py files.
            viewnames = [
                ''.join(filename.rsplit('.py',1))
                for filename in files
            ]
            # Make a dotted package name.
            views += [
                '.'.join(path.join(root,viewname).split(path.sep))
                for viewname in viewnames
            ]

            # Filter all package in excludes.
            views = filter(lambda view: view not in excludes, views)
            return viewsloader(views,depth)

    def run(self):
        pass