from api.viewsets import FormsViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register('forms', FormsViewset)

