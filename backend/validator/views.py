import re
from datetime import date, timedelta, time, datetime
from typing import List

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def easter_holiday(year: int) -> date:
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


def move_holiday(day: date) -> date:
    return day if day.weekday() == 0 else day + timedelta(days=(7 - day.weekday()))


def get_holidays(year: int):
    """
    Returns a list of holidays for the given year in Emilia-Romagna, Italy.
    """
    holidays = []
    fixed = [(1, 1), (5, 1), (7, 20), (8, 7), (12, 8), (12, 25)]
    emiliani = [(1, 6), (3, 19), (6, 24), (6, 29), (8, 15), (10, 12), (11, 1), (11, 11)]
    for m, d in fixed:
        holidays.append(date(year, m, d))
    for m, d in emiliani:
        holidays.append(move_holiday(date(year, m, d)))
    easter = easter_holiday(year)
    holidays.append(easter - timedelta(days=3))
    holidays.append(easter - timedelta(days=2))
    holidays.append(move_holiday(easter + timedelta(days=39)))
    holidays.append(move_holiday(easter + timedelta(days=60)))
    holidays.append(move_holiday(easter + timedelta(days=68)))
    return sorted(holidays)


def check_parity(num: int) -> List[int]:
    """
    Returns a list of numbers based on the parity of the input number, based on decrement 003 2023.
    :param num: An integer to check parity.
    :return: A list of integers based on the parity of the input number.
    """
    return [1, 2, 3, 4, 5] if num % 2 == 0 else [6, 7, 8, 9, 0]


def check_hours() -> bool:
    current_time = datetime.now().time()
    start_time = time(6, 0)  # 6:00 AM
    end_time = time(21, 0)  # 9:00 PM
    return start_time <= current_time <= end_time


class CirculationRestrictionView(APIView):

    @staticmethod
    def get(request):
        license_plate = request.query_params.get('placa', '').replace(' ', '').upper()
        year_param = request.query_params.get('year')

        # Validar formato de placa
        format_valid = bool(re.match(r'^[A-Z]{3}\d{3}$', license_plate))

        # Determinar año
        if year_param:
            try:
                year = int(year_param)
            except ValueError:
                return Response({'error': 'Año inválido'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            year = date.today().year

        # Validar si hoy es festivo
        holidays = get_holidays(year)
        today = date.today()
        is_holiday = today in holidays

        # Verificar si estamos en horario de pico y placa
        in_pico_hours = check_hours()

        # Último dígito de la placa
        last_digit = int(license_plate[-1]) if format_valid else None

        # Mensaje según resultado
        if not format_valid:
            msng = "Invalid format for private car"
        elif is_holiday:
            msng = "The license plate is valid and TODAY is a holiday"
        else:
            msng = "The license plate is valid and today is NOT a holiday."

        # Estado de circulación
        st = None
        if not is_holiday and in_pico_hours:
            if last_digit is not None:
                if last_digit in check_parity(today.day):
                    st = False
                else:
                    st = True

        return Response({
            "valid_format": format_valid,
            "holiday": is_holiday,
            "rush_hour": in_pico_hours,
            "weekend": today.weekday() >= 5,
            "message": msng,
            "today": today.isoformat(),
            "license_plate": license_plate,
            "last_digit": last_digit,
            "circulation_status:": st,
        }, status=status.HTTP_200_OK)
