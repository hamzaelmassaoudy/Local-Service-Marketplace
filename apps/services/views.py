from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from math import radians, cos, sin, asin, sqrt
from .models import Service, ServiceCategory
from .serializers import ServiceSerializer, ServiceCategorySerializer

# Helper function for distance
def haversine(lon1, lat1, lon2, lat2):
    if lon1 is None or lat1 is None or lon2 is None or lat2 is None:
        return float('inf') 
    
    try:
        lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers
        return c * r
    except (ValueError, TypeError):
        return float('inf')

class ServiceCategoryList(generics.ListAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.AllowAny]

class ServiceCreateView(generics.CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

class ServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # --- UPDATED FILTERSET FIELDS ---
    filterset_fields = ['category__slug', 'is_hourly', 'provider__city']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Service.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Check if user provided coordinates
        user_lat = request.query_params.get('lat')
        user_lng = request.query_params.get('lng')

        if user_lat and user_lng:
            # Calculate distance for every service
            services_with_distance = []
            for service in queryset:
                dist = haversine(service.location_long, service.location_lat, user_lng, user_lat)
                # Attach distance to the object (temporary attribute)
                service.distance = round(dist, 2)
                services_with_distance.append(service)
            
            # Sort by distance (smallest to largest)
            queryset = sorted(services_with_distance, key=lambda s: s.distance)
        
        # Serialize
        serializer = self.get_serializer(queryset, many=True)
        
        # If we calculated distances, inject them into the response data
        if user_lat and user_lng:
            for i, service_data in enumerate(serializer.data):
                dist = queryset[i].distance
                if dist != float('inf'):
                    service_data['distance_km'] = dist

        return Response(serializer.data)

class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ensure users can only edit/delete their OWN services
        return Service.objects.filter(provider__user=self.request.user)