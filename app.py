import streamlit as st
print("Loading frontend.py")
import scripts.main as m
print("Main imported")
import scripts.hash as h
print("Hash imported")
from PIL import Image
import os

st.set_page_config(page_title="Caption Craft : Image Caption & Hashtag Generator", layout="centered")

st.title("Caption Craft :  Image Description &Hashtag Generator ")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Show uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Save temporarily
    image_path = f"assets\\Image\\temp_{uploaded_file.name}"
    image.save(image_path)

    # Select captioning method
    method = st.radio("Choose Description Method", ["Greedy", "Beam Search"])
    if method == "Beam Search":
        K_beams = st.slider("Select Beam Width", 2, 10, 3)
    else:
        K_beams = None

    print("Image uploaded and method selected.")
    print(f"Method: {method}, K_beams: {K_beams}")
    print(f"Image path: {image_path}")
    print("Ready to generate caption.")
    print("Calling m.generate_caption and h.process_image")
    # Generate caption
    if st.button("Generate Description & Hashtags"):
        with st.spinner("Caption Craft is Generating ..."):
            if method == "Greedy":
                caption = m.generate_caption(image_path, method="greedy")
            else:
                caption = m.generate_caption(image_path, method="beam_search", K_beams=K_beams)

        st.success(f"**Generated Description:** {caption}")

        # Mood / Color analysis
        with st.spinner("Analyzing mood and colors..."):
            mood_output = h.process_image(image_path, h.color_prompts, h.Mood_prompts)

        st.info(f"**Mood Analysis or Recomended Hashtag:** {mood_output}")
    os.remove(image_path)
    
