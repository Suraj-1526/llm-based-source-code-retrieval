import os
from config import REPOSITORIES
from utils import get_files


def clone_repositories():
    if os.path.exists("repositories"):
        print("Repositories already cloned")
        return
    else:
        for repo in REPOSITORIES:
            print(f"Cloning {repo}")
            os.system(f"git clone {repo} repositories/{repo.split('/')[-1]} --depth 1")
            print(f"Cloned {repo}")
        print("Cloned all repositories")


if __name__ == "__main__":
    clone_repositories()
    files = get_files()
    print(files)
    print("Done")
