import instaloader
import sys
import os
import re # Імпортуємо модуль для роботи з регулярними виразами

# Ваш логін в Instagram (обов'язково замініть на свій)
# Скрипт шукатиме файл сесії з цим іменем


class InstagramDownloader:

    def __init__(self, url) -> None:
        self.INSTAGRAM_USERNAME = "etseoo"
        self.L = instaloader.Instaloader(
                    download_pictures=False,       # Не завантажувати обкладинку/постер
                    download_videos=True,          # Завантажувати тільки відео
                    download_video_thumbnails=False, # Не завантажувати прев'ю
                    download_geotags=False,
                    download_comments=False,
                    save_metadata=False,           # Не зберігати метадані у .json файлах
                    compress_json=False,
                    post_metadata_txt_pattern=None
                )
        self.url = url
        
    def download_media_by_url(self):
        """
    Завантажує будь-який медіа-контент (Reel, пост, IGTV) з Instagram за посиланням.
        """
        # Створюємо екземпляр Instaloader з налаштуваннями
        
    
        print("-> Спроба завантажити сесію...")
        try:
            self.L.load_session_from_file(self.INSTAGRAM_USERNAME)
            print(f"✅ Сесію для користувача '{self.INSTAGRAM_USERNAME}' успішно завантажено.")
        except FileNotFoundError:
            print(f"⚠️ Файл сесії для '{self.INSTAGRAM_USERNAME}' не знайдено.")
            print("   Для надійної роботи рекомендується створити сесію командою: instaloader --login=" + self.INSTAGRAM_USERNAME)
    
        # Універсальний патерн для вилучення shortcode з URL (для /p/, /reel/, /tv/)
        match = re.search(r"/(?:p|reel|tv)/([^/]+)", self.url)
        if not match:
            print("❌ Помилка: Неправильне посилання.")
            print("   Переконайтеся, що посилання веде на пост, Reel або IGTV.")
            return False
    
        shortcode = match.group(1)
    
        try:
            print(f"\n🔗 Отримую інформацію про пост (shortcode: {shortcode})")
            post = instaloader.Post.from_shortcode(self.L.context, shortcode)

            # Створюємо папку "downloads", якщо її немає
            output_dir = "reels_downloads"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
    
            # Задаємо кастомний шаблон для імені файлу: {owner_username}_{shortcode}.{ext}
            self.L.filename_pattern = f"{post.owner_username}_{post.shortcode}"
    
            print(f"📥 Починаю завантаження у папку '{output_dir}'...")
    
            # Завантажуємо пост у вказану директорію
            result: bool = self.L.download_post(post, target=output_dir)
    
            print(f"\n✅ Готово! Відео збережено у папці '{os.path.abspath(output_dir)}'.")
            
    
        except instaloader.exceptions.BadResponseException as e:
            print(f"❌ Помилка запиту: {e}. Можливо, пост приватний, видалений або посилання невірне.")
            return False
        except instaloader.exceptions.PrivateProfileNotFollowedException:
            print("❌ Помилка: Профіль приватний, і ви не авторизовані або не підписані на нього.")
            return False
        except Exception as e:
            print(f"❌ Виникла неочікувана помилка: {e}")
            return False
        else:
            print("✅ Всі завантаження завершено.")
            return result
    
    
    async def remove_temp_dir(self, path: str):
        
        print(f"⏳ Видалення файлу '{path}'...")
        
        # await asyncio.sleep(2)
        
        try:
            if os.path.exists(path):
                os.remove(path)
                print(f"✅ Файл '{path}' видалено.")
            else:
                print("❌ Помилка при видаленні: Файл не знайдено")
        except Exception as e:
            print(f"❌ Помилка при видаленні: {e}")
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        media_url = sys.argv[1]
    else:
        media_url = input("Введіть посилання на Reel (або пост) в Instagram: ")

    if not media_url.strip():
        print("Посилання не може бути порожнім.")
    else:
        Inst = InstagramDownloader(url=media_url)
        Inst.download_media_by_url()