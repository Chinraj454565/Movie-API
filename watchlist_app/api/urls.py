from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("streamS",views.StreamPlatformVS, basename="StreamUrl")


urlpatterns = [
    path("list/", views.WatchListAV.as_view(), name="watch_list"),
    path("list2/", views.WatchListGV.as_view(), name="watch_list2"),
    
    path("<int:pk>/", views.WatchListDetailAV.as_view(), name="watch_list_details"),
    path("<int:pk>/review-create/",views.ReviewCreate.as_view(), name="review-create"),
    path("<int:pk>/reviews/",views.ReviewList.as_view(), name="review-list"),
    path("user/",views.UserReview.as_view(),name="user-review"),
    path("review/<int:pk>/",views.ReviewDetail.as_view(), name="review-detail"),
    path("", include(router.urls)),
    path("api-auth/",include('rest_framework.urls')),
 
    
    
]

 # path("stream/",views.StreamPlatformAV.as_view(), name="stream_platform"),
    # path("stream/<int:pk>/",views.StreamPlatformDetailAV.as_view(), name="stream_detail"),
    # path("review/",views.ReviewList.as_view(), name="review-list"),
    # path("review/<int:pk>",views.ReviewDetail.as_view(), name="review-detail"),
       # path("api-auth/",include('rest_framework.urls')),