def is_filename_char(x):
    if x.isalnum():
        return True
    if x in ['-', '_']:
        return True
    return False

def URL_to_filename(filename):
    return "".join(x for x in filename if is_filename_char(x))
