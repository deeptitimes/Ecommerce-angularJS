from rest_framework import routers
from . import views as api_views

router = routers.DefaultRouter()
router.register('info', api_views.CompanyInfo, "company-information"),
urlpatterns = router.urls