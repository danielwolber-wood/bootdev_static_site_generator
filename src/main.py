from utils import generate_page
import pathlib
import shutil
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--static", type=pathlib.Path, default="./static")
    parser.add_argument("--content", type=pathlib.Path, default="./content")
    parser.add_argument("--destination", type=pathlib.Path, default="./docs")
    parser.add_argument("--template", type=pathlib.Path, default="./template.html")
    parser.add_argument("--basepath", type=str, default="/")

    args = parser.parse_args()
    static_dir = args.static
    destination_dir = args.destination
    template_path = args.template
    content_dir = args.content
    basepath = args.basepath

    shutil.rmtree(destination_dir)
    shutil.copytree(static_dir, destination_dir)

    md_files = [f for f in content_dir.rglob("*.md")]
    for file in md_files:
        path_inside_content_dir = file.relative_to(content_dir)
        output_path = destination_dir / path_inside_content_dir
        print(f"{file} -> {output_path}")
        print(f'destination_dir is {destination_dir}')
        generate_page(from_path=file,template_path=template_path, dest_path=output_path.with_suffix(".html"), basepath=basepath)



if __name__ == '__main__':
    main()