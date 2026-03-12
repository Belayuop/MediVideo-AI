import streamlit as st
import os
import shutil
from pdf_reader import process_pdf
from ppt_reader import process_ppt
from script_generator import generate_structured_script
from voice_generator import generate_scene_audio
from video_creator import assemble_video

st.set_page_config(page_title="MediVideo-AI Pro", layout="wide")

st.title("🏥 MediVideo-AI: Advanced Medical Education")
st.markdown("---")

# UI Sidebar
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    st.info("This tool uses GPT-4 for scripting and TTS-HD for high-quality medical narration.")

# Main Interface
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload Medical PDF or PPTX", type=["pdf", "pptx"])
    process_btn = st.button("🚀 Generate Professional Video")

if uploaded_file and api_key:
    if process_btn:
        # Create unique temp workspace
        if os.path.exists("temp_slides"): shutil.rmtree("temp_slides")
        if os.path.exists("temp_audio"): shutil.rmtree("temp_audio")
        
        with st.status("🏗️ Building your medical video...", expanded=True) as status:
            # 1. Extraction
            st.write("🔍 Extracting assets from document...")
            if uploaded_file.name.endswith(".pdf"):
                with open("temp.pdf", "wb") as f: f.write(uploaded_file.getbuffer())
                raw_text, images = process_pdf("temp.pdf")
            else:
                raw_text = process_ppt(uploaded_file)
                images = [] # PPT image extraction requires separate logic or conversion

            # 2. Scripting
            st.write("🧠 AI Scriptwriter is analyzing medical content...")
            scenes = generate_structured_script(raw_text, api_key)
            
            # 3. Audio Synthesis
            st.write("🎙️ Synthesizing HD Medical Narration...")
            audio_files = generate_scene_audio(scenes, api_key)
            
            # 4. Video Assembly
            st.write("🎬 Rendering Final Video (Full HD)...")
            # If no images found (like in simple PPT logic), use a placeholder
            if not images:
                images = ["placeholder_medical.png"] # Ensure you have a generic med image
                
            final_path = assemble_video(images, audio_files)
            
            status.update(label="✅ Video Ready!", state="complete")

        with col2:
            st.header("Final Production")
            st.video(final_path)
            with open(final_path, "rb") as file:
                st.download_button("💾 Download Video", file, file_name="Medical_Video.mp4")
            
            st.subheader("Script Preview")
            for i, s in enumerate(scenes):
                st.write(f"**Scene {i+1}:** {s}")

elif not api_key:
    st.warning("Please enter your API Key to unlock deep AI features.")
