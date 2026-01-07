from django.urls import path
from .views import DemoRestApi, DemoRestApiItem

urlpatterns = [
    path("index/", DemoRestApi.as_view(), name="demo_rest_api_resources"),
    path("<str:item_id>/", DemoRestApiItem.as_view(), name="demo_rest_api_item"),
]
