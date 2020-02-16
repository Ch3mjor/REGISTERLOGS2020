from collections import OrderedDict

from django.shortcuts import render
from ipware import get_client_ip
from rest_framework import viewsets
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response

from api.serializers import RequestLogSerializer
from .models import RequestLog


class StandardPageNumberPagination(PageNumberPagination):
    # Standard PageNumberPagination configuration
    page_size = 20
    page_size_query_param = 'page_size'
    serializer_class = RequestLogSerializer
    results_name = 'objects'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            (self.results_name, data),
        ]))


class RequestLogViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = RequestLogSerializer
    pagination_class = StandardPageNumberPagination
    queryset = RequestLog.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        results = self.paginate_queryset(queryset)
        serializer = self.serializer_class(results, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        event = self.get_object()
        serializer = self.serializer_class(event)
        return Response(serializer.data)


@api_view(('GET',))
@renderer_classes((BrowsableAPIRenderer, JSONRenderer))
def log_request(request):
    client_ip, is_routable = get_client_ip(request, proxy_count=1)
    browser = request.user_agent.browser

    log = RequestLog.objects.create(
        ip_addr=client_ip,
        browser=f'{browser.family} {browser.version_string}',
        ctype=request.content_type,
        query=request.query_params.dict(),
    )
    serializer = RequestLogSerializer(log)
    return Response(serializer.data)
