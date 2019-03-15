## Ddjango_debug_toolbar

> [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html)

### 1. in `local`

- install

```bash
$ pip install django-debug-toolbar
```

- Prerequisites

```python
# settings.py

INSTALLED_APPS = [
    # ...
    'debug_toolbar',
    # ...
]
```

- URLconf

```python
from django.conf import settings
from django.conf.urls import include, url  # For django versions before 2.0
from django.urls import include, path  # For django versions from 2.0 and up

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
```

- Middleware

```python
# settings.py

MIDDLEWARE = [
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ...
]
```

- Internal IPs

```python
# settings.py

INTERNAL_IPS = ('127.0.0.1',)
```

---

### 2. in `c9`

> 아래 추가 사항을 제외한 나머지는 위 local 설정과 동일
>
> https://stackoverflow.com/questions/10517765/django-debug-toolbar-not-showing-up

```python
# settings.py

def show_toolbar(request):
    return True
    
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
}

INTERNAL_IPS = ('0.0.0.0',)
```

