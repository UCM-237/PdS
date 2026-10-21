# ------------------------------------------------------------------------------
# Carga de módulos
# ------------------------------------------------------------------------------
from machine import Pin, PWM, ADC, SPI, Timer
import math
import cmath
import collections
import json
import time
import sys
import uselect
import _thread
# ------------------------------------------------------------------------------
# Configuración de entrada/salida 
# ------------------------------------------------------------------------------
SOURCE = 'Procesamiento de Señales'
internal_led = Pin(25, Pin.OUT)
led = PWM(Pin(16))
signal_in = ADC(26)
signal_out = PWM(Pin(14))
signal_out.freq(10000)
# ------------------------------------------------------------------------------
# ADC
# ------------------------------------------------------------------------------
def read_input() -> float:
    '''Lee el valor de la entrada analógica (signal_in)'''
    return signal_in.read_u16() # Poner aquí la conversión
# ------------------------------------------------------------------------------
# DAC
# ------------------------------------------------------------------------------
def write_output(value: float) -> None:
    '''Escrribe un valor en la salida PWM (signal_out)'''
    duty = int(value) # Poner aquí la conversión de salida int(...)
    signal_out.duty_u16(duty)
# ------------------------------------------------------------------------------
# Comunicación serie
# ------------------------------------------------------------------------------
def parse_command(cmd):
    try:
        command = json.loads(cmd)
        # Pon aquí el código que interpreta y ejecuta la orden
    except Exception as e:
        print('{"error":"orden incorrecta o desconocida"}')
# ------------------------------------------------------------------------------
# Sincronización
# ------------------------------------------------------------------------------
data_lock = _thread.allocate_lock()
SAMPLING_PERIOD_US = 10000 # Periodo de muestreo en microsegundos
SAMPLING_PERIOD_S = SAMPLING_PERIOD_US*1e-6 # Periodo de muestreo en segundos
DATA_BUFFER_SIZE = 256 # Muestras en el buffer


def wait_next_period(previous):
    now = time.ticks_us()
    lapsed = now - previous
    offset = -0
    remaining = SAMPLING_PERIOD_US - lapsed + offset
    if 0 < lapsed <= SAMPLING_PERIOD_US:
        time.sleep_us(remaining)
    return now

# Especifica la señal.
def signal(t):
  f1 = 10
  f2 = .1
  return 0.5*math.sin(2*math.pi*f1*t) + 0.5*math.sin(2*math.pi*f2*t)
#   return math.exp(-t/10.0)

def sampling_loop(queue):
    '''Bucle de adquisición y generación
       ---------------------------------
       1. Espera hasta el siguiente periodo de muestreo (PERIOD_US).
       2. Lee el valor de la entrada analógica (ADC).
       3. Genera la siguiente muestra de la señal y la envía a la salida (PWM).
    '''
    t_last = time.ticks_us()
    t0 = t_last
    print('Inicia hilo de muestreo.')
    i = 0
    while True:
        t = wait_next_period(t_last)
        u = signal((t-t0)*1e-6)
        y = read_input()
        write_output(u)
        t_last = t
        with data_lock:
            queue.append([(t-t0)*1e-6, (t-t_last)/1000, u, y])
        #t_last = t
# ---------------------d---------------------------------------------------------
# INSTRUCCIONES
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Hilo 1 - sampling_loop
# ------------------------------------------------------------------------------
q_data = collections.deque((), DATA_BUFFER_SIZE)
_thread.start_new_thread(sampling_loop, (q_data,))

# ------------------------------------------------------------------------------
# Hilo 2 - log
# ------------------------------------------------------------------------------
def logging(t, queue_in):
    spoll = uselect.poll()
    spoll.register(sys.stdin, uselect.POLLIN)
    if spoll.poll(0):
        cmd = str(sys.stdin.readline())
        parse_command(cmd)
    
    internal_led.toggle()
    while queue_in:
        with data_lock:
            x = queue_in.popleft()
        print(f'{x[1]}')


LOGGING_PERIOD_S = int(100*SAMPLING_PERIOD_US/1000.0)
tim1 = Timer(period=LOGGING_PERIOD_S, mode=Timer.PERIODIC, callback=lambda t: logging(t, q_data))
