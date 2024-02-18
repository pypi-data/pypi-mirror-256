"""Helper classes / functions for the parsing of numbers.

"""



def _parse_number(number):
    if isinstance(number, str):
        return number
    else:
        try:
            if int(number) == number:
                return str(int(number))
            else:
                return str(number)
        except ValueError:
            raise ValueError("number must be a string or a number.")
