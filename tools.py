import os
import settings as s
import numpy as np

"""
File with commonly used functions.
"""

def read_from_file():
    '''
    Reads all solved network files in the 'nodes_folder' set in 'settings.py'.
    Returns a list of dictionaries with the values from the files in the form:
        [{'c':'u', 'f':'s', 'a':1.00, 'g':1.00, 'b':1.00},
            {'c':'c', 'f':'s', 'a':1.00, 'g':1.00, 'b':1.00}]
    '''
    filename_list = os.listdir(s.nodes_folder)
    all_combinations = []
    for name in filename_list:
        all_combinations.append({'c':name[0],
                                 'f':name[2],
                                 'a':float(name[5:9]),
                                 'g':float(name[11:15]),
                                 'b':float(name[17:21])})
    return all_combinations


def get_chosen_combinations(**kwargs):
    '''
    Function that extracts the wanted files in the 'self.all_combinations list'.

    To choose all the solved networks in the synchronized flow scheme:
        "self.get_chosen_combinations(f='s')".

    All unconstrained networks with a gamma = 1.00 can be found by:
        self.get_chosen_combinations(c='u', g=1.00)

    returns a list of dictionaries with the desired values.
    For instance:
        [{'c':'u', 'f':'s', 'a':1.00, 'g':1.00, 'b':1.00},
            {'c':'c', 'f':'s', 'a':0.80, 'g':1.00, 'b':0.50}
            ...]
    '''
    def _check_in_dict(dic, kwargs):
        """ Check if values are present in a dictionary.

        Args:
            dic: dictionary to check in.
            kwargs: the keyword arguments to check for in the dictionary.
        Returns:
            boolean: True if all values are present in the dictionary, False if any are not.
        """
        for (name, value) in kwargs.items():
            value = np.array(value)
            if not dic[name] in value:
                return False
        return True

    chosen_combinations = []
    # Checking all combinations.
    for combination in read_from_file():

        if _check_in_dict(combination, kwargs):
            chosen_combinations.append(combination)

    if len(chosen_combinations) == 0:
        # Raise error if no chosen combinations are found.
        raise ValueError('No files with {0} found!'.format(kwargs))
    return chosen_combinations


def quantile(quantile, dataset):
    """
    Docstring for quantile.
    Args:
        quantile [float]: the desired quantile eg. 0.99.
        dataset [list/1-dimensional array]: a timeseries.
    """
    return np.sort(dataset)[int(round(quantile*len(dataset)))]


def storage_size(backup_timeseries, q=0.99):
    """
    Docstring
    """
    q = quantile(q, backup_timeseries)
    storage = backup_timeseries - q
    for index, val in enumerate(storage):
        if index == 0:
            if storage[index] < 0:
                storage[index] = 0
        else:
            storage[index] += storage[index - 1]
            if storage[index] < 0:
                storage[index] = 0
    return max(storage)

def get_remote_figures():
    if not os.path.exists(s.remote_figures):
        os.mkdir(s.remote_figures)
    """Copy figures from the result-folder on a remote server"""
    os.system('scp -r {0}. {1}'.format(s.remote_figures_folder, s.remote_figures))
    return