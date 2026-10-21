function iniciar()
% Prepara el entorno: en Octave carga el paquete signal (pkg install -forge signal).
% En Matlab hace falta la Signal Processing Toolbox.
if exist('OCTAVE_VERSION', 'builtin')
    pkg load signal
end
if ~exist('figuras', 'dir'), mkdir('figuras'); end
end
