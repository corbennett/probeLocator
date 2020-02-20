"""Rename this file 'config.py' and make the appropriate changes"""

import os
import logging


directory_list = [r'Z:', r'\\10.128.50.43\sd6.2', r'\\10.128.50.43\sd6']
                  
desired_image_filenames_contain = ['surface-image1', 'surface-image3']


npz_file_suffix = 'ISIregistration.npz'



def get_insertion_image_paths(mouse_number):
    path_list = []
    for directory in directory_list:
        try:
            sessions = os.listdir(directory)
        except Exception as E:
            log_str = 'Failed to find sessions at {}'.format(directory)
            logging.error(log_str)
            sessions = []
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
    npz_filename = get_session_name(file_path)+'.'+npz_file_suffix
    save_path = os.path.join(saveDirectory, npz_filename)
    return save_path

def get_session_name(insertion_image_path):
    session_name = ''
    try:
        session_path = os.path.split(insertion_image_path)[0]
        data_dirname = os.path.split(session_path)[1]
        assert(data_dirname.count('_')==2)
        session_name = data_dirname
    except Exception as E:
        logging.warning('Unable to retrieve an acceptable session_name', exc_info=True)
    return session_name
