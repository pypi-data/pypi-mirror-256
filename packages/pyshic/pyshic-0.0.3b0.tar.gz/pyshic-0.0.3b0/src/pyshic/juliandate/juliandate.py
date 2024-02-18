# pyshic/juliandate/juliandate.py
"""
Julian-Gregorian Date Conversion Tool

Provides utilities for converting dates between Julian and Gregorian calendars, 
including Julian Day Number calculations. Features include type hints, 
improved docstrings, and refined function names for enhanced usability.

The module contains the following functions:

- `to_julian(J)` - Returns the sum of two numbers.
- `to_gregorian(J)` - Returns the difference of two numbers.
- `from_gregorian(a, b)` - Returns the product of two numbers.
- `from_julian(a, b)` - Returns the quotient of two numbers.


This tool is based on modified source code originally available at a public 
repository https://github.com/seanredmond/juliandate. 
We thank the original contributors for their foundational work.

Copyright (C) 2024  Cédric Renda

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


from typing import Tuple, Union

def __tdiv(t: float, d: float) -> Tuple[int, float]:
    """
    Performs division and returns the quotient and remainder as a fraction.

    Args:
        t (float): The numerator.
        d (float): The denominator.

    Returns:
        Tuple[int, float]: Quotient as an integer, and the remainder as a fraction.
    """
    return (int(d * t), d * t - int(d * t))



def __day_pct(hour, minute, second):
    """
    Calculate the fractional day from hour, minute, and second.

    Args:
        hour (int): Hour.
        minute (int): Minute.
        second (float): Second with 1/10 second  

    Returns:
        float: The fractional day.
    """
    return ((hour * 3600 + minute * 60 + second) / 86400) - 0.5


def __h_m_s(t, is_int=True):
    """
    Convert the decimal part of a Julian Day Number to hours, minutes, and seconds.

    Args:
        julian_day (float): The Julian Day Number.
        is_int (bool): Returns the full seconds as integer. if false it returns a 
        float resembling the first digit after the decimal point. Getting a resulution
        of 100 miliseconds.

    Returns:
        Tuple[int, int, float|int]: A tuple containing hour, minute, and second.
    """
    pct = t - int(t)
    (hour, r) = __tdiv(pct, 24)
    (minutes, r) = __tdiv(r, 60)
    (seconds, r) = __tdiv(r, 60)

    if is_int:
        seconds = round(seconds+r)
    else:
        seconds = seconds+round(r,2)
    if seconds >= 60:
        seconds -= 60
        minutes += 1  
    if is_int:
        return ((hour + 12) % 24, minutes, int(round(seconds)))
    return ((hour + 12) % 24, minutes, round(seconds, 1))


def __jd_to_date(jdn, is_gregorian=False):
    """
    Convert a Julian Day Number to a date in either Julian or Gregorian calendar.

    Examples:
        >>> add(4.0, 2.0)
        6.0
        >>> add(4, 2)
        6.0

    Args:
        julian_day_number (float): The Julian Day Number.
        is_gregorian (bool): True if the conversion is to Gregorian calendar, False for Julian calendar.

    Returns:
        Tuple[int, int, int]: A tuple containing year, month, and day.
    """
    J = int(jdn + 0.5)

    m = 2
    n = 12
    p = 1461
    r = 4
    s = 153
    u = 5
    v = 3
    w = 2
    y = 4716

    f = __param_f(J, is_gregorian)
    e = r * f + v
    g = int((e % p) / r)
    h = u * g + w

    D = int((h % s) / u) + 1
    M = ((int(h / s) + m) % n) + 1
    Y = e / p - y + (n + m - M) / n

    Y = int(e / p) - y + int((n + m - M) / n)

    return (Y, M, D)


def __param_f(julian_day: Union[int,float], is_gregorian: bool = False) -> int:
    """
    Calculate parameter f for conversion algorithm depending on the calendar type.

    Args:
        julian_day (float|int): The Julian Day Number.
        is_gregorian (bool): True if the conversion is to Gregorian calendar, False otherwise.

    Returns:
        int: The calculated parameter f.
    """
    j = 1401
    B = 274277
    C = -38

    if is_gregorian:
        return julian_day + j + int((int((4 * julian_day + B) / 146_097) * 3) / 4) + C
    return julian_day + j




def to_julian(julian_day: Union[int,float], is_int:bool=True) -> Tuple[int, int, int, int, int, Union[int,float]]:
    """
    Convert a Julian Day Number to a Julian calendar date including hour, minute, and seconds. 

    Examples:
        >>> to_julian(1566223.56309468)
        (-424, 2, 2, 1, 30, 51)
        >>> to_julian(1566223.56309468, is_int=False)
        (-424, 2, 2, 1, 30, 51.4)
        >>> to_julian(1566223.563096, is_int=False)
        (-424, 2, 2, 1, 30, 51.5)
        >>> to_julian(0)
        (-4712, 1, 1, 12, 0, 0)
    
    The negative year indicates BCE. 
    1 BCE is 0, so -43 means 44 BCE, and this value is March 15, 44 BCE (the Ides of March).
        >>> to_julian(1705426)
        (-43, 3, 15, 12, 0, 0, 0)


    Args:
        julian_day (float, int): The Julian Day Number as float or int.

    Returns:
        A tuple containing year, month, day, hour, minute, and second.
    """
    return __jd_to_date(julian_day) + __h_m_s(julian_day, is_int)


def to_gregorian(julian_day: Union[int,float], is_int:bool=True) -> Tuple[int, int, int, int, int, int]:
    """
    Convert a Julian Day Number to a Gregorian calendar date including hour, minute, and second.

    Examples:
        >>> to_gregorian(1566223.56309468)
        (-424, 1, 28, 1, 30, 51)
        >>> to_julian(0)
        (-4712, 1, 1, 12, 0, 0)

    !!! tip 
        ## Datetime usage
        If you want to convert it to a datetime format use the **to_gregorian** method togeher 
        with the * operator to unpack the values into a datetime object.

        ``` py
            from datetime import datetime
            datetime(*to_gregorian(2440423.345139, is_int=True))
        ```


    Args:
        julian_day (float, int): The Julian Day Number.

    Returns:
        A tuple containing year, month, day, hour, minute, and second.
    """
    return __jd_to_date(julian_day, True) + __h_m_s(julian_day, is_int)


def from_gregorian(year:int, month:int, day:int, hour:int=0, minute:int=0, seconds:Union[float,int]=0):
    """
    Convert a Gregorian calendar date to a Julian Day Number. The algorithm 
    is valid for all (possibly proleptic) Gregorian calendar dates after 
    November 23, −4713. Divisions are integer divisions towards zero; 
    fractional parts are ignored.

    Examples:
        >>> from_gregorian(-4713, 11, 24, 12, 0, 0)
        0
        >>> from_gregorian(1969, 7, 20)
        2440422.5
        >>> from_gregorian(1969, 7, 20, 20, 17, 30)
        2440423.345486111
        >>> to_gregorian(from_gregorian(1969, 7, 20, 20, 17, 58.4),is_int=False)
        (1969, 7, 20, 20, 17, 58.4)

    Args:
        year (int): Year.
        month (int): Month.
        day (int): Day.
        hour (int): Hour.
        minute (int): Minute.
        seconds (int|float): Seconds get rounded to the closest tenth of a second.

    Returns:
        (float): The Julian Day Number.
    """
    tmp = (
        int((1461 * (year + 4800 + int((month - 14) / 12))) / 4)
        + int((367 * (month - 2 - 12 * int((month - 14) / 12))) / 12)
        - int((3 * int((year + 4900 + int((month - 14) / 12)) / 100)) / 4)
        + day
        - 32075
    ) 

    seconds = round(seconds,1)
    return tmp + __day_pct(hour, minute, seconds)


def from_julian(year:int, month:int, day:int, hour:int=0, minute:int=0, second:Union[int,float]=0):
    """
    Convert a Julian calendar date to a Julian Day Number. The algorithm 
    is valid for all (possibly proleptic) Julian calendar years ≥ −4712, 
    that is, for all JDN ≥ 0. Divisions are integer divisions, 
    fractional parts are ignored.

    Examples:
        >>> from_julian(-43, 3, 15)
        1705425.5
        >>> from_julian(-43, 3, 15, 15)
        1705426.125
        >>> from_julian(-4712, 1, 1, 12, 0, 0)
        0

    Args:
        year (int): Year.
        month (int): Month.
        day (int): Day.
        hour (int): Hour.
        minute (int): Minute.
        second (int|float): Seconds get rounded to the closest tenth of a second.

    Returns:
        (float): The Julian Day Number.
    """
    second = round(second, 1)
    return (
        367 * year
        - int((7 * (year + 5001 + int((month - 9) / 7))) / 4)
        + int((275 * month) / 9)
        + day
        + 1729777
        + __day_pct(hour, minute, second)
    )
















