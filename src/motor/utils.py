def float_to_uint(value: float, range_min: float, range_max: float, bits: int) -> int:
    """
    Converts a floating-point number into an unsigned integer with a specified bit depth while respecting a given range.

    For example: If you call float_to_uint(0.5, 0.0, 1.0, 8):
      - You're converting 0.5 in the range [0.0, 1.0] to an 8-bit integer
      - It would return 127, which is halfway between 0 and 255
    """
    span = range_max - range_min
    offset = range_min
    if value > range_max:
        value = range_max
    elif value < range_min:
        value = range_min
    return int((value - offset) * ((1 << bits) - 1) / span)


def uint_to_float(value: int, value_min: float, value_max: float) -> float:
    """
    This is the opposite of float_to_uint. It takes an unsigned integer received from the CAN bus and
    converts it back into a floating point number
    """
    int_max = 0xFFFF
    span = value_max - value_min
    return value / int_max * span + value_min
