from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Song
from rest_framework.pagination import PageNumberPagination
from .serializers import DetailedSongSerializer, SongSerializer
from albums.models import Album
from rest_framework.generics import ListCreateAPIView
import ipdb


class SongView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        """
        Obtençao de musicas
        """
        songs = Song.objects.filter(album_id=pk)

        result_page = self.paginate_queryset(songs, request)
        serializer = SongSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request, pk):
        """
        Criaçao de musica
        """
        album = get_object_or_404(Album, pk=pk)

        serializer = SongSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(album=album)

        return Response(serializer.data, status.HTTP_201_CREATED)


class SongView(ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        album = get_object_or_404(Album, pk=self.kwargs["pk"])
        # ipdb.set_trace()
        serializer.save(album=album)

    # def get_serializer_class(self):
    #     if self.request.method == "POST":
    #         return DetailedSongSerializer
    #     return SongSerializer
