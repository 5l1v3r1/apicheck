"""
This file build the documentation for APICheck
"""
import os
import json
import hashlib
import configparser

HERE = os.path.abspath(os.path.dirname(__file__))

DOC_PATH = os.path.join(HERE, "docs")
TOOLS_PATH = os.path.join(HERE, "tools")
STATIC_PATH = os.path.join(HERE, "docs", "static")

META_KEYS = ("name", "short-command", "version", "description",
             "home", "author")


def main():

    catalog = []
    short_commands = set()
    tool_names = set()

    #
    # Getting README from plugin
    #
    for d in os.listdir(TOOLS_PATH):

        # Get README.md file
        tools_path = os.path.join(TOOLS_PATH, d)

        meta_path = os.path.join(tools_path, "META")
        readme_path = os.path.join(tools_path, "README.md")

        try:
            with open(readme_path, "r") as readme_handler:
                readme_text = readme_handler.readlines()
        except OSError:
            print(f"[!] Tool \"{d}\" doesnt has README.md file")
            continue

        try:
            with open(meta_path, "r") as meta_handler:
                cf = configparser.ConfigParser()
                cf.read_string(f"[DEFAULT]\n {meta_handler.read()}")

                meta = dict(cf["DEFAULT"])

                # Check that META contains all needed keys
                if not all(x in meta.keys() for x in META_KEYS):
                    print(f"[!] Missing keys in META \"{d}\". "
                          f"Needed keys: \"{', '.join(META_KEYS)}\"")
                    exit(1)

                #
                # Check that 'name' and 'short-command' are unique
                #
                name = meta["name"]
                short_command = meta["short-command"]

                if short_command in short_commands:
                    print(f"[!] Short-command \"{short_command}\" at tool "
                          f"'{name}' already exits in another tool")
                    exit(1)
                else:
                    short_commands.add(short_command)

                if name in tool_names:
                    print(f"[!] Tool name '{name}' already exits used "
                          f"for other tool")
                    exit(1)
                else:
                    tool_names.add(name)

                catalog.append(meta)

        except OSError:
            print(f"[!] Tool \"{d}\" doesnt has README.md file")
            continue

        #
        # Build tools documentation
        #
        doc_tool_path = os.path.join(DOC_PATH,
                                     "content",
                                     "docs",
                                     "tools",
                                     d.replace("_", "-"))
        readme_title = readme_text[0].replace("#", "").strip()

        if not os.path.exists(doc_tool_path):
            os.makedirs(doc_tool_path, exist_ok=True)

        with open(os.path.join(doc_tool_path, "index.md"), "w") as f:
            f.write(f"---\ntitle: {readme_title}\n---\n")
            f.write("\n".join(readme_text))
            f.flush()

    #
    # Build catalog
    #
    catalog_path = os.path.join(STATIC_PATH, "catalog.json")
    catalog_path_checksum = os.path.join(STATIC_PATH, "catalog.json.checksum")
    with open(catalog_path, "w") as f, open(catalog_path_checksum, "w") as c:
        cat_content = json.dumps(catalog)

        h = hashlib.sha512()
        h.update(cat_content.encode("UTF-8"))

        f.write(cat_content)
        c.write(h.hexdigest())


if __name__ == '__main__':
    main()