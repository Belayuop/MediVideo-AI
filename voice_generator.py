from openai import OpenAI
import os

def generate_scene_audio(scenes, api_key, output_dir="temp_audio"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    client = OpenAI(api_key=api_key)
    audio_files = []
    
    for i, scene_text in enumerate(scenes):
        file_path = os.path.join(output_dir, f"scene_{i}.mp3")
        response = client.audio.speech.create(
            model="tts-1-hd",
            voice="shimmer", # Soft, medical professional voice
            input=scene_text
        )
        response.stream_to_file(file_path)
        audio_files.append(file_path)
        
    return audio_files
