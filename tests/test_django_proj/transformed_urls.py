# -*- coding: utf-8 -*-
from autoroute import Inspector
def transformer(url):
    return url.replace('views/','')

urlpatterns = Inspector(transformer=transformer).run()
