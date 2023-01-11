from django.urls import include, path
# import routers
from rest_framework import routers
 
# import everything from views
from .views import *
 
# define the router
router = routers.DefaultRouter()

router.register(r'logs', LogsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]
