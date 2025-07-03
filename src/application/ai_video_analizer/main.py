import os
import sys
import json
import time
import argparse
from google import genai
from google.genai import types
from .prompt import DEFAULT_SYSTEM_PROMPT
from src.settings.config import settings

# -- Системний промпт можна залишити як константу поза класом --


class VideoSegmenter:
    """
Клас для аналізу відео за допомогою Google Gemini AI та розділення його на сегменти.
    """
    def __init__(
            self,
            api_key: str = settings.API_KEY,
            model_name: str = 'gemini-2.5-flash-lite-preview-06-17',
            system_prompt: str = DEFAULT_SYSTEM_PROMPT
            ):
        """
            Ініціалізує сегментатор відео.

            :param api_key: Ключ API для Google AI. Якщо None, спробує отримати з змінної середовища API_KEY.
            :param model_name: Назва моделі Gemini для використання.
            :param system_prompt: Системний промпт для інструктування моделі.
        """
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("API ключ не надано")

        self.model_name = model_name
        self.system_prompt = system_prompt

        self.client = genai.Client(api_key=self.api_key)


    def _upload_video(self, video_path: str):
        """Приватний метод для завантаження відеофайлу на сервери Google."""
        print(f"Завантаження відео: {video_path}...")
        video_file = self.client.files.upload(file=video_path)

        while video_file.state.name != "ACTIVE":
            print("...", end="", flush=True)
            time.sleep(5) # Інтервал очікування
            video_file = self.client.files.get(name=video_file.name)

            # Негайно перериваємо процес у разі помилки обробки
            if video_file.state.name == "FAILED":
                raise IOError(f"Обробка відеофайлу '{video_file.display_name}' на сервері Google не вдалася.")

        return video_file

    def process_video(self, video_path: str) -> list | None:
        """
            Обробляє відеофайл: завантажує його та аналізує для отримання сегментів.

            :param video_path: Шлях до відеофайлу.
            :return: Список сегментів у форматі JSON або None у разі помилки.
        """
        if not os.path.exists(video_path):
            print(f"Помилка: Файл не знайдено за шляхом: {video_path}")
            return None

        try:
            # Крок 1: Завантаження відео
            video = self._upload_video(video_path)

            # Крок 2: Аналіз відео
            print("Аналіз відео моделлю Gemini... Це може зайняти деякий час.")
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=video,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt
                ),

            )
            # Крок 3: Повернення результату
            return json.loads(response.text)

        except json.JSONDecodeError:
            print("Помилка: Модель повернула невалідний JSON.")
            print("Спроба відповіді від моделі:", response.text)
            return None
        except Exception as e:
            print(f"Виникла помилка під час обробки відео: {e}")
            return None

def main():
    """Головна функція для запуску скрипту з командного рядка."""
    parser = argparse.ArgumentParser(description="Розділяє відео на сегменти за допомогою Gemini AI.")
    parser.add_argument("video_path", type=str, help="Шлях до відеофайлу для аналізу.")
    args = parser.parse_args()

    try:
        # 1. Створюємо екземпляр нашого класу
        segmenter = VideoSegmenter()

        # 2. Викликаємо головний метод обробки
        segments = segmenter.process_video(args.video_path)

        # 3. Обробляємо результат
        if segments:
            print("\n--- Результат аналізу ---")
            print(json.dumps(segments, indent=2, ensure_ascii=False))

            # Визначаємо назву теки для результатів
            output_dir = "segments_of_clip"

            # Створюємо теку, якщо вона не існує (безпечно)
            os.makedirs(output_dir, exist_ok=True)

            # Формуємо назву файлу та повний шлях до нього
            base_name = os.path.splitext(os.path.basename(args.video_path))[0]
            filename = f"{base_name}_segments.json"
            output_filepath = os.path.join(output_dir, filename)

            # Зберігаємо результат за новим шляхом
            with open(output_filepath, 'w', encoding='utf-8') as f:
                json.dump(segments, f, indent=2, ensure_ascii=False)
            print(f"\nРезультат збережено у файл: {output_filepath}")
        else:
            print("\nНе вдалося отримати сегменти з відео.")

    except Exception as e:
        print(f"\nВиникла критична помилка: {e}")
        sys.exit(1)

# Блок для запуску скрипту з командного рядка
if __name__ == "__main__":
    main()