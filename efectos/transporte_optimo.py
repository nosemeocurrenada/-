import sys
from time import time
import librosa
import ot
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

SR = 48000
NFFT = 1024 * 4
VERBOSE = True
VENTANA = "blackman"
METRIC = "cityblock"

source = "retro_loop.wav"
target = "whoosh1.wav"
outfile= "test_rlo.wav"

def transport(espectro_c, espectro_o):
    a = espectro_c @ np.ones(np.shape(espectro_c)[1])
    b = espectro_o @ np.ones(np.shape(espectro_o)[1])
    n = len(a)
    a /= np.sum(a)
    b /= np.sum(b)
    T_mat = ot.emd_1d(a, b, a, b, metric="minkowski", p=2)
    print("Transporte óptimo resuelto")

    return T_mat.transpose() @ espectro_c

class T:
    pass
t = T()
t.inicial = None
t.ultimo = None
def print_benchmark(msg):
    total = time() - t.inicial
    dt = time() - t.ultimo
    print(msg, '\t', f'dt:{dt:.2f}', '\t', f'total:{total:.2f}')

def do_magic(source, target):
    carrier, _ = librosa.load(source, sr=SR)
    objetivo, _ = librosa.load(target, sr=SR)

    espectro_1 = np.abs(  # espectro[i,j] es la componente de la i-ésima banda de frecuencia en el tiempo j.
        librosa.stft(
            carrier,
            n_fft=NFFT,
            hop_length=512,
            window=VENTANA,
            center=True,
        )
    )
    print_benchmark('Espectro 1 calculado')

    espectro_2 = np.abs(
        librosa.stft(
            objetivo,
            n_fft=NFFT,
            hop_length=512,
            window=VENTANA,
            center=True,
        )
    )
    print_benchmark('Espectro 2 calculado')

    A = transport(espectro_1, espectro_2)
    print_benchmark('Transformacion aplicada')
    return librosa.griffinlim(
        200 * A / np.max(A),
        n_fft=NFFT,
        hop_length=512,
        window=VENTANA,
        center=True,
    )

def main(source, target, outfile):
    t.inicial = time()
    t.ultimo = time()
    audio_reconstruido = do_magic(source,target)
    print("Audio reconstruido")
    wavfile.write(outfile, SR, audio_reconstruido)
    print_benchmark(f'Guardado en {outfile}')

# Exige uso desde la consola via
#   python efecto.py <source> <target> <salida>
# Puede comentarse si molesta
if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) != 4:
        print('Usage:')
        print(f'\t{sys.argv[0]} source target outfile')
        exit(0)

    (source, target, outfile) = sys.argv[1:]
    main(source,target,outfile)