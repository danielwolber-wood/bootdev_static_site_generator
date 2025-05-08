from utils import generate_page
import pathlib
import shutil


def main():
    source_dir = pathlib.Path("./static")
    destination_dir = pathlib.Path("./public")

    shutil.rmtree(destination_dir)
    shutil.copytree(source_dir, destination_dir)
    """TEST
    page_source = pathlib.Path("content/index.md")
    page_template = pathlib.Path("template.html")
    page_dest = pathlib.Path("public/index.md")
    generate_page(from_path=page_source, dest_path=page_dest, template_path=page_template)
    """

    template_path = pathlib.Path("template.html")
    content_dir = pathlib.Path("./content")
    md_files = [f for f in content_dir.rglob("*.md")]
    for file in md_files:
        path_inside_content_dir = file.relative_to(content_dir)
        output_path = destination_dir / path_inside_content_dir
        print(f"{file} -> {output_path}")
        generate_page(from_path=file,template_path=template_path, dest_path=output_path.with_suffix(".html"))



if __name__ == '__main__':
    main()