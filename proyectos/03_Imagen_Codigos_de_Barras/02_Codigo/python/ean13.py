"""Codificación EAN-13 (compartida por el generador y la solución)."""
L = ["0001101", "0011001", "0010011", "0111101", "0100011",
     "0110001", "0101111", "0111011", "0110111", "0001011"]
G = [c[::-1] for c in ["1110010", "1100110", "1101100", "1000010", "1011100",
                       "1001110", "1010000", "1000100", "1001000", "1110100"]]
R = ["1110010", "1100110", "1101100", "1000010", "1011100",
     "1001110", "1010000", "1000100", "1001000", "1110100"]
PARIDAD = ["LLLLLL", "LLGLGG", "LLGGLG", "LLGGGL", "LGLLGG",
           "LGGLLG", "LGGGLL", "LGLGLG", "LGLGGL", "LGGLGL"]


def digito_control(d12):
    s = sum(int(c) * (3 if i % 2 else 1) for i, c in enumerate(d12))
    return str((10 - s % 10) % 10)


def modulos(codigo):
    """Cadena de 95 módulos ('1' = barra) de un EAN-13 de 13 cifras."""
    assert len(codigo) == 13 and codigo[12] == digito_control(codigo[:12])
    par = PARIDAD[int(codigo[0])]
    s = "101"
    for c, p in zip(codigo[1:7], par):
        s += (L if p == "L" else G)[int(c)]
    s += "01010"
    for c in codigo[7:]:
        s += R[int(c)]
    return s + "101"


def anchos(patron):
    """Longitudes de las rachas de una cadena de módulos (empezando por el primer carácter)."""
    out, n = [], 1
    for a, b in zip(patron, patron[1:]):
        if a == b:
            n += 1
        else:
            out.append(n)
            n = 1
    return out + [n]
