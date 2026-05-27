import os
from config import ACCEPTED_LANGUAGES, EXCLUDE_FOLDER


def get_files():
    files = []

    for root, dirs, filenames in os.walk("repositories"):
        for exclude in EXCLUDE_FOLDER:
            if exclude in dirs:
                dirs.remove(exclude)

        for filename in filenames:
            if filename.split(".")[-1] in ACCEPTED_LANGUAGES:
                files.append(os.path.join(root, filename))

    return files