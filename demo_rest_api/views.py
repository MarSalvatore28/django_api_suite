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

def find_item(item_id):
    """
    Busca un item por ID en data_list.
    Retorna (item, index) si lo encuentra, o (None, None) si no existe.
    """
    for index, item in enumerate(data_list):
        if item["id"] == item_id:
            return item, index
    return None, None

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):

      # Filtra la lista para incluir solo los elementos donde 'is_active' es True
      active_items = [item for item in data_list if item.get('is_active', False)]
      return Response(active_items, status=status.HTTP_200_OK)
    

    def post(self, request):
        """
        Crea un nuevo elemento en data_list con los campos name y email.
        """
        data = request.data

        # Validación mínima
        if 'name' not in data or 'email' not in data:
            return Response(
                {'error': 'Faltan campos requeridos: name y email.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Asignar ID único y marcar como activo
        data['id'] = str(uuid.uuid4())
        data['is_active'] = True

        # Agregar a la lista de datos
        data_list.append(data)

        return Response(
            {'message': 'Dato guardado exitosamente.', 'data': data},
            status=status.HTTP_201_CREATED
        )

class DemoRestApiItem(APIView):
    name = "Demo REST API Item"

    def get(self, request, item_id):
        for item in data_list:
            if item["id"] == item_id:
                return Response(item, status=status.HTTP_200_OK)

        return Response(
            {"error": "Elemento no encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )

    def put(self, request, item_id):
        data = request.data

        if "id" not in data:
            return Response(
                {"error": "El campo id es obligatorio."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if data["id"] != item_id:
            return Response(
                {"error": "El id del cuerpo no coincide con el id de la URL."},
                status=status.HTTP_400_BAD_REQUEST
            )

        for item in data_list:
            if item["id"] == item_id:

                required = {"name", "email", "is_active"}
                if not required.issubset(data.keys()):
                    return Response(
                        {"error": "Faltan campos requeridos: name, email, is_active."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                item["name"] = data["name"]
                item["email"] = data["email"]
                item["is_active"] = data["is_active"]

                return Response(
                    {"message": "Elemento actualizado completamente (PUT).", "data": item},
                    status=status.HTTP_200_OK
                )

        return Response(
            {"error": "Elemento no encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )

    def patch(self, request, item_id):
        item, index = find_item(item_id)
        if item is None:
            return Response(
                {"error": f"Item con id '{item_id}' no existe."},
                status=status.HTTP_404_NOT_FOUND
            )

        allowed_fields = {"name", "email", "is_active"}
        invalid_fields = [k for k in request.data if k not in allowed_fields]

        if invalid_fields:
            return Response(
                {"error": f"Campos inválidos: {invalid_fields}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        for key in allowed_fields:
            if key in request.data:
                item[key] = request.data[key]

        data_list[index] = item

        return Response(
            {"message": "Actualización parcial exitosa (PATCH).", "data": item},
            status=status.HTTP_200_OK
        )

    def delete(self, request, item_id):
        item, index = find_item(item_id)
        if item is None:
            return Response(
                {"error": f"Item con id '{item_id}' no existe."},
                status=status.HTTP_404_NOT_FOUND
            )

        if item.get("is_active") is False:
            return Response(
                {"message": "Ya estaba desactivado.", "data": item},
                status=status.HTTP_200_OK
            )

        item["is_active"] = False
        data_list[index] = item

        return Response(
            {"message": "Eliminación lógica exitosa.", "data": item},
            status=status.HTTP_200_OK
        )