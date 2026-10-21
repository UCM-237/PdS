Velocidad de referencia del atleta (mediana de v en carrera): 10.16 km/h

## Resultados sobre las sesiones reales

| Actividad   | Tramos andando/parado (min)   |   Cambios ritmo (seg. binaria) | Instantes (min)              |   Cambios derivada+MAD |   Muestras > umbral (main.py) |   Repeticiones | Clase        | Etiqueta manual   | Motivo                                      |
|:------------|:------------------------------|-------------------------------:|:-----------------------------|-----------------------:|------------------------------:|---------------:|:-------------|:------------------|:--------------------------------------------|
| 2026-01-07  | 48.5-49.7                     |                              5 | 1.1, 2.5, 36.9, 42.3, 48.5   |                      1 |                            11 |              1 | Rodaje       | Rodaje            | v = 10.0 km/h, 58 % en Z4-Z5                |
| 2026-01-09  | -                             |                              3 | 0.7, 1.5, 2.6                |                      1 |                            10 |              0 | Tempo        | Tempo             | v = 11.2 km/h (> 105 % ref.), 76 % en Z4-Z5 |
| 2026-01-11  | 88.9-91.1                     |                              5 | 28.3, 29.3, 80.9, 81.8, 88.9 |                      1 |                            19 |              2 | Tirada larga | Tirada larga      | 15.1 km                                     |
| 2026-01-14  | -                             |                              3 | 1.0, 2.5, 25.9               |                      1 |                            19 |              0 | Tempo        | Tempo             | v = 11.3 km/h (> 105 % ref.), 63 % en Z4-Z5 |
| 2026-01-15  | 56.7-58.5                     |                              5 | 0.7, 43.6, 45.1, 56.7, 57.4  |                      4 |                            21 |              0 | Rodaje       | Rodaje            | v = 9.6 km/h, 9 % en Z4-Z5                  |


## Validacion de cambios de ritmo (30 sesiones sinteticas, tolerancia 20 s)

| metodo               |   TP |   FP |   FN |   precision |   sensibilidad |    F1 |   error medio (s) |
|:---------------------|-----:|-----:|-----:|------------:|---------------:|------:|------------------:|
| Derivada + MAD       |  223 |    0 |  175 |       1     |          0.56  | 0.718 |             5.267 |
| Segmentacion binaria |  395 |   63 |    3 |       0.862 |          0.992 | 0.923 |             4.493 |


### F1 medio segun el ruido (sigma, km/h)

| metodo               |   0.5 |   1.0 |   1.5 |
|:---------------------|------:|------:|------:|
| Derivada + MAD       |  0.99 |  0.6  |  0.21 |
| Segmentacion binaria |  0.98 |  0.92 |  0.88 |


## Matriz de confusion del clasificador de sesion (30 sinteticas)

| real         |   Rodaje |   Series |   Tirada larga |
|:-------------|---------:|---------:|---------------:|
| Rodaje       |       10 |        0 |              0 |
| Series       |        0 |       10 |              0 |
| Tirada larga |        0 |        0 |             10 |

