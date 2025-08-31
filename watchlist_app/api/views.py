from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from django.shortcuts import get_object_or_404 
# from rest_framework.decorators import api_view
from rest_framework.views import APIView 
from rest_framework import generics
from rest_framework import mixins
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializers, StreamPlatformSerializers, ReviewSerializer
from rest_framework.exceptions import ValidationError
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from rest_framework.permissions import IsAuthenticated
# from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle
from watchlist_app.api.throttling import ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlist_app.api.pagination import WatchListPagenumberPagination, WatchListLOpagination, WatchListCPagination


class WatchListGV(generics.ListAPIView):
    serializer_class=WatchListSerializers
    queryset=WatchList.objects.all()
    permission_classes=[IsAuthenticated]
    pagination_class=WatchListCPagination
    # filter_backends=[filters.OrderingFilter]
    # ordering_fields=['avg_rating']
    


class ReviewCreate(generics.CreateAPIView):
    serializer_class=ReviewSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk=self.kwargs['pk']
        watchlist=WatchList.objects.get(pk=pk)
        review_user=self.request.user
        review_queryset=Review.objects.filter(watchlist=watchlist,review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed")
        if watchlist.avg_rating==0:
            watchlist.avg_rating=serializer.validated_data.get("rating")
        else:
            watchlist.avg_rating=(watchlist.avg_rating + serializer.validated_data.get("rating"))/2
        watchlist.number_rating=watchlist.number_rating + 1 
        watchlist.save()
        serializer.save(watchlist=watchlist, review_user=review_user)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[IsReviewUserOrReadOnly]
    # throttle_classes=[UserRateThrottle]
    
class ReviewList(generics.ListAPIView):
    # queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[permissions.IsAuthenticated]
    throttle_classes=[ReviewListThrottle]
    
    def get_queryset(self):
        pk=self.kwargs['pk']
        #it get modify by django_filters
        return Review.objects.filter(watchlist=pk)
    
    
class UserReview(generics.ListAPIView):
    # queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[permissions.IsAuthenticated]
    # throttle_classes=[ReviewListThrottle]
    
    def get_queryset(self):
        # pk=self.kwargs['pk']
        #it get modify by django_filters
        username=self.request.query_params.get('username',None)
        return Review.objects.filter(review_user__username=username)
    
# class ReviewDetail(generics.GenericAPIView,mixins.RetrieveModelMixin):
#     queryset=Review.objects.all()
#     serializer_class=ReviewSerializer
#     def get(self, request, *args, **kwargs): 
#         return self.retrieve(request, *args, **kwargs)

# class ReviewList(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
#     queryset=Review.objects.all()
#     serializer_class=ReviewSerializer
    
#     def get(self, request, *args, **kwargs): 
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs): 
#         return self.create(request, *args, **kwargs)
class StreamPlatformVS(viewsets.ModelViewSet):
    permission_classes=[IsAdminOrReadOnly]
    queryset=StreamPlatform.objects.all()
    serializer_class=StreamPlatformSerializers
    # throttle_classes=[ScopedRateThrottle]
    # throttle_scope="stream-throttle"



# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         platform=StreamPlatform.objects.all()
#         serializer=StreamPlatformSerializers(platform,many=True)
#         return Response(serializer.data)
    
#     def retrieve(self,request,pk=None):
#         platform=get_object_or_404(StreamPlatform,pk=pk)
#         serializer=StreamPlatformSerializers(platform)
#         return Response(serializer.data)
        
    
#     def create(self,request):
#         serializer=StreamPlatformSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
    
#     def update(self, request, pk=None):
#         platform=get_object_or_404(StreamPlatform,pk=pk)
#         serializer=StreamPlatformSerializers(platform,request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)   
    
#     def destroy(self,request,pk=None):
#         platform=get_object_or_404(StreamPlatform,pk=pk)
#         platform.delete()
#         return Response(status=status.HTTP_200_OK)
        
             


# class StreamPlatformAV(APIView):
#     def get(self,request):
#         platform=StreamPlatform.objects.all()
#         serializer=StreamPlatformSerializers(platform,many=True)
#         return Response(serializer.data)
    
#     def post(self,request):
#         serializer=StreamPlatformSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
# class StreamPlatformDetailAV(APIView):
#     def get(self,request,pk):
#         try:
#             stream=StreamPlatform.objects.get(pk=pk)
#         except Exception as e:
#             return  Response({"error":"not exist"}, status=status.HTTP_404_NOT_FOUND)
#         serializer=StreamPlatformSerializers(stream)
#         return Response(serializer.data)
    
#     def put(self,request,pk):
#         stream=StreamPlatform.objects.get(pk=pk)
#         serializer=StreamPlatformSerializers(stream,request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        
    
#     def delete(self,request,pk):
#         stream=StreamPlatform.objects.get(pk=pk)
#         stream.delete()
#         Response({"delete":"successfull"},staus=status.HTTP_200_OK)

class WatchListAV(APIView):
    permission_classes=[IsAdminOrReadOnly]
    def get(self,request):
        watchlist=WatchList.objects.all()
        serializer=WatchListSerializers(watchlist,many=True,context={'request':request})
        return Response(serializer.data)
        
    
    def post(self,request):
        serializer=WatchListSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    
        
    
   
    
class WatchListDetailAV(APIView):
    permission_classes=[IsAdminOrReadOnly]
    def get(self,request,pk):
        try:
            watchlist=WatchList.objects.get(pk=pk)
        except Exception as e:
            return  Response({"error":"not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer=WatchListSerializers(watchlist)
        return Response(serializer.data)
    
    def put(self,request,pk):
        watchlist=WatchList.objects.get(pk=pk)
        serializer=WatchListSerializers(watchlist,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        
    
    def delete(self,request,pk):
        watchlist=WatchList.objects.get(pk=pk)
        watchlist.delete()
        Response({"delete":"successfull"},staus=status.HTTP_200_OK)

# @api_view(['GET','POST',])
# def movie_list(request):
#     if request.method=='GET':
#         movies=Movie.objects.all()
#         serializer=MovieSerializers(movies, many=True)
#         return Response(serializer.data)
    
#     if request.method=='POST':
#         serializer=MovieSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        
#         return Response(serializer.errors)
    
# @api_view(['GET','PUT','DELETE'])    
# def movie_details(request,pk):
#     if request.method=='GET':
#         try:
#             movie=Movie.objects.get(pk=pk)
#         except Exception as e:
#             return  Response({"error":"not exist"}, status=status.HTTP_404_NOT_FOUND)
#         serializer=MovieSerializers(movie)
#         return Response(serializer.data)
    
#     if request.method=='PUT':
#         movie=Movie.objects.get(pk=pk)
#         serializer=MovieSerializers(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    
#     if request.method=='DELETE':
#         movie=Movie.objects.get(pk=pk)
#         movie.delete()
#         Response({"delete":"successfull"},staus=status.HTTP_200_OK)