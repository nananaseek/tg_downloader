import os
import tempfile

def create_kostil():
    
    os.makedirs("tmp", exist_ok=True)
    
    project_root = os.getcwd()
    tmp_dir_path = os.path.join(project_root, "tmp")
    
    try:
        # Використовуємо NamedTemporaryFile, вказуючи 'dir' для розміщення файлу
        with tempfile.NamedTemporaryFile(
            mode='w',
            delete_on_close=False, # Важливо: файл не буде автоматично видалений після закриття
            dir=tmp_dir_path, # Вказуємо нашу власну теку 'tmp'
            encoding='utf-8',
            delete=False
        ) as tmp_file:
            tmp_file.write("")
            
        print(f"Тимчасовий файл '{os.path.basename(tmp_file.name)}' успішно створено у '{tmp_dir_path}'.")
        return tmp_file.name
    except IOError as e:
        print(f"Помилка при створенні тимчасового файлу у '{tmp_dir_path}': {e}")
        return ""
    

def count_files_in_project_tmp_dir() -> int:
    """
    Перевіряє кількість файлів у теці 'tmp' всередині кореневої теки проекту.

    Returns:
        int: Кількість файлів у теці 'tmp' проекту, або -1 у разі помилки.
    """
    project_root = os.getcwd()
    tmp_dir_path = os.path.join(project_root, "tmp")

    if not os.path.exists(tmp_dir_path):
        print(f"Тека '{tmp_dir_path}' не існує. Файлів не знайдено.")
        return 0

    try:
        # Фільтруємо лише файли, ігноруючи підтеки
        files = [f for f in os.listdir(tmp_dir_path) if os.path.isfile(os.path.join(tmp_dir_path, f))]
        count = len(files)
        print(f"У теці проекту '{tmp_dir_path}' знайдено {count} файлів.")
        return count
    except OSError as e:
        print(f"Помилка при доступі до теки '{tmp_dir_path}': {e}")
        return -1
    
    
