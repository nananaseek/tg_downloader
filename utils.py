import os

def find_project_files_in_reels_downloads():
    """
    Знаходить файли з розширеннями .mp4 та .txt у директорії 'reels_downloads'
    (яка знаходиться поруч зі скриптом) та всіх її піддиректоріях,
    виключаючи директорії з назвою '.venv'.

    Коректно обробляє файли, назви яких містять крапки (наприклад, 'my.video.final.mp4').

    Повертає:
        dict: Словник, де ключами є розширення (без крапки, у нижньому регістрі),
              а значеннями – список повних шляхів до знайдених файлів цього розширення.
              Приклад: {'mp4': ['/path/to/file.mp4'], 'txt': ['/path/to/file.txt']}
    """
    # Автоматично визначаємо кореневу директорію проєкту як директорію,
    # де знаходиться цей скрипт.
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Визначаємо шлях до цільової директорії 'reels_downloads'
    target_directory = os.path.join(script_directory, 'reels_downloads')

    # Перевіряємо, чи існує цільова директорія
    if not os.path.isdir(target_directory):
        print(f"Помилка: Директорія '{target_directory}' не знайдена.")
        return {'mp4': [], 'txt': []}

    # Визначаємо розширення файлів, які потрібно знайти.
    target_extensions = ['mp4', 'txt']

    # Ініціалізуємо словник для зберігання знайдених файлів, групуючи їх за розширенням.
    found_files_dict = {ext.lower(): [] for ext in target_extensions}

    print(f"Пошук файлів з розширеннями {', '.join(target_extensions)} у директорії '{target_directory}' (виключаючи .venv)...")

    # Проходимося по всіх директоріях та файлах, починаючи з цільової директорії.
    for root, dirs, files in os.walk(target_directory):
        # Видаляємо '.venv' зі списку директорій, щоб os.walk не заходив у них.
        # Важливо: модифікувати 'dirs' на місці.
        if '.venv' in dirs:
            dirs.remove('.venv')
        if "src" in dirs:
            dirs.remove("src")
        if "logs" in dirs:
            dirs.remove("logs")
        
        for file in files:
            # Використовуємо os.path.splitext() для безпечного отримання розширення.
            _, file_extension_with_dot = os.path.splitext(file)

            # Видаляємо крапку на початку розширення і переводимо його в нижній регістр.
            file_extension = file_extension_with_dot.lstrip('.').lower()

            # Перевіряємо, чи розширення файлу є одним з цільових.
            if file_extension in found_files_dict:
                # Додаємо повний шлях до файлу у відповідний список у словнику.
                found_files_dict[file_extension].append(os.path.join(root, file))

    return found_files_dict
    
    
def check_for_files_in_directory(directory_path: str = "reels_downloads"):
    """
    Перевіряє, чи є файли в заданій теці.

    Args:
        directory_path (str): Шлях до теки, яку потрібно перевірити.

    Returns:
        bool: True, якщо в теці є файли, False в іншому випадку.
        str: Повідомлення про результат.
    """
    if not os.path.isdir(directory_path):
        return False

    # Отримуємо список всіх елементів (файлів та папок) у теці
    items = os.listdir(directory_path)

    # Фільтруємо, залишаючи лише файли
    files = [item for item in items if os.path.isfile(os.path.join(directory_path, item))]

    if files:
        return True
    else:
        return False