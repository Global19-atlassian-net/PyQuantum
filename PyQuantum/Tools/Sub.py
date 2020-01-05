SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def sub(s):
    return s.translate(SUB)
