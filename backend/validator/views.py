from django.shortcuts import render
from rest_framework.views import Response, APIView

# Create your views here.
class ParityCheckView(APIView):
    @staticmethod
    def get(request):
        try:
            number = request.query_params.get('number')
            if number is None:
                return Response({'error': 'No number provided'}, status=400)
            num = int(number)
            parity = 'par' if num % 2 == 0 else 'impar'
            return Response({'Numero es ': parity})
        except ValueError:
            return Response({'error': 'Invalid number format'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
