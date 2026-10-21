# ------------------------------------------------------------------------------
## Carga de módulos
# ------------------------------------------------------------------------------
import json
from machine import Pin, PWM, ADC, SPI, Timer
import math
import time
import sys
import uselect
# ------------------------------------------------------------------------------
SOURCE = 'Procesamiento de Señales'
# ------------------------------------------------------------------------------
# Configuración de entrada/salida 
# ------------------------------------------------------------------------------
led = PWM(Pin(14))
signal_in = ADC(26)
signal_out = PWM(Pin(14))
signal_out.freq(10000)

# ------------------------------------------------------------------------------
# ADC
# ------------------------------------------------------------------------------
IN1_OFFSET = -1
IN1_GAIN = 2.0

def readInput():
    return -(IN1_OFFSET + IN1_GAIN*signal_in.read_u16() / 65535)
# ------------------------------------------------------------------------------
# DAC
# ------------------------------------------------------------------------------
OUT1_OFFSET = 32767
OUT1_GAIN = 32763
def writeOutput(value: int):
    '''Write output to DAC '''
    duty = int(OUT1_GAIN*value + OUT1_OFFSET)
    signal_out.duty_u16(duty)
# ------------------------------------------------------------------------------
# Comunicación serie
# ------------------------------------------------------------------------------
def parse_command(cmd):
    global params
    try:
        command = json.loads(cmd)
        # Escribe aquí el código para interpretar las órdenes recibidas
    except Exception as e:
        print('{"result":"unknown or malformed command"}')
# ------------------------------------------------------------------------------
# Bucle principal
# ------------------------------------------------------------------------------
#   1. Espera hasta el siguiente periodo de muestreo (PERIOD_US).
#   2. Genera la siguiente muestra de la señal y la envía a la salida (PWM).
#   3. Lee el valor de la entrada analógica (ADC).
# ------------------------------------------------------------------------------
def waitNextPeriod(previous):
    lapsed = time.ticks_us() - previous
    offset = -60
    remaining = PERIOD_US - lapsed + offset
    if 0 < lapsed <= PERIOD_US:
        time.sleep_us(remaining)
    return time.ticks_us()

def loop():
    state = []
    tLast = time.ticks_us()
    t0 = tLast
    spoll = uselect.poll()
    spoll.register(sys.stdin, uselect.POLLIN)
    while True:
        data = []
        for i in range(BUFFER_SIZE):
            t = waitNextPeriod(tLast)
            u = signal((t-t0)*1e-6)
            y = readInput()
            try:
              writeOutput(u)
              led.duty_u16(int(65354*(u)))
            except ValueError:
              pass
            data.append([(t-t0)*1e-6, u, y])
            tLast = t
        if spoll.poll(0):
            cmd = str(sys.stdin.readline())
            parse_command(cmd)
        print(f'{u} {y}')
# ------------------------------------------------------------------------------
# INSTRUCCIONES
# ------------------------------------------------------------------------------
PERIOD_US = 1000 # Periodo de muestreo en microsegundos
BUFFER_SIZE = 10 # Muestras en el buffer

def signal(t):
  # Pon aquí el código necesario para generar tu señal.
  return 1

# ------------------------------------------------------------------------------
# Comienza la ejecución
# ------------------------------------------------------------------------------
loop()
