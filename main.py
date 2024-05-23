import shutil, os
from src.utils.markdown import markdown_to_html


def copy_files(src, dest):
    files_to_be_removed = filecrawler(dest)
    files_to_be_removed = sorted(files_to_be_removed, key=lambda x: x[1], reverse=True)

    files_to_be_copied = filecrawler(src)

    for filepath, filetype in files_to_be_removed:
        print("deleting: ", filepath)
        if filetype == "dir":
            os.rmdir(filepath)
        else:
            os.remove(filepath)
    
    for filepath, filetype in files_to_be_copied:
        print("copying: ", filepath)
        if filetype == "dir":
            os.makedirs(filepath.replace(src, dest), exist_ok=True)
        else:
            shutil.copy(filepath, filepath.replace(src, dest))

def filecrawler(path):
    paths = []
    for filename in os.listdir(path):
        if os.path.isdir(os.path.join(path, filename)):
            paths.append((os.path.join(path, filename), "dir"))
            paths.extend(filecrawler(os.path.join(path, filename)))
        else:
            paths.append((os.path.join(path, filename), "file"))
    return paths

def extract_title(markdown: str) -> str:
    # we can use the functionality that we have already implemented
    # but I'll implement a one-liner for this, cuz' they look cool.
    try: # split document to lines, filter the lines that start with "# "
         # the `filter` returns an iterator, so you can't index it but get the next element using `next`
         # return the characters after the first two characters of the line using `[2:]`
        return next(filter(lambda x: x.startswith("# "), markdown.split("\n")))[2:] 
    except: # it'll also raise an exception if there is no h1 element
        raise Exception("No title found in the markdown file")

def generate_path_recursive(from_path, template_path, dest_path):
    source_files = filecrawler(from_path)
    for source_file, filetype in source_files:
        if filetype == "file":
            generate_page(source_file, template_path, source_file.replace(from_path, dest_path).replace(".md", ".html"))
        else:
            os.makedirs(source_file.replace(from_path, dest_path), exist_ok=True)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        markdown_content = file.read()
    with open(template_path, "r") as f:
        template_content = f.read()

    title = extract_title(markdown_content)
    # now we can also convert the markdown content to blocks
    htmlnode = markdown_to_html(markdown_content)
    htmlcode = htmlnode.to_html()
    # replace the title and content placeholders in the template
    template_content = template_content.replace("{{ title }}", title).replace("{{ content }}", htmlcode)
    with open(dest_path, "w") as f:
        f.write(template_content)
    print(f"Page generated successfully at {dest_path}")
    return


def main():
    generate_path_recursive("content", "template.html", "static")
    copy_files("static", "public")
    print("Copied files from `static` to `public`")


if __name__ == "__main__":
    main()