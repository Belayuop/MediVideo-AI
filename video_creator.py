from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, TextClip
import os

def assemble_video(image_paths, audio_paths, output_filename="medical_presentation.mp4"):
    clips = []
    
    # We match images to audio scenes. 
    # If we have 10 images and 3 audio scenes, we distribute images evenly.
    for i in range(len(audio_paths)):
        audio_clip = AudioFileClip(audio_paths[i])
        
        # Select an image (loop back if we run out of images)
        img_idx = i if i < len(image_paths) else len(image_paths) - 1
        
        img_clip = (ImageClip(image_paths[img_idx])
                    .set_duration(audio_clip.duration)
                    .set_audio(audio_clip)
                    .resize(height=720)) # Normalize to 720p
        
        clips.append(img_clip)

    final_video = concatenate_videoclips(clips, method="compose")
    
    # Optional: Add a watermark
    watermark = (TextClip("MediVideo-AI: Medical Education", fontsize=24, color='white')
                 .set_duration(final_video.duration)
                 .set_position(('right', 'bottom'))
                 .set_opacity(0.5))
    
    result = CompositeVideoClip([final_video, watermark])
    result.write_videofile(output_filename, fps=24, codec="libx264", audio_codec="aac")
    
    return output_filename
