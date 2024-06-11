from django.urls import path
from . import views
urlpatterns=[
    path("",views.search_view,name="search_view"),
    path("addContent",views.add_content_view,name="add_content"),
    
]