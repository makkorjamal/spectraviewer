import numpy as np
import os
def read_cal_spec(path):

    with open(os.path.join(path)) as f:
        lines = f.readlines()
    wl_line = np.fromstring(lines[3], dtype = float, sep = '\t')
    wl_line = wl_line.astype(float)
    spec = np.array(lines[4:])
    spec = spec.astype(float)
    wavelength = np.linspace(wl_line[0], wl_line[1], int(wl_line[3]))
    return spec, wavelength

if __name__ == '__main__':
   print('Hello')