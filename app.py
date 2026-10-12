import streamlit as st
import requests
import io
from PIL import Image

# Page Configuration
st.set_page_config(page_title="Free Tracing & Coloring Book AI Generator", page_icon="🎨", layout="centered")

# Header Section
st.title("🎨 Free Tracing & Coloring Book AI Tool")
st.write("Yahan aap bina kisi paid API key ke super high-quality line art aur tracing images generate kar sakte hain.")

# Hugging Face API Key Input (Free token)
api_key = st.text_input("Apni Hugging Face Free API Key (Token) darj karein:", type="password")
st.markdown("[Free Hugging Face Token yahan se hasil karein](https://huggingface.co/settings/tokens)")

# User Input for the Object
user_prompt = st.text_input("Aap kis cheez ya object ki image banana chahte hain? (Misal ke taur par: Cute Cat, Apple, Car)", placeholder="Yahan likhein...")

if st.button("Generate Perfect Line Art"):
    if not api_key:
        st.error("Baharbani apni Hugging Face API Key darj karein.")
    elif not user_prompt:
        st.error("Baharbani kisi object ya cheez ka naam likhein.")
    else:
        try:
            # Using a reliable free stable diffusion model for line art
            API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
            headers = {"Authorization": f"Bearer {api_key}"}
            
            # Locked System Prompt for Perfect Tracing & Coloring
            fixed_style_suffix = (
                ", minimalist coloring book page, clean white background, flat vector lines, "
                "black and white line art, thick clear outlines, no shading, no gradients, "
                "no 3D effects, high resolution, perfect shapes, ideal for kids tracing and printing."
            )
            
            final_prompt = f"{user_prompt}{fixed_style_suffix}"
            payload = {"inputs": final_prompt}
            
            with st.spinner("Hugging Face se line art taiyar ho raha hai..."):
                response = requests.post(API_URL, headers=headers, json=payload)
                
                if response.status_code == 200:
                    image_bytes = response.content
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    # Display the generated image
                    st.success("Image kamyabi ke sath generate ho gayi hai!")
                    st.image(image, caption=f"Generated for: {user_prompt}", use_column_width=True)
                    
                    # Save bytes for download
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    st.download_button(
                        label="Download High-Resolution Image",
                        data=byte_im,
                        file_name=f"{user_prompt.replace(' ', '_')}_tracing.png",
                        mime="image/png"
                    )
                else:
                    st.error(f"Error: {response.text}")
                
        except Exception as e:
            st.error(f"Koi kharabi pesh aayi: {e}")
