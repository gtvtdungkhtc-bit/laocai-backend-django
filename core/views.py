from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Road, Asset, Project, UserProfile
from .serializers import RoadSerializer, AssetSerializer, ProjectSerializer, UserSerializer
from .permissions import IsAdminOrReadOnly

def health(request):
    return JsonResponse({'status':'ok'})

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username','email','first_name','last_name']
    ordering = ['id']

class RoadViewSet(viewsets.ModelViewSet):
    queryset = Road.objects.all()
    serializer_class = RoadSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['kind','owner_unit','district','commune','status','year']
    search_fields = ['name','code','owner_unit','start','end']
    ordering_fields = ['length_km','bn','bm','year','name']
    ordering = ['name']

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['kind','status','road','road_name']
    search_fields = ['road_name','kind','status','note']
    ordering_fields = ['quantity']
    ordering = ['id']

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['owner','district','commune']
    search_fields = ['name','owner','note']
    ordering_fields = ['total_budget','planned_capital','disbursed','progress_pct','start_date']
    ordering = ['name']

class ImportRoadsView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def post(self, request):
        data = request.data
        if isinstance(data, list):
            objs = [Road(**{{k:v for k,v in item.items() if k in [f.name for f in Road._meta.get_fields()]}}) for item in data]
            Road.objects.all().delete()
            Road.objects.bulk_create(objs)
            return Response({{'inserted': len(objs)}}, status=status.HTTP_201_CREATED)
        return Response({{'detail':'Payload phải là mảng JSON'}}, status=400)

class SummaryView(APIView):
    def get(self, request):
        total_km = Road.objects.aggregate(s=Sum('length_km'))['s'] or 0
        cnt_assets = Asset.objects.count()
        cnt_projects = Project.objects.count()
        by_kind = Road.objects.values('kind').annotate(total_km=Sum('length_km')).order_by('kind')
        by_unit = Road.objects.values('owner_unit').annotate(total_km=Sum('length_km')).order_by('owner_unit')
        return Response({{
            'total_km': float(total_km),
            'assets_count': cnt_assets,
            'projects_count': cnt_projects,
            'km_by_kind': list(by_kind),
            'km_by_owner_unit': list(by_unit),
        }})
