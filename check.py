import os
import itertools
import functools

lst = [
    '/home/dudko/Projects/cleanup scripts/data/Jan-26-18/SAFETY/RESULTS/Result_Summary.txt',
    '/home/dudko/Projects/cleanup scripts/data/Jan-27-18/SAFETY/RESULTS/Result_Summary.txt',
    '/home/dudko/Projects/cleanup scripts/data/Mar-06-18/SAFETY/RESULTS/Result_Summary.txt',
    '/home/dudko/Projects/cleanup scripts/data/Nov-24-17/LCD/equipment_list/equipment_list.txt',
]


def find_common_string(lst):

    def match(x, y):

        matched = ""

        for a, b in zip(x, y):
            if a == b:
                matched += a
                continue

            else:
                return matched

        return matched

    return reduce(match, lst)


def accumulate(iterable, func, optional_concat=None):

    it = iter(iterable)

    try:
        total = next(it)

    except StopIteration:
        return

    if not optional_concat:
        yield total

    else:
        yield optional_concat+total

    for element in it:
        total = func(total, element)
        yield total


def check_permissions(files):

    # Get rid of the file name in path
    dirs_to_check_string = []

    for file_ in files:
        temp = file_.split(os.sep)
        parent_index = len(temp) - 1
        dirs_to_check_string.append(os.sep.join(temp[:parent_index]))

    # Find the common string among them
    # common_string = find_common_string(dirs_to_check_string)

    # In Python2 os.access doesn't take keyword arguments, come up with a workaround
    _access = os.access
    access = lambda path, mode: _access(path, mode)

    # Create a partial function that checks for access permission
    access_func = functools.partial(access, mode=os.X_OK)

    # Create concatenate functionality
    concat = lambda x, y: x+os.sep+y

    dirs_to_check_split = []

    for dir_ in dirs_to_check_string:

        for c in accumulate(dir_.split(os.sep), concat, os.sep):
            print c
            print access_func(c)

    return True


if __name__ == "__main__":
    check_permissions(files=lst)
