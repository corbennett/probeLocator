import os
import logging


directory_list = [r"\\10.128.50.77\sd5", r"\\10.128.50.77\sd5.2", r"\\10.128.50.77\sd5.3", r"\\10.128.50.151\sd4", r"\\10.128.50.151\sd4.2"]
                  
filename_string = 'surface-image3'



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
                for filename in os.lisdir(session_path):
                    if (mouse_number in filename) and (filename_string in filename):
                        path_list.append(session_path)

    return path_list


def get_save_path(file_path):
    save_dir = os.path.dirname(file_path)
    save_path = os.path.join(saveDirectory, 'ISIregistration.npz')
    return save_path
