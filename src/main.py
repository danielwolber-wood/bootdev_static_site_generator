import pathlib
import shutil


def main():
    source_dir = pathlib.Path("./static")
    destination_dir = pathlib.Path("./public")

    shutil.rmtree(destination_dir)
    shutil.copytree(source_dir, destination_dir)

if __name__ == '__main__':
    main()