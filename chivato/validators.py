#-*- coding: utf-8 -*-

import re

from .helpers import _posint, mult_add, mod1110


def austria(vat):
    '''Check Austria VAT number.'''
    if len(vat) != 9:
        return False

    if vat[0] != 'U':
        return False

    num = vat[1:]
    try:
        _posint(num)
    except ValueError:
        return False

    check_sum = sum(mult_add(n) if i % 2 else n
                    for i, n in enumerate(map(int, num[:-1])))

    check = 10 - ((check_sum + 4) % 10)

    if check == 10:
        check = 0

    if int(vat[-1:]) != check:
        return False

    return True


def albania(vat):
    '''Check Albania VAT number.'''
    if len(vat) != 10:
        return False

    if vat[0] not in ('J', 'K'):
        return False

    try:
        _posint(vat[1:9])
    except ValueError:
        return False

    if ord(vat[9]) < 65 or ord(vat[9]) > 90:
        return False

    return True


def argentina(vat):
    '''Check Argentina VAT number.'''
    if len(vat) != 11:
        return False

    base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    aux = 0
    for i in range(10):
        aux += int(vat[i]) * base[i]

    aux = 11 - (aux - (int(aux / 11) * 11))
    if aux == 11:
        aux = 0
    if aux == 10:
        aux = 9

    return aux == int(vat[10])


def belgium(vat):
    '''Check Belgium VAT number.'''
    if len(vat) != 10:
        return False

    if vat[0] != '0':
        return False

    try:
        _posint(vat)
    except ValueError:
        return False

    num, control = int(vat[:-2]), int(vat[-2:])

    return control == 97 - (num % 97)


def bulgaria(vat):
    '''Check Bulgaria VAT number.'''
    if len(vat) == 9:
        #XXX don't know any rules for this length
        return True

    if len(vat) != 10:
        return False

    try:
        _posint(vat)
    except ValueError:
        return False

    if int(vat[0]) in (2, 3) and \
            int(vat[1:2]) != 22:
        return False

    coefficients = (4, 3, 2, 7, 6, 5, 4, 3, 2)
    check_sum = sum(c * int(n) for c, n in zip(coefficients, vat))

    check = 11 - (check_sum % 11)
    if check == 11:
        check = 0

    if check == 10:
        return False

    if check != int(vat[9]):
        return False

    return True


def chile(rut):
    '''Check Chile RUT number.'''
    try:
        _posint(rut[:-1])
    except ValueError:
        return False

    sum = 0
    for i in range(len(rut) - 2, -1, -1):
        sum += int(rut[i]) * (((len(rut) - 2 - i) % 6) + 2)

    check = 11 - (sum % 11)
    if check == 11:
        return rut[-1] == '0'
    elif check == 10:
        return rut[-1].upper() == 'K'
    else:
        return check == int(rut[-1])


def colombia(rut):
    '''Check Colombian RUT number.'''
    if len(rut) != 10:
        return False

    try:
        _posint(rut)
    except ValueError:
        return False

    nums = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71]
    sum = 0
    for i in range(len(rut) - 2, -1, -1):
        sum += int(rut[i]) * nums[len(rut) - 2 - i]

    if sum % 11 > 1:
        return int(rut[-1]) == 11 - (sum % 11)
    else:
        return int(rut[-1]) == sum % 11


def cyprus(vat):
    '''Check Cyprus VAT number.'''
    if len(vat) != 9:
        return False

    try:
        _posint(vat[:8])
    except ValueError:
        return False

    conv = {0: 1, 1: 0, 2: 5, 3: 7, 4: 9, 5: 13, 6: 15, 7: 17, 8: 19, 9: 21}

    num0, num1, num2, num3, num4, num5, num6, num7 = map(int, vat[:8])

    num0 = conv.get(num0, num0)
    num2 = conv.get(num2, num2)
    num4 = conv.get(num4, num4)
    num6 = conv.get(num6, num6)

    check_sum = num0 + num1 + num2 + num3 + num4 + num5 + num6 + num7

    check = chr(check_sum % 26 + 65)
    if check != vat[8]:
        return False

    return True


def czech_republic(vat):
    '''Check Czech Republic VAT number.'''
    if len(vat) not in (8, 9, 10):
        return False

    try:
        _posint(vat)
    except ValueError:
        return False

    if len(vat) == 8:
        if int(vat[0]) not in (0, 1, 2, 3, 4, 5, 6, 7, 8):
            return False
        check_sum = 8 * int(vat[0]) + 7 * int(vat[1]) + 6 * int(vat[2]) + \
            5 * int(vat[3]) + 4 * int(vat[4]) + 3 * int(vat[5]) + \
            2 * int(vat[6])
        check = 11 - (check_sum % 11)
        if check == 10:
            check = 0
        if check == 11:
            check = 1
        if check != int(vat[7]):
            return False

    elif len(vat) == 9 and int(vat[0]) == 6:
        check_sum = 8 * int(vat[1]) + 7 * int(vat[2]) + 6 * int(vat[3]) + \
            5 * int(vat[4]) + 4 * int(vat[5]) + 3 * int(vat[6]) + \
            2 * int(vat[7])
        check = 9 - ((11 - (check_sum % 11)) % 10)
        if check != int(vat[8]):
            return False

    elif len(vat) == 9:
        if int(vat[0:2]) > 53 and int(vat[0:2]) < 80:
            return False
        if int(vat[2:4]) < 1:
            return False
        if int(vat[2:4]) > 12 and int(vat[2:4]) < 51:
            return False
        if int(vat[2:4]) > 62:
            return False
        if int(vat[2:4]) in (2, 52) and int(vat[0:2]) % 4 > 0:
            if int(vat[4:6]) < 1:
                return False
            if int(vat[4:6]) > 28:
                return False
        if int(vat[2:4]) in (2, 52) and int(vat[0:2]) % 4 == 0:
            if int(vat[4:6]) < 1:
                return False
            if int(vat[4:6]) > 29:
                return False
        if int(vat[2:4]) in (4, 6, 9, 11, 54, 56, 59, 61):
            if int(vat[4:6]) < 1:
                return False
            if int(vat[4:6]) > 30:
                return False
        if int(vat[2:4]) in (1, 3, 5, 7, 8, 10, 12, 51,
                             53, 55, 57, 58, 60, 62):
            if int(vat[4:6]) < 1:
                return False
            if int(vat[4:6]) > 31:
                return False

    elif len(vat) == 10:
        if int(vat[0:2]) < 54:
            return False
        if int(vat[2:4]) < 1:
            return False
        if int(vat[2:4]) > 12 and int(vat[2:4]) < 51:
            return False
        if int(vat[2:4]) > 62:
            return False
        if int(vat[2:4]) in (2, 52) and int(vat[0:2]) % 4 > 0:
            if int(vat[4:6]) < 1:
                return False
            if int(vat[4:6]) > 28:
                return False
        if int(vat[2:4]) in (2, 52) and int(vat[0:2]) % 4 == 0:
            if int(vat[4:6]) < 1:
                return False
            if int(vat[4:6]) > 29:
                return False
        if int(vat[2:4]) in (4, 6, 9, 11, 54, 56, 59, 61):
            if int(vat[4:6]) < 1:
                return False
            if int(vat[4:6]) > 30:
                return False

        if int(vat[2:4]) in (1, 3, 5, 7, 8, 10, 12, 51,
                             53, 55, 57, 58, 60, 62):
            if int(vat[4:6]) < 1:
                return False
            if int(vat[4:6]) > 31:
                return False

        if (int(vat[0:10]) % 11 != 0 or ((int(vat[0:2]) + int(vat[2:4]) + int(vat[4:6]) +
                                         int(vat[6:8]) + int(vat[8:10]))
                                         % 11 != 0)):
            return False

    return True


def germany(vat):
    '''Check Germany VAT number .'''
    if len(vat) != 9:
        return False

    try:
        _posint(vat)
    except ValueError:
        return False

    if int(vat[0:7]) <= 0:
        return False

    check_sum = 0
    for i in range(8):
        check_sum = (2 * ((int(vat[i]) + check_sum + 9) % 10 + 1)) % 11

    check = 11 - check_sum
    if check == 10:
        check = 0

    if int(vat[8]) != check:
        return False

    return True


def denmark(vat):
    '''Check Denmark VAT number.'''
    if len(vat) != 8:
        return False

    try:
        _posint(vat)
    except ValueError:
        return False

    if int(vat[0]) <= 0:
        return False

    check_sum = (2 * int(vat[0]) + 7 * int(vat[1]) + 6 * int(vat[2]) +
                 5 * int(vat[3]) + 4 * int(vat[4]) + 3 * int(vat[5]) +
                 2 * int(vat[6]) + int(vat[7]))

    if check_sum % 11 != 0:
        return False
    return True


def estonia(vat):
    '''Check Estonia VAT number.'''
    if len(vat) != 9:
        return False

    try:
        _posint(vat)
    except ValueError:
        return False

    check_sum = (3 * int(vat[0]) + 7 * int(vat[1]) + 1 * int(vat[2]) +
                 3 * int(vat[3]) + 7 * int(vat[4]) + 1 * int(vat[5]) +
                 3 * int(vat[6]) + 7 * int(vat[7]))

    check = 10 - (check_sum % 10)
    if check == 10:
        check = 0

    if check != int(vat[8]):
        return False

    return True


class Spain(object):
    """Spanish VAT number 'CIF'

    The code has 9 characters, always starts with a single letter,
    has a control code and 3 different fields:

        kind: A letter which indicates the company kind
                the allowed letters are A-H J-N P-S and U V W

        number: Seven-digit id number

        control: A single character computed over the concatenation of
                    province and number digits, which may end up being
                    a letter or a digit depending on the kind

    documentation: http://www.boe.es/buscar/doc.php?id=BOE-A-1998-16310
    """

    _parse_re = re.compile(
        '(?P<kind>[A-HJ-NP-SUVW])'  # company category letter
        '(?P<number>\d{7})'         # province + id number
        '(?P<control>\w)',          # control character
        flags=re.IGNORECASE)

    DIGIT_ONLY = 'ABEH'
    LETTER_ONLY = 'KPQS'
    CONTROL_LETTERS = 'JABCDEFGHI'

    def __call__(self, vat):
        return self.validate(vat)

    def validate(self, vat):
        """Check Spain VAT number."""
        try:
            kind, number, control = self.parse(vat)
        except ValueError:
            return False

        calculated_control = self.control_char(kind, number)

        return self.compare_control_chars(kind, control, calculated_control)

    def parse(self, vat):
        match = self._parse_re.match(vat)
        if not match:
            raise ValueError(u'Invalid format for vat number "{0}"'
                             .format(vat))

        return match.groups()

    def compare_control_chars(self, kind, given, calculated):
        """Check if the given control code matches the calculated one
        This is necessary as some numbers may accept the character
        both in it's letter and digit form

        The calculated control char should be an integer
        """
        calculated_letter = self.CONTROL_LETTERS[calculated]

        return (
            (kind not in self.LETTER_ONLY and given == str(calculated))
            or (kind not in self.DIGIT_ONLY and given == calculated_letter)
        )

    def control_char(self, kind, number, digit_only=DIGIT_ONLY):
        """Compute the control char from the company kind and the number

        The algorithm is the following:

            A = Sum all the digits in even positions in the number
                 ([0] is odd)

            B = Get all the odd digits in the number
                 Multiply each digit by two
                 If the result has two digits, add them
                 (eg: 6 * 2 = '12' and 1 + 2 = 3)
                 Add them all together

            C = A + B

            D = Get the unit digit from C
                 (eg: unit digit of '12' is 2)

            If happens to not to be 0, substract it from 10
                E = 10 - D

            If the number kind letter is one of A B E H
             the control character is a digit, and return E right away.

            Otherwise, if the number kind letter is K P Q S
             a letter must be return which can be looked up
             in a table using E as index.
        """
        control_number = sum(d if i % 2 else mult_add(d)
                             for i, d in enumerate(int(c) for c in number))

        # get the units (rightmost digit)
        unit = int(str(control_number)[-1])
        return unit if unit == 0 else 10 - unit  # 10 - n but in [0-9]


def finland(vat):
    '''Check Finland VAT number.'''
    if len(vat) != 8:
        return False

    try:
        _posint(vat)
    except ValueError:
        return False

    check_sum = (7 * int(vat[0]) + 9 * int(vat[1]) + 10 * int(vat[2]) +
                 5 * int(vat[3]) + 8 * int(vat[4]) + 4 * int(vat[5]) +
                 2 * int(vat[6]))

    check = 11 - (check_sum % 11)
    if check == 11:
        check = 0

    if check == 10:
        return False

    if check != int(vat[7]):
        return False
    return True


def france(vat):
    '''Check France VAT number.'''
    if len(vat) != 11:
        return False

    try:
        _posint(vat[2:11])
    except ValueError:
        return False

    system = None
    try:
        _posint(vat[0:2])
        system = 'old'
    except ValueError:
        system = 'new'

    if system == 'old':
        check = ((int(vat[2:11]) * 100) + 12) % 97
        if check != int(vat[0:2]):
            return False
        return True
    else:
        conv = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B',
                'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P',
                'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        if (vat[0] not in conv) or (vat[1] not in conv):
            return False

        check1 = conv.index(vat[0])
        check2 = conv.index(vat[1])

        if check1 < 10:
            check_sum = check1 * 24 + check2 - 10
        else:
            check_sum = check1 * 34 + check2 - 100

        mod_x = check_sum % 11
        check_sum = (int(check_sum) / 11) + 1
        mod_y = (int(vat[2:11]) + check_sum) % 11

        if mod_x != mod_y:
            return False
        return True


def united_kingdom(vat):
    '''Check United Kingdom VAT number.'''
    if len(vat) == 5:
        try:
            _posint(vat[2:5])
        except ValueError:
            return False

        if vat[0:2] == 'GD':
            if int(vat[2:5]) >= 500:
                return False
            return True

        if vat[0:2] == 'HA':
            if int(vat[2:5]) < 500:
                return False
            return True

        return False

    elif len(vat) == 11 and vat[0:6] in ('GD8888', 'HA8888'):
        try:
            _posint(vat[6:11])
        except ValueError:
            return False

        if vat[0:2] == 'GD' and int(vat[6:9]) >= 500:
            return False

        elif vat[0:2] == 'HA' and int(vat[6:9]) < 500:
            return False

        if int(vat[6:9]) % 97 == int(vat[9:11]):
            return True
        return False

    elif len(vat) in (12, 13) and vat[0:3] in ('000', '001'):
        try:
            _posint(vat)
        except ValueError:
            return False

        if int(vat[3:10]) < 1:
            return False

        if int(vat[10:12]) > 97:
            return False

        if len(vat) == 13 and int(vat[12]) != 3:
            return False

        check_sum = (8 * int(vat[3]) + 7 * int(vat[4]) + 6 * int(vat[5]) +
                     5 * int(vat[6]) + 4 * int(vat[7]) + 3 * int(vat[8]) +
                     2 * int(vat[9]) + 10 * int(vat[10]) + int(vat[11]))

        if check_sum % 97 != 0:
            return False
        return True

    elif len(vat) in (9, 10, 12):
        try:
            _posint(vat)
        except ValueError:
            return False

        if int(vat[0:7]) < 1:
            return False

        if int(vat[7:9]) > 97:
            return False

        if len(vat) == 10 and int(vat[9]) != 3:
            return False

        check_sum = (8 * int(vat[0]) + 7 * int(vat[1]) + 6 * int(vat[2]) +
                     5 * int(vat[3]) + 4 * int(vat[4]) + 3 * int(vat[5]) +
                     2 * int(vat[6]) + 10 * int(vat[7]) + int(vat[8]))

        if int(vat[0:3]) >= 100:
            if check_sum % 97 not in (0, 55, 42):
                return False

        else:
            if check_sum % 97 != 0:
                return False
        return True

    return False


def greece(vat):
    '''Check Greece VAT number.'''
    try:
        _posint(vat)
    except ValueError:
        return False

    if len(vat) == 8:

        check_sum = (128 * int(vat[0]) + 64 * int(vat[1]) + 32 * int(vat[2]) +
                     16 * int(vat[3]) + 8 * int(vat[4]) + 4 * int(vat[5]) +
                     2 * int(vat[6]))

        check = check_sum % 11
        if check == 10:
            check = 0

        if check != int(vat[7]):
            return False

        return True

    elif len(vat) == 9:

        check_sum = (256 * int(vat[0]) + 128 * int(vat[1]) + 64 * int(vat[2]) +
                     32 * int(vat[3]) + 16 * int(vat[4]) + 8 * int(vat[5]) +
                     4 * int(vat[6]) + 2 * int(vat[7]))

        check = check_sum % 11
        if check == 10:
            check = 0

        if check != int(vat[8]):
            return False
        return True

    return False


def croatia(vat):
    '''Check Croatia VAT number.'''
    if len(vat) != 11:
        return False

    try:
        _posint(vat)
    except ValueError:
        return False

    check = mod1110(vat[:-1])
    if check != int(vat[10]):
        return False
    return True


def hungary(vat):
    '''Check Hungary VAT number.'''
    if len(vat) != 8:
        return False

    try:
        _posint(vat)
    except ValueError:
        return False

    if int(vat[0]) <= 0:
        return False

    check_sum = (9 * int(vat[0]) + 7 * int(vat[1]) + 3 * int(vat[2]) +
                 1 * int(vat[3]) + 9 * int(vat[4]) + 7 * int(vat[5]) +
                 3 * int(vat[6]))

    check = 10 - (check_sum % 10)
    if check == 10:
        check = 0

    if check != int(vat[7]):
        return False
    return True


def ireland(vat):
    '''Check Ireland VAT number.'''
    if len(vat) != 8:
        return False

    if (ord(vat[1]) >= 65 and ord(vat[1]) <= 90) or vat[1] in ('+', '*'):
        try:
            _posint(vat[0])
            _posint(vat[2:7])
        except ValueError:
            return False

        if int(vat[0]) <= 6:
            return False

        check_sum = (7 * int(vat[2]) + 6 * int(vat[3]) + 5 * int(vat[4]) +
                     4 * int(vat[5]) + 3 * int(vat[6]) + 2 * int(vat[0]))

        check = check_sum % 23
        if check == 0:
            check = 'W'
        else:
            check = chr(check + 64)

        if check != vat[7]:
            return False
        return True

    else:
        try:
            _posint(vat[0:7])
        except ValueError:
            return False

        check_sum = (8 * int(vat[0]) + 7 * int(vat[1]) + 6 * int(vat[2]) +
                     5 * int(vat[3]) + 4 * int(vat[4]) + 3 * int(vat[5]) +
                     2 * int(vat[6]))

        check = check_sum % 23
        if check == 0:
            check = 'W'
        else:
            check = chr(check + 64)
            if check != vat[7]:
                return False
        return True


def italy(vat):
    '''Check Italy VAT number.'''
    if len(vat) != 11:
        return False

    try:
        _posint(vat)
    except ValueError:
        return False

    if int(vat[0:7]) <= 0:
        return False

    if not((0 <= int(vat[7:10]) <= 100)
            or int(vat[7:10]) in (120, 121, 888, 999)):
        return False

    check_sum = (int(vat[0]) + mult_add(2, int(vat[1])) + int(vat[2]) +
                 mult_add(2, int(vat[3])) + int(vat[4]) +
                 mult_add(2, int(vat[5])) + int(vat[6]) +
                 mult_add(2, int(vat[7])) + int(vat[8]) +
                 mult_add(2, int(vat[9])))

    check = 10 - (check_sum % 10)
    if check == 10:
        check = 0

    if check != int(vat[10]):
        return False

    return True


def lithuania(vat):
    '''Check Lithuania VAT number.'''
    try:
        _posint(vat)
    except ValueError:
        return False

    if len(vat) == 9:
        if int(vat[7]) != 1:
            return False

        check_sum = (1 * int(vat[0]) + 2 * int(vat[1]) + 3 * int(vat[2]) +
                     4 * int(vat[3]) + 5 * int(vat[4]) + 6 * int(vat[5]) +
                     7 * int(vat[6]) + 8 * int(vat[7]))

        if check_sum % 11 == 10:
            check_sum = (3 * int(vat[0]) + 4 * int(vat[1]) + 5 * int(vat[2]) +
                         6 * int(vat[3]) + 7 * int(vat[4]) + 8 * int(vat[5]) +
                         9 * int(vat[6]) + 1 * int(vat[7]))

        check = check_sum % 11
        if check == 10:
            check = 0

        if check != int(vat[8]):
            return False
        return True

    elif len(vat) == 12:
        if int(vat[10]) != 1:
            return False

        check_sum = 1 * int(vat[0]) + 2 * int(vat[1]) + 3 * int(vat[2]) + \
            4 * int(vat[3]) + 5 * int(vat[4]) + 6 * int(vat[5]) + \
            7 * int(vat[6]) + 8 * int(vat[7]) + 9 * int(vat[8]) + \
            1 * int(vat[9]) + 2 * int(vat[10])

        if check_sum % 11 == 10:
            check_sum = (3 * int(vat[0]) + 4 * int(vat[1]) + 5 * int(vat[2]) +
                         6 * int(vat[3]) + 7 * int(vat[4]) + 8 * int(vat[5]) +
                         9 * int(vat[6]) + 1 * int(vat[7]) + 2 * int(vat[8]) +
                         3 * int(vat[9]) + 4 * int(vat[10]))

        check = check_sum % 11
        if check == 10:
            check = 0

        if check != int(vat[11]):
            return False
        return True

    return False


def luxembourg(vat):
    '''Check Luxembourg VAT number.'''
    if len(vat) != 8:
        return False

    try:
        _posint(vat)
    except ValueError:
        return False

    if int(vat[0:6]) <= 0:
        return False

    check = int(vat[0:6]) % 89
    if check != int(vat[6:8]):
        return False
    return True


def latvia(vat):
    '''Check Latvia VAT number.'''
    if len(vat) != 11:
        return False

    try:
        _posint(vat)
    except ValueError:
        return False

    if int(vat[0]) >= 4:
        check_sum = (9 * int(vat[0]) + 1 * int(vat[1]) + 4 * int(vat[2]) +
                     8 * int(vat[3]) + 3 * int(vat[4]) + 10 * int(vat[5]) +
                     2 * int(vat[6]) + 5 * int(vat[7]) + 7 * int(vat[8]) +
                     6 * int(vat[9]))

        if check_sum % 11 == 4 and int(vat[0]) == 9:
            check_sum = check_sum - 45

        if check_sum % 11 == 4:
            check = 4 - (check_sum % 11)
        elif check_sum % 11 > 4:
            check = 14 - (check_sum % 11)
        elif check_sum % 11 < 4:
            check = 3 - (check_sum % 11)

        if check != int(vat[10]):
            return False
        return True

    else:
        if int(vat[2:4]) == 2 and int(vat[4:6]) % 4 > 0:
            if int(vat[0:2]) < 1 or int(vat[0:2]) > 28:
                return False

        if int(vat[2:4]) == 2 and int(vat[4:6]) % 4 == 0:
            if int(vat[0:2]) < 1 or int(vat[0:2]) > 29:
                return False

        if int(vat[2:4]) in (4, 6, 9, 11):
            if int(vat[0:2]) < 1 or int(vat[0:2]) > 30:
                return False

        if int(vat[2:4]) in (1, 3, 5, 7, 8, 10, 12):
            if int(vat[0:2]) < 1 or int(vat[0:2]) > 31:
                return False

        if int(vat[2:4]) < 1 or int(vat[2:4]) > 12:
            return False

        return True


def malta(vat):
    '''Check Malta VAT number.'''
    if len(vat) != 8:
        return False

    try:
        _posint(vat)
    except ValueError:
        return False

    if int(vat[0:6]) < 100000:
        return False

    check_sum = (3 * int(vat[0]) + 4 * int(vat[1]) + 6 * int(vat[2]) +
                 7 * int(vat[3]) + 8 * int(vat[4]) + 9 * int(vat[5]))

    check = 37 - (check_sum % 37)
    if check != int(vat[6:8]):
        return False
    return True


def netherlands(vat):
    '''Check Netherlands VAT number.'''
    if len(vat) != 12:
        return False

    try:
        _posint(vat[0:9])
        _posint(vat[10:12])
    except ValueError:
        return False

    if int(vat[0:8]) <= 0:
        return False

    if vat[9] != 'B':
        return False

    check_sum = (9 * int(vat[0]) + 8 * int(vat[1]) + 7 * int(vat[2]) +
                 6 * int(vat[3]) + 5 * int(vat[4]) + 4 * int(vat[5]) +
                 3 * int(vat[6]) + 2 * int(vat[7]))

    check = check_sum % 11
    if check == 10:
        return False

    if check != int(vat[8]):
        return False
    return True


def poland(vat):
    '''Check Poland VAT number.'''
    if len(vat) != 10:
        return False

    try:
        _posint(vat)
    except ValueError:
        return False

    check_sum = (6 * int(vat[0]) + 5 * int(vat[1]) + 7 * int(vat[2]) +
                 2 * int(vat[3]) + 3 * int(vat[4]) + 4 * int(vat[5]) +
                 5 * int(vat[6]) + 6 * int(vat[7]) + 7 * int(vat[8]))

    check = check_sum % 11
    if check == 10:
        return False

    if check != int(vat[9]):
        return False
    return True


def portugal(vat):
    '''Check Portugal VAT number.'''
    if len(vat) != 9:
        return False

    try:
        _posint(vat)
    except ValueError:
        return False

    if int(vat[0]) <= 0:
        return False

    check_sum = (9 * int(vat[0]) + 8 * int(vat[1]) + 7 * int(vat[2]) +
                 6 * int(vat[3]) + 5 * int(vat[4]) + 4 * int(vat[5]) +
                 3 * int(vat[6]) + 2 * int(vat[7]))

    check = 11 - (check_sum % 11)
    if check == 10 or check == 11:
        check = 0

    if check != int(vat[8]):
        return False
    return True


def romania(vat):
    '''Check Romania VAT number.'''
    try:
        _posint(vat)
    except ValueError:
        return False

    if len(vat) >= 2 and len(vat) <= 10:
        vat = (10 - len(vat)) * '0' + vat

        check_sum = (7 * int(vat[0]) + 5 * int(vat[1]) + 3 * int(vat[2]) +
                     2 * int(vat[3]) + 1 * int(vat[4]) + 7 * int(vat[5]) +
                     5 * int(vat[6]) + 3 * int(vat[7]) + 2 * int(vat[8]))

        check = (check_sum * 10) % 11
        if check == 10:
            check = 0

        if check != int(vat[9]):
            return False

        return True

    elif len(vat) == 13:
        if int(vat[0]) not in (1, 2, 3, 4, 6):
            return False

        if int(vat[3:5]) < 1 or int(vat[3:5]) > 12:
            return False

        if int(vat[3:5]) == 2 and int(vat[1:3]) % 4 > 0:
            if int(vat[5:7]) < 1 or int(vat[5:7]) > 28:
                return False

        if int(vat[3:5]) == 2 and int(vat[1:3]) % 4 == 0:
            if int(vat[5:7]) < 1 or int(vat[5:7]) > 29:
                return False

        if int(vat[3:5]) in (4, 6, 9, 11):
            if int(vat[5:7]) < 1 or int(vat[5:7]) > 30:
                return False

        if int(vat[3:5]) in (1, 3, 5, 7, 8, 10, 12):
            if int(vat[5:7]) < 1 or int(vat[5:7]) > 31:
                return False

        check_sum = (2 * int(vat[0]) + 7 * int(vat[1]) + 9 * int(vat[2]) +
                     1 * int(vat[3]) + 4 * int(vat[4]) + 6 * int(vat[5]) +
                     3 * int(vat[6]) + 5 * int(vat[7]) + 8 * int(vat[8]) +
                     2 * int(vat[9]) + 7 * int(vat[10]) + 9 * int(vat[11]))

        check = check_sum % 11
        if check == 10:
            check = 1

        if check != int(vat[12]):
            return False
        return True

    return False


def sweden(vat):
    '''Check Sweden VAT number.'''
    if len(vat) != 12:
        return False

    try:
        _posint(vat)
    except ValueError:
        return False

    if int(vat[10:12]) <= 0:
        return False

    check_sum = (mult_add(2, int(vat[0])) + int(vat[1]) +
                 mult_add(2, int(vat[2])) + int(vat[3]) +
                 mult_add(2, int(vat[4])) + int(vat[5]) +
                 mult_add(2, int(vat[6])) + int(vat[7]) +
                 mult_add(2, int(vat[8])))

    check = 10 - (check_sum % 10)
    if check == 10:
        check = 0
        if check != int(vat[9]):
            return False
    return True


def slovenia(vat):
    '''Check Slovenia VAT number.'''
    if len(vat) != 8:
        return False

    try:
        _posint(vat)
    except ValueError:
        return False

    if int(vat[0:7]) <= 999999:
        return False

    check_sum = (8 * int(vat[0]) + 7 * int(vat[1]) + 6 * int(vat[2]) +
                 5 * int(vat[3]) + 4 * int(vat[4]) + 3 * int(vat[5]) +
                 2 * int(vat[6]))

    check = 11 - (check_sum % 11)
    if check == 10:
        check = 0

    if check == 11:
        check = 1

    if check != int(vat[7]):
        return False
    return True


def slovakia(vat):
    '''Check Slovakia VAT number.'''
    try:
        _posint(vat)
    except ValueError:
        return False

    if len(vat) not in(9, 10):
        return False

    if int(vat[0:2]) in (0, 10, 20) and len(vat) == 10:
        return True

    if len(vat) == 10:
        if int(vat[0:2]) < 54 or int(vat[0:2]) > 99:
            return False

    if len(vat) == 9:
        if int(vat[0:2]) > 53:
            return False

    if int(vat[2:4]) < 1:
        return False

    if int(vat[2:4]) > 12 and int(vat[2:4]) < 51:
        return False

    if int(vat[2:4]) > 62:
        return False

    if int(vat[2:4]) in (2, 52) and int(vat[0:2]) % 4 > 0:
        if int(vat[4:6]) < 1 or int(vat[4:6]) > 28:
            return False

    if int(vat[2:4]) in (2, 52) and int(vat[0:2]) % 4 == 0:
        if int(vat[4:6]) < 1 or int(vat[4:6]) > 29:
            return False

    if int(vat[2:4]) in (4, 6, 9, 11, 54, 56, 59, 61):
        if int(vat[4:6]) < 1 or int(vat[4:6]) > 30:
            return False

    if int(vat[2:4]) in (1, 3, 5, 7, 8, 10, 12,
                         51, 53, 55, 57, 58, 60, 62):
        if int(vat[4:6]) < 1 or int(vat[4:6]) > 31:
            return False
    return True


def san_marino(vat):
    '''Check San Marino VAT number.'''
    if len(vat) != 5:
        return False

    try:
        _posint(vat)
    except ValueError:
        return False

    return True


def ukraine(vat):
    '''Check Ukraine VAT number.'''
    if len(vat) != 8:
        return False

    try:
        _posint(vat)
    except ValueError:
        return False

    return True


def russia(vat):
    '''Check Russia VAT number.'''
    if len(vat) != 10 and len(vat) != 12:
        return False

    try:
        _posint(vat)
    except ValueError:
        return False

    if len(vat) == 10:
        check_sum = (2 * int(vat[0]) + 4 * int(vat[1]) + 10 * int(vat[2]) +
                     3 * int(vat[3]) + 5 * int(vat[4]) + 9 * int(vat[5]) +
                     4 * int(vat[6]) + 6 * int(vat[7]) + 8 * int(vat[8]))

        check = check_sum % 11
        if check % 10 != int(vat[9]):
            return False

    else:
        check_sum1 = (7 * int(vat[0]) + 2 * int(vat[1]) + 4 * int(vat[2]) +
                      10 * int(vat[3]) + 3 * int(vat[4]) + 5 * int(vat[5]) +
                      9 * int(vat[6]) + 4 * int(vat[7]) + 6 * int(vat[8]) +
                      8 * int(vat[9]))

        check = check_sum1 % 11

        if check != int(vat[10]):
            return False

        check_sum2 = (3 * int(vat[0]) + 7 * int(vat[1]) + 2 * int(vat[2]) +
                      4 * int(vat[3]) + 10 * int(vat[4]) + 3 * int(vat[5]) +
                      5 * int(vat[6]) + 9 * int(vat[7]) + 4 * int(vat[8]) +
                      6 * int(vat[9]) + 8 * int(vat[10]))

        check = check_sum2 % 11
        if check != int(vat[11]):
            return False

    return True
