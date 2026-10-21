from scipy import signal

RC = 1e-3                      # 1 kΩ, 1 µF
H = signal.TransferFunction([1], [RC, 1])
print("polos:", H.poles)       # [-1000.]
t, s = signal.step(H)          # escalón
W, mag, fase = signal.bode(H)  # dB, grados
