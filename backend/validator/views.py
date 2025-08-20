import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ValidatePlaca(APIView):
    
    def get(self, request):
        return Response({'mensaje': 'Usa POST para validar la placa.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def post(self, request):
        # Busca primero en body, luego en params
        placa = request.data.get('placa') or request.GET.get('placa', '')
        placa = placa.replace(' ', '').upper()  # Elimina todos los espacios y pone en mayúsculas
        #usa regex para validar el formato de la placa
        if not re.match(r'^[A-Z]{3}\d{3}$', placa):
            return Response(
                {'valido': False, 'mensaje': 'Formato invalido para carro particular'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'valido': True, 'mensaje': 'Formato valido para carro particular'},
            status=status.HTTP_200_OK
        )