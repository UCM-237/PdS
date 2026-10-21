function iniciar()
% Prepara el entorno. No hace falta ninguna toolbox; en Octave, si está instalado el paquete
% signal, se carga (útil para freqz).
if exist('OCTAVE_VERSION', 'builtin')
    try
        pkg load signal
    catch
    end
end
if ~exist('figuras', 'dir'), mkdir('figuras'); end
end
