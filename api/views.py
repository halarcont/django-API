from venv import logger
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Item
from .serializers import ItemSerializer
from api import serializers

@api_view(['GET'])
def ApiOverview(request):
    """
    Vista de API que proporciona una descripción general de las rutas de la API disponibles.

    Parámetros:
    request (HttpRequest): El objeto de solicitud HTTP.

    Retorna:
    Response: Un objeto de respuesta HTTP con las rutas de la API.
    """
    api_urls = {
        'all_items': '/',
        'Search by Category': '/?category=category_name',
        'Search by Subcategory': '/?subcategory=category_name',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
    }
    return Response(api_urls)

@api_view(['POST'])
def add_items(request):
    """
    Vista de API que maneja las solicitudes POST para agregar nuevos items.

    Parámetros:
    request (HttpRequest): El objeto de solicitud HTTP.

    Retorna:
    Response: Un objeto de respuesta HTTP.
    """
    item = ItemSerializer(data=request.data)

    try:
        item = ItemSerializer(data=request.data)

        # validando datos existentes
        if Item.objects.filter(**request.data).exists():
            raise serializers.ValidationError('This data already exists')

        if item.is_valid():
            item.save()
            return Response(item.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error al agregar items: {e}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def list_items(request):
    """
    Vista de API que maneja las solicitudes GET para listar items.

    Parámetros:
    request (HttpRequest): El objeto de solicitud HTTP.

    Retorna:
    Response: Un objeto de respuesta HTTP.
    """
    try:
        # chequendo los parametros de la url
        if request.query_params:
            items = Item.objects.filter(**request.query_params.dict())
        else:
            items = Item.objects.all()

        # si hay algo en item, si no lanza error
        if items:
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error al listar items: {e}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def update_items(request, pk):
    """
    Vista de API que maneja las solicitudes POST para actualizar items.

    Parámetros:
    request (HttpRequest): El objeto de solicitud HTTP.
    pk (int): El identificador primario del item a actualizar.

    Retorna:
    Response: Un objeto de respuesta HTTP.
    """
    try:
        item = Item.objects.get(pk=pk)
        data = ItemSerializer(instance=item, data=request.data)

        if data.is_valid():
            data.save()
            return Response(data.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error al actualizar items: {e}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_items(request, pk):
    """
    Vista de API que maneja las solicitudes DELETE para eliminar items.

    Parámetros:
    request (HttpRequest): El objeto de solicitud HTTP.
    pk (int): El identificador primario del item a eliminar.

    Retorna:
    Response: Un objeto de respuesta HTTP.
    """
    try:
        item = get_object_or_404(Item, pk=pk)
        item.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        logger.error(f"Error al eliminar items: {e}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

