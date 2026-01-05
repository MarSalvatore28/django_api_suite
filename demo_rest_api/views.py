from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Datos de ejemplo
data_list.append({
    'id': str(uuid.uuid4()),
    'name': 'User01',
    'email': 'user01@example.com',
    'is_active': True
})

data_list.append({
    'id': str(uuid.uuid4()),
    'name': 'User02',
    'email': 'user02@example.com',
    'is_active': True
})

data_list.append({
    'id': str(uuid.uuid4()),
    'name': 'User03',
    'email': 'user03@example.com',
    'is_active': False
})

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):

      # Filtra la lista para incluir solo los elementos donde 'is_active' es True
      active_items = [item for item in data_list if item.get('is_active', False)]
      return Response(active_items, status=status.HTTP_200_OK)
