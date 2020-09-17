"""Rename this file 'config.py' and make the appropriate changes"""

import os
import logging


directory_list = [r'\\w10DTSM18306\neuropixels_data', r'\\w10DTSM112719\neuropixels_data', r'Z:'],# r'\\10.128.50.43\sd6.2', r'\\10.128.50.43\sd6', r'\\10.128.50.43\sd6.3', r'\\10.128.50.43\sd6.3\habituation']#r'Z:', r'\\10.128.50.43\sd6.2', r'\\10.128.50.43\sd6', 112719
                  
desired_image_filenames_contain = ['surface-image1']#, 'surface-image1']


npz_file_suffix = 'ISIregistration.npz'



def get_insertion_image_paths(mouse_number, desired_image_filenames_contain=desired_image_filenames_contain):
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


def get_warped_image_from_day1(d2_insertion_image_path):

    session_dir = os.path.dirname(d2_insertion_image_path)
    session_base = os.path.basename(d2_insertion_image_path)

    parent_dir = os.path.dirname(session_dir)

    try:
        mouseID = session_base.split('_')[1]
        date = session_base.split('_')[2]

        other_dirs = os.listdir(parent_dir)
        other_dirs = [o for o in other_dirs if os.path.isdir(os.path.join(parent_dir,o))]

        #find putative day 1 directory
        day1_dir_candidates = [o for o in other_dirs if (mouseID in o) and (int(o.split('_')[2])<int(date))] # has mouse ID and comes from earlier session
        day1_candidate_dates = [int(d.split('_')[2]) for d in day1_dir_candidates]
        
        day1_dir = [d for d in day1_dir_candidates if str(max(day1_candidate_dates)) in d] #take the most recent of these
        day1_dir = os.path.join(parent_dir, day1_dir[0])

        #look for warped image in day 1 directory
        day1_files = os.listdir(day1_dir)
        warped_insertion_image_file = [w for w in day1_files if 'warpedInsertionImage' in w]
        if len(warped_insertion_image_file)==0:
            logging.warning('Could not find day 1 warped insertion image. Please override path to this image if it exists')
            return
        else:
            warped_insertion_image_file = os.path.join(day1_dir, warped_insertion_image_file[0])

    except Exception as E:
        logging.warning('Could not find day 1 data directory', exc_info=True)
        warped_insertion_image_file = ''

    return warped_insertion_image_file

