import re
from datetime import date, timedelta, time, datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

def easterHoliday(year: int) -> date:
    a = year % 19                 
    b = year // 100               
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)

def moveHoliday(day: date) -> date:
    return day if day.weekday() == 0 else day + timedelta(days=(7 - day.weekday()))

def getHolidays(year: int):
    holidays = []
    fixed = [(1,1),(5,1),(7,20),(8,7),(12,8),(12,25)]
    emiliani = [(1,6),(3,19),(6,24),(6,29),(8,15),(10,12),(11,1),(11,11)]
    for m,d in fixed:
        holidays.append(date(year,m,d))
    for m,d in emiliani:
        holidays.append(moveHoliday(date(year,m,d)))
    easter = easterHoliday(year)
    holidays.append(easter - timedelta(days=3))
    holidays.append(easter - timedelta(days=2))
    holidays.append(moveHoliday(easter + timedelta(days=39)))
    holidays.append(moveHoliday(easter + timedelta(days=60)))
    holidays.append(moveHoliday(easter + timedelta(days=68)))
    return sorted(holidays)

def par_impar(num : int) -> str:
    return [1, 2, 3, 4, 5] if num % 2 == 0 else [6, 7, 8, 9, 0]

def checkHours() -> bool:
    current_time = datetime.now().time()
    start_time = time(6, 0)  # 6:00 AM
    end_time = time(21, 0)   # 9:00 PM
    return start_time <= current_time <= end_time

class ValidatePlaca(APIView):

    def get(self, request):
        placa = request.query_params.get('placa', '').replace(' ', '').upper()
        year_param = request.query_params.get('year')

        # Validar formato de placa
        format_valid = bool(re.match(r'^[A-Z]{3}\d{3}$', placa))

        # Determinar año
        if year_param:
            try:
                year = int(year_param)
            except ValueError:
                return Response({'error': 'Año inválido'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            year = date.today().year

        # Validar si hoy es festivo
        holidays = getHolidays(year)
        today = date.today()
        is_holiday = today in holidays

        # Verificar si estamos en horario de pico y placa
        in_pico_hours = checkHours()

        # Último dígito de la placa
        last_digit = int(placa[-1]) if format_valid else None

        # Mensaje según resultado
        if not format_valid:
            msng = "Formato inválido para carro particular"
        elif is_holiday:
            msng = "La placa es válida y HOY es festivo"
        else:
            msng = "La placa es válida y hoy NO es festivo"

        # Estado de circulación
        st = None
        if not is_holiday and in_pico_hours:
            if last_digit is not None:
                if last_digit in par_impar(today.day):
                    st = False
                else:
                    st = True

        return Response({
            "valid format": format_valid,
            "holiday": is_holiday,
            "rush hour": in_pico_hours,
            "weekend": today.weekday() >= 5,
            "message": msng,
            "today": today.isoformat(),
            "placa": placa,
            "last digit": last_digit,
            "circulacion status:": st,
        }, status=status.HTTP_200_OK)