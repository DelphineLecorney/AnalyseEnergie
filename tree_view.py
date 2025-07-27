import os

IGNORE = {"venv", ".git", "__pycache__"}

def print_tree(path, prefix=""):
    entries = sorted(e for e in os.listdir(path) if e not in IGNORE)
    for i, entry in enumerate(entries):
        full_path = os.path.join(path, entry)
        connector = "└── " if i == len(entries) - 1 else "├── "
        print(prefix + connector + entry)
        if os.path.isdir(full_path):
            new_prefix = prefix + ("    " if i == len(entries) - 1 else "│   ")
            print_tree(full_path, new_prefix)

if __name__ == "__main__":
    print("Structure du projet :")
    print_tree(".")
