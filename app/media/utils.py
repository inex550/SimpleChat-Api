from os import path


base_img_path = path.join('.', 'res', 'img')


def async_file(filepath):
    with open(filepath, 'rb') as file:
        yield from file