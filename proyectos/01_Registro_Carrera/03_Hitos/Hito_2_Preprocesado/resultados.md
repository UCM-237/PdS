## Validacion de filtros (20 sesiones sinteticas)

| filtro                            |   RMSE (km/h) |   retardo (s) |
|:----------------------------------|--------------:|--------------:|
| EMA tau=10 s (main.py)            |          1.32 |          9    |
| EMA tau=30 s                      |          1.81 |         20.3  |
| Mediana 61 s                      |          0.8  |          2.1  |
| Butterworth fc=1/60 Hz (filtfilt) |          0.93 |          2.25 |
| Sin filtrar                       |        nan    |          0    |


## Ruido de la velocidad y correccion de distancia

| Actividad   |   sigma residuo (km/h) |   autocorrelacion lag 1 |   Distancia Strava (m) |   Distancia corregida (m) |
|:------------|-----------------------:|------------------------:|-----------------------:|--------------------------:|
| 2026-01-07  |                   0.96 |                    0.38 |                   8123 |                      8123 |
| 2026-01-09  |                   1.03 |                    0.32 |                   5052 |                      4956 |
| 2026-01-11  |                   0.88 |                    0.41 |                  15138 |                     15138 |
| 2026-01-14  |                   1.07 |                    0.43 |                   5005 |                      5005 |
| 2026-01-15  |                   0.81 |                    0.35 |                   9133 |                      9133 |


## Desnivel positivo segun el tratamiento

| Actividad   |   Suma dh>0 bruta (m) |   Filtrada, sin histeresis (m) |   Filtrada + histeresis 1 m (m) |
|:------------|----------------------:|-------------------------------:|--------------------------------:|
| 2026-01-07  |                  36.7 |                           31.2 |                            22.3 |
| 2026-01-09  |                  23.5 |                           17.2 |                            10.2 |
| 2026-01-11  |                  81.6 |                           74.1 |                            61.3 |
| 2026-01-14  |                  22   |                           16.1 |                            11.2 |
| 2026-01-15  |                  51.5 |                           43.7 |                            33.7 |

