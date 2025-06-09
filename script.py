import os

def rename_html_files_by_size(folder_path):
    html_files = [
        f for f in os.listdir(folder_path) if f.lower().endswith('.html')
    ]
    html_files.sort(key=lambda f: os.path.getsize(os.path.join(folder_path, f)))

    for idx, old_name in enumerate(html_files, start=1):
        new_name = f"{idx}.html"
        old_path = os.path.join(folder_path, old_name)
        new_path = os.path.join(folder_path, new_name)
        
        if old_name != new_name:
            os.rename(old_path, new_path)
            print(f"{old_name} → {new_name}")
        else:
            print(f"{old_name} уже имеет корректное имя.")

folder = r"C:\Users\Кирилл\Desktop\ConvertHTML"
rename_html_files_by_size(folder)
