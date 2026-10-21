# Código de partida (Matlab / Octave)

Ejecuta los scripts desde esta carpeta: `hito1`, `hito2`, …

- Funciona en Matlab (con Signal Processing Toolbox) y en Octave (con el paquete `signal`: `pkg install -forge signal`).
- `cargar`, `snr_db`, `alinear`, `espectro`: lectura del audio, SNR, compensación de retardo y espectro en dB.
- `psd_welch`: PSD de Welch. Se da hecha porque `pwelch` recibe el solape de forma distinta en Matlab y en Octave.
- `mi_stft`, `mi_istft`: STFT con ventana de Hann y 75 % de solape, y su inversa, iguales en Matlab y en Octave.
- `hito1.m` … `hito4.m`: un esqueleto por hito. Se ejecutan tal cual y dejan marcado con `TODO` lo que tienes que completar.
- Las figuras se guardan en `figuras/`.
