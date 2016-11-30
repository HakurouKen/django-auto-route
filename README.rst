
An automatically route-generator for django based on file path.

To use autoroute, just run the ``Inspector``:

.. code-block:: python

    from autoroute import Inspector
    urlpatterns = Inspector().run()

Inspector has the following optional params:

- root : the root of the project, using ``SETTINGS.BASE_DIR`` as default.
- style: dash / underscore / camel , default ``dash``.

And then, decorate your view function with ``@route(url,name)``

.. code-block:: python

    from django.http import HttpResponse
    from autoroute import route

    @route()
    def auto_generated(request):
        return HttpResponse("A default auto-generated route")

    @route(name='with-name')
    def with_name(request):
        return HttpResponse("A route with name.")

    @route(url='/custom/',name='custom-name')
    def custom_route(request):
        return HttpResponse("This is a custom route.")

**Note**: The custom url is also based on filepath.
For example , the ``custom_route`` view above will be load as ``/path/to/view/custom/``.
If you want to have the full control of the view, just handle it yourself.

You can see some full demos in tests.
