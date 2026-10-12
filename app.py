import streamlit as st
import requests
import io
from PIL import Image
import urllib.parse

# Page Configuration & Professional Styling
st.set_page_config(
    page_title="NexusArt Studio | Pro Tracing & Coloring Generator", 
    page_icon="🎨", 
    layout="wide"
)

# Custom CSS for Professional Dashboard Look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4f46e5 0%, #3b82f6 100%);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #4338ca 0%, #2563eb 100%);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Configuration for Dashboard Settings
st.sidebar.title("🎛️ Control Panel")
st.sidebar.markdown("---")
st.sidebar.success("✨ No API Key Required!\n100% Free & Unlimited.")

st.sidebar.markdown("### ⚙️ Generation Settings")
art_mode = st.sidebar.selectbox(
    "Design Mode:", 
    ["Classic Line Art (Tracing)", "Color Tracing & Vector Illustration", "Flat Colors with 3D Depth Feel"]
)

num_images = st.sidebar.slider("Bulk Quantity (Images):", min_value=1, max_value=5, value=1)

# Main Dashboard Header
st.title("🎨 NexusArt Pro Studio")
st.write("Bulk high-resolution tracing, coloring books, and 3D flat-vector generator tool.")
st.markdown("---")

# User Input Section
col1, col2 = st.columns([3, 1])
with col1:
    user_prompt = st.text_input("What would you like to generate?", placeholder="e.g., Cute cartoon dinosaur, alphabet letter A, space rocket...")

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("🚀 Generate Bulk Art", use_container_width=True)

if generate_btn:
    if not user_prompt:
        st.error("⚠️ Barahbani kisi object ya theme ka naam likhein.")
    else:
        # Style mapping based on user selection
        if art_mode == "Classic Line Art (Tracing)":
            style_suffix = ", minimalist coloring book page, pure white background, crisp black outlines, vector line art, no shading, ideal for tracing and printing."
        elif art_mode == "Color Tracing & Vector Illustration":
            style_suffix = ", clean vector illustration, vibrant flat colors, crisp outlines, white background, high quality kids book art."
        else: # Flat Colors with 3D Depth Feel
            style_suffix = ", vector art with smooth clean flat colors, subtle soft vector shading giving a tactile 3D depth feel, crisp clean background, high resolution studio quality."

        final_prompt = f"{user_prompt}{style_suffix}"
        
        st.markdown(f"### 📦 Generating {num_images} Image(s) in bulk...")
        
        cols = st.columns(num_images if num_images <= 3 else 3)
        
        try:
            for i in range(num_images):
                with st.spinner(f"Generating image {i+1} of {num_images}..."):
                    # Using free public endpoint with unique seed for bulk variations
                    seed = 42 + i
                    encoded_prompt = urllib.parse.quote(final_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed={seed}&nologo=true"
                    
                    response = requests.get(image_url, timeout=60)
                    
                    if response.status_code == 200:
                        image = Image.open(io.BytesIO(response.content))
                        
                        target_col = cols[i % len(cols)]
                        with target_col:
                            st.image(image, caption=f"Variant {i+1}: {user_prompt}", use_column_width=True)
                            
                            buf = io.BytesIO()
                            image.save(buf, format="PNG")
                            byte_im = buf.getvalue()
                            
                            st.download_button(
                                label=f"📥 Download #{i+1}",
                                data=byte_im,
                                file_name=f"{user_prompt.replace(' ', '_')}_v{i+1}.png",
                                mime="image/png",
                                key=f"dl_{i}"
                            )
                    else:
                        st.error(f"Error on image {i+1}: Server responded with status {response.status_code}")
        except Exception as ex:
            st.error(f"Generation error: {ex}")
