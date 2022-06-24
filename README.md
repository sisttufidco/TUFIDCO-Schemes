# TUFIDCO_Schemes

1. To install required libraries, type following command in terminal.
```python
pip install -r requirements.txt
```

In smart_selects library, replace the following line in widgets.py, utils.py, form_fields.py file mentioned as below
<br>
<br>

Existing Code
```python
from django.utils.encoding import force_text
```
New Code
```python
from django.utils.encoding import force_str
```
<br>

Similary, in urls.py replace the following lines.

Existing Code
```python
from smart_selects import views
try:
    from django.conf.urls.defaults import url
except ImportError:
    from django.conf.urls import url

urlpatterns = [
    url(r'^all/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<field>[\w\-]+)/(?P<foreign_key_app_name>[\w\-]+)/(?P<foreign_key_model_name>[\w\-]+)/(?P<foreign_key_field_name>[\w\-]+)/(?P<value>[\w\-,]+)/$',  # noqa: E501
        views.filterchain_all, name='chained_filter_all'),
    url(r'^filter/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<field>[\w\-]+)/(?P<foreign_key_app_name>[\w\-]+)/(?P<foreign_key_model_name>[\w\-]+)/(?P<foreign_key_field_name>[\w\-]+)/(?P<value>[\w\-,]+)/$',  # noqa: E501
        views.filterchain, name='chained_filter'),
    url(r'^filter/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<manager>[\w\-]+)/(?P<field>[\w\-]+)/(?P<foreign_key_app_name>[\w\-]+)/(?P<foreign_key_model_name>[\w\-]+)/(?P<foreign_key_field_name>[\w\-]+)/(?P<value>[\w\-,]+)/$',  # noqa: E501
        views.filterchain, name='chained_filter'),
]

```
New Code
```python
from smart_selects import views
try:
    from django.conf.urls.defaults import url
except ImportError:
    from django.urls import re_path

urlpatterns = [
    re_path(r'^all/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<field>[\w\-]+)/(?P<foreign_key_app_name>[\w\-]+)/(?P<foreign_key_model_name>[\w\-]+)/(?P<foreign_key_field_name>[\w\-]+)/(?P<value>[\w\-,]+)/$',  # noqa: E501
        views.filterchain_all, name='chained_filter_all'),
    re_path(r'^filter/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<field>[\w\-]+)/(?P<foreign_key_app_name>[\w\-]+)/(?P<foreign_key_model_name>[\w\-]+)/(?P<foreign_key_field_name>[\w\-]+)/(?P<value>[\w\-,]+)/$',  # noqa: E501
        views.filterchain, name='chained_filter'),
    re_path(r'^filter/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<manager>[\w\-]+)/(?P<field>[\w\-]+)/(?P<foreign_key_app_name>[\w\-]+)/(?P<foreign_key_model_name>[\w\-]+)/(?P<foreign_key_field_name>[\w\-]+)/(?P<value>[\w\-,]+)/$',  # noqa: E501
        views.filterchain, name='chained_filter'),
]
```

2. To start localhost server, in terminal type the following line.

```python
python manage.py runserver
```
3. Server will start on the following port
```python
http://127.0.0.1:8000/
```