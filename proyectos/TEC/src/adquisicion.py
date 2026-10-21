# ------------------------------------------------------------------------------
# Carga de módulos
# ------------------------------------------------------------------------------
import json
from machine import Pin, PWM, ADC, SPI, Timer
import math
import cmath
import time
import sys
import uselect
import uasyncio
import _thread
import collections
# ------------------------------------------------------------------------------
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
def get_params_string():
    return [valid_modes.index(params['mode']), params['amplitude'], params['period'], params['offset_A'], params['offset_T']]

def parse_command(cmd):
    global params
    try:
        command = json.loads(cmd)
    except Exception as e:
        print('{"result":"unknown or malformed command"}')
# ------------------------------------------------------------------------------
# Sincronización
# ------------------------------------------------------------------------------
data_lock = _thread.allocate_lock()
fft_lock = _thread.allocate_lock()
# ------------------------------------------------------------------------------
# Bucle principal
# ------------------------------------------------------------------------------
#   1. Espera hasta el siguiente periodo de muestreo (PERIOD_US).
#   2. Genera la siguiente muestra de la señal y la envía a la salida (PWM).
#   3. Lee el valor de la entrada analógica (ADC).
# ------------------------------------------------------------------------------
def wait_next_period(previous):
    lapsed = time.ticks_us() - previous
    offset = -60
    remaining = PERIOD_US - lapsed + offset
    if 0 < lapsed <= PERIOD_US:
        time.sleep_us(remaining)
    return time.ticks_us()

def loop(queue, queue_fft):
    t_last = time.ticks_us()
    t0 = t_last
    while True:
        t = wait_next_period(t_last)
        u = signal((t-t0)*1e-6)
        y = readInput()
        try:
          writeOutput(u)
          led.duty_u16(int(65354*(u)))
        except ValueError:
          pass
        with data_lock:
            queue.append([(t-t0)*1e-6, u, u, y])
        t_last = t
        #print(f'{u} {y}')
        #print(f'{{"topic":"evolution","source":"{SOURCE}","payload":{data}}}')
        #print(f'{{"topic":"reference","source":"{SOURCE}","payload":{get_params_string()}}}')
# ------------------------------------------------------------------------------
# INSTRUCCIONES
# ------------------------------------------------------------------------------
PERIOD_US = 10000 # Periodo de muestreo en microsegundos
PERIOD_S = PERIOD_US*1e-6 # Periodo de muestreo en segundos
DATA_BUFFER_SIZE = 256 # Muestras en el buffer
FFT_BUFFER_SIZE = 64 # Muestras en el buffer


# Especifica la señal.
def signal(t):
  f1 = 10
  f2 = .1
  return 0.5*math.sin(2*math.pi*f1*t) + 0.5*math.sin(2*math.pi*f2*t)
#   return math.exp(-t/10.0)


def nextpow(x):
  return math.ceil(math.log2(x))

def binary_inverse(n, N):
  return int(''.join(reversed(bin(2**(N+1)+n)[-N:])), 2)
 
 
N = FFT_BUFFER_SIZE
WN = cmath.exp(-1j*2*math.pi/N)
def butterfly(x, y, c):
    return x + c*y, x - c*y
    
def fft(x, N):
    m = nextpow(len(x))
    X = [x[binary_inverse(n, m)] for n in range(N)]
    for j in range(m):
        l, p = 2**j, 2**(m-j-1)
        for k in range(p):
            n = k*2*l
            for i in range(l):
                X[n+i], X[n+i+l] = butterfly(X[n+i], X[n+i+l], WN**(p*i))
    return X
    
    
def compute_fft_and_print(t, queue, queue_fft):
    internal_led.toggle()
    q = collections.deque((), N)
    try:
        if len(queue_fft) == N:
            with fft_lock:
                x = [queue_fft.popleft() for i in range(N)]
            X = fft(x, N)
            for i, p in enumerate(X):
                #print(i/N/PERIOD_S, 10*math.log10(abs(p)**2 / N * PERIOD_S))
                print(10*math.log10(abs(p)**2 / N * PERIOD_S))
                if i > N/2: break
    except Exception as e:
        print('Buffer underrun')
        #print (e)


def log(t, queue_in, queue_fft):
#     spoll = uselect.poll()
#     spoll.register(sys.stdin, uselect.POLLIN)
#         if spoll.poll(0):
#             cmd = str(sys.stdin.readline())
#             parse_command(cmd)
    
    while queue_in:
        with data_lock:
            x = queue_in.popleft()
        if not fft_lock.locked():
            queue_fft.append(x[2])
#        print(f'{x[2]} {x[3]}')
# ------------------------------------------------------------------------------
# Comienza la ejecución
# ------------------------------------------------------------------------------

q_data = collections.deque((), DATA_BUFFER_SIZE)
q_fft = collections.deque((), FFT_BUFFER_SIZE)
_thread.start_new_thread(loop, (q_data, q_fft))

period_fft = int(FFT_BUFFER_SIZE*PERIOD_US/1000.0)
period_log = int(10*PERIOD_US/1000.0)

tim1 = Timer(period=1000, mode=Timer.PERIODIC, callback=lambda t: compute_fft_and_print(t, q_data, q_fft))
tim2 = Timer(period=period_log, mode=Timer.PERIODIC, callback=lambda t: log(t, q_data, q_fft))
