from django.conf.urls import url, include
from . import views
# from rest_framework import routers

# router = routers.SimpleRouter()
# router.register(r'views', UserViewSet)

# urlpatterns = router.urls

urlpatterns = [
    url(r'^$', views.index),
    url(r'^price/', views.price),
    # url(r'^price/(?P<c_from>\w{1,50})/(?P<c_to>\w{1,50})$', views.exchange),
    url(r'^exchange/$', views.exchange), # for method post
    url(r'^exchange/(?P<c_from>\w{1,50})/(?P<c_to>\w{1,50})$', views.exchange), # for method delete

]