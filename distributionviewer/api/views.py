from django.shortcuts import get_object_or_404
from rest_framework.decorators import (api_view, permission_classes,
                                       renderer_classes)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from .models import CategoryCollection, LogCollection, Metric
from .renderers import MetricsJSONRenderer
from .serializers import (CategoryDistributionSerializer,
                          LogDistributionSerializer, MetricSerializer)


def render_category(dist):
    s = CategoryDistributionSerializer(dist)
    return s.data


def render_log(dist):
    s = LogDistributionSerializer(dist)
    return s.data


@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def distributions(request, metric):
    metric = get_object_or_404(Metric, name=metric)
    qc = CategoryCollection.objects.filter(metric=metric)
    ql = LogCollection.objects.filter(metric=metric)
    data = [render_category(d) for d in qc] + [render_log(d) for d in ql]
    return Response(data[0])


@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([MetricsJSONRenderer])
def metrics(request):
    metrics = Metric.objects.all().order_by('name')
    return Response([MetricSerializer(m).data for m in metrics])
