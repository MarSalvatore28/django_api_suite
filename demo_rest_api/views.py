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

def find_item(item_id: str):
    """Busca un item por id en data_list. Retorna (item, index) o (None, None)."""
    for i, item in enumerate(data_list):
        if item.get("id") == item_id:
            return item, i
    return None, None


class DemoRestApiItem(APIView):
    name = "Demo REST API Item"

    def patch(self, request, item_id):
        item, index = find_item(item_id)
        if item is None:
            return Response(
                {"message": "No encontrado", "error": f"Item con id '{item_id}' no existe."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Si está inactivo, igual puedes decidir si permites editarlo o no:
        # Aquí lo permitimos, pero tú puedes bloquearlo si quieres.
        data = request.data

        # Campos permitidos a actualizar (parcial)
        allowed_fields = {"name", "email", "is_active"}

        # Si mandan campos raros, avisa
        invalid_fields = [k for k in data.keys() if k not in allowed_fields]
        if invalid_fields:
            return Response(
                {
                    "message": "Campos inválidos",
                    "error": f"No puedes actualizar: {invalid_fields}. Permitidos: {sorted(list(allowed_fields))}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Actualiza solo lo que venga en el body
        for key in allowed_fields:
            if key in data:
                item[key] = data[key]

        # Guarda de vuelta (en lista es la misma referencia, pero lo dejamos claro)
        data_list[index] = item

        return Response(
            {"message": "Actualización parcial exitosa (PATCH)", "data": item},
            status=status.HTTP_200_OK
        )
           def delete(self, request, item_id):
        item, index = find_item(item_id)
        if item is None:
            return Response(
                {"message": "No encontrado", "error": f"Item con id '{item_id}' no existe."},
                status=status.HTTP_404_NOT_FOUND
            )

        # DELETE lógico: si ya está inactivo, responde bonito
        if item.get("is_active") is False:
            return Response(
                {"message": "Ya estaba desactivado", "data": item},
                status=status.HTTP_200_OK
            )

        item["is_active"] = False
        data_list[index] = item

        return Response(
            {"message": "Eliminación lógica exitosa (is_active=False)", "data": item},
            status=status.HTTP_200_OK
        )