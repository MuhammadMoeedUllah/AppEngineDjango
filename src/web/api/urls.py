from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'dents', views.DentsViewSet)
router.register(r'list_scans', views.ScanViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('scans/', views.ScanPostView.as_view())
]


# curl -X POST "http://127.0.0.1:8000/api/scans/" -H "Content-Type: application/json" -d '{"meta_data": {"scanned_at_utc": "2022-07-11 00:25:00", "scanned_at_local": "2022-07-11 10:25:00", "vehicle_registration": "1AB1CD"}, "dent_data": {"scan_id": null, "size_0_9": 4, "size_10_19": 21, "size_20_29": 34, "size_30_39": 87, "size_40_49": 23, "size_50_59": 42, "size_60_69": 18, "size_70_79": 1, "size_80_89": 3, "size_90_100": 0, "size_100_plus": 0}}'
