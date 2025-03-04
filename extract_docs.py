import os

def read_files_from_directory(directory, file_extensions=(".md")):
    repo_data = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(file_extensions):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    repo_data[file_path] = f.read()
    return repo_data

repo_path = "../Solidvessel"
docs = read_files_from_directory(repo_path)

print(len(docs))