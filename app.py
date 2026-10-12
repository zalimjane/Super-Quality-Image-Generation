import streamlit as st
from openai import OpenAI

# Page Configuration
st.set_page_config(page_title="Tracing & Coloring Book AI Generator", page_icon="🎨", layout="centered")

# Header Section
st.title("🎨 Tracing & Coloring Book AI Tool")
st.write("Yahan aap bina kisi extra instruction ke super high-quality line art aur tracing images generate kar sakte hain.")

# OpenAI API Key Input (Aap apni API key yahan daal sakte hain ya environment variable me rakh sakte hain)
api_key = st.text_input("Apni OpenAI API Key darj karein:", type="password")

# User Input for the Object
user_prompt = st.text_input("Aap kis cheez ya object ki image banana chahte hain? (Misal ke taur par: Cute Cat, Apple, Car)", placeholder="Yahan likhein...")

# Bulk quantity option agar mazeed aasaani karni ho
num_images = st.slider("Tadad (Number of Images):", min_value=1, max_value=4, value=1)

if st.button("Generate Perfect Line Art"):
    if not api_key:
        st.error("Brahmeharbani apni OpenAI API Key darj karein.")
    elif not user_prompt:
        st.error("Brahmeharbani kisi object ya cheez ka naam likhein.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            
            # Master System & Style Enforcement (User ko bar-bar likhne ki zaroorat nahi)
            # Yeh backend par automatically har prompt ke sath attach ho jayega
            fixed_style_suffix = (
                ", clean white background, flat vector lines, black and white line art, "
                "thick clear outlines, no shading, no gradients, no 3D effects, "
                "high resolution, perfect shapes, ideal for kids tracing and printing books."
            )
            
            final_prompt = f"A minimalist coloring book page of {user_prompt}{fixed_style_suffix}"
            
            with st.spinner("Super high-quality line art taiyar ho raha hai..."):
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=final_prompt,
                    size="1024x1024",
                    quality="hd", # High definition for printing quality
                    n=1,
                )
                
                image_url = response.data[0].url
                
                # Display the generated image
                st.success("Image kamyabi ke sath generate ho gayi hai!")
                st.image(image_url, caption=f"Generated for: {user_prompt}", use_column_width=True)
                
                # Download link helper text
                st.markdown(f"[Download High-Resolution Image]({image_url})")
                
        except Exception as e:
            st.error(f"Koi kharabi pesh aayi: {e}")
