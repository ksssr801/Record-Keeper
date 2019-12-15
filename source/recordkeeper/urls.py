from django.conf.urls import url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .views import get_records, dump_data_to_database

router = DefaultRouter()
urlpatterns = router.urls
urlpatterns.append(url(r'record-list', get_records))
urlpatterns.append(url(r'inserting-data-to-db', dump_data_to_database))
# urlpatterns.append(url(r'leave-parking-slot', leave_the_parking_lot))
# urlpatterns.append(url(r'parking-lot-current-status', get_parking_lot_status))
