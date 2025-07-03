import os

from utils import find_project_files_in_reels_downloads

def classify_social_media_url(url: str) -> dict:
    """
    Classifies a given URL as either TikTok, Instagram, or 'Other' based on its domain.

    Args:
        url (str): The URL string to classify.

    Returns:
        dict: {'tt': bool, 'inst': bool}
    """
    url = url.lower()

    result = {
        "tt": False, 
        "inst": False
    }
    
    if "tiktok" in url:
        result["tt"] = True
    elif "instagram" in url:
        result["inst"] = True
    
    return result
        
def instagram_video_url():
        files = find_project_files_in_reels_downloads()
        raw_video = files.get("mp4")[0]
        raw_text = files.get("txt")[0]
        
        with open(raw_video, "rb") as f:
            video_data = f.read()
        
        with open(raw_text, "rb") as f:
            text = f.read().decode("utf-8")
        
        for file in [raw_video, raw_text]:
            try:
                if os.path.exists(file):
                    os.remove(file)
                    print(f"✅ Файл '{file}' видалено.")
                else:
                    print(f"❌ Помилка при видаленні: Файл {file} не знайдено")
            except Exception as e:
                print(f"❌ Помилка при видаленні: {e}")
        
        return video_data, text