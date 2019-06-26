
import numpy as np
import logging


def points_from_path(path, *args):
    count = 0
    points = np.empty(2,1)
    if not(os.path.isdir(directory_path):
        path = os.path.isdir(os.path.split(path)[0])
    for filename in os.lisdir(path):
        if os.path.splittext(filename)[1]==npz:
            count += 1
            npz_file = np.load(os.path.join(directory_path, filename)
            for array_name in npz_file.files:
                match = True
                for arg in args:
                    if not(arg in filename):
                        match = False
                if match:
                    points = np.stack(points, npz_file[array_name])
    if count>1:
        log_str = 'Found more than 1 npz file in {}, something might be wrong'.format(path)
        logging.warning(log_str)
    return points
