"""Rename this file 'config.py' and make the appropriate changes"""

import os
import logging


directory_list = []
                  
desired_image_filenames_contain = ['surface-image3']


npz_filename = 'ISIregistration.npz'



def get_insertion_image_paths(mouse_number):
    path_list = []
    for directory in directory_list:
        try:
            sessions = os.listdir(directory)
        except Exception as E:
            log_str = 'Failed to find sessions at {}'.format(directory)
            logging.warning(log_str)
            sessionts = []
        for session_dir in sessions:
            if mouse_number in session_dir:
                session_path = os.path.join(directory, session_dir)
                for filename in os.listdir(session_path):
                    match = False
                    for sub_string in desired_image_filenames_contain:
                        if sub_string in filename:
                            match = True
                    if (mouse_number in filename) and match:
                        path_list.append(os.path.join(session_path, filename))

    return path_list


def get_save_path(file_path):
    saveDirectory = os.path.dirname(file_path)
    save_path = os.path.join(saveDirectory, npz_filename)
    return save_path
