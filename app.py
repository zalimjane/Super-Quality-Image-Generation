import streamlit as st
import requests
import io
from PIL import Image
import urllib.parse

# Page Configuration & Professional Styling
st.set_page_config(
    page_title="NexusArt Pro Studio | AI Tracing & Vector Generator", 
    page_icon="🎨", 
    layout="wide"
)

# Custom Professional Dashboard CSS Styling
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
        padding: 0.6rem 1.2rem;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #4338ca 0%, #2563eb 100%);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }
    .card {
        padding: 20px;
        border-radius: 12px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Configuration for Pro Dashboard
st.sidebar.title("🎛️ Studio Control Panel")
st.sidebar.markdown("---")
st.sidebar.success("✨ Engine Status: Active & Free\n🚀 Ready for Bulk Generation")

st.sidebar.markdown("### ⚙️ Design Modes")
art_mode = st.sidebar.selectbox(
    "Select Art Style:", 
    [
        "Classic Line Art (Tracing & Coloring Books)", 
        "Color Tracing & Vector Illustration", 
        "Flat Colors with 3D Depth Feel"
    ]
)

num_images = st.sidebar.slider("Bulk Quantity (Images):", min_value=1, max_value=5, value=1)

# Main Dashboard Header
st.title("🎨 NexusArt Pro Studio")
st.write("Professional-grade bulk image generator for preschool curricula, worksheets, coloring books, and vector tracing.")
st.markdown("---")

# User Input Section inside a clean layout
col1, col2 = st.columns([3, 1])
with col1:
    user_prompt = st.text_input(
        "Enter your creative prompt or object:", 
        placeholder="e.g., Cute cartoon dinosaur, alphabet letter A, space rocket, math worksheet icons..."
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("🚀 Generate Bulk Art", use_container_width=True)

if generate_btn:
    if not user_prompt:
        st.error("⚠️ Barahbani kisi object, theme ya curriculum topic ka naam likhein.")
    else:
        # Automatic Professional Style Enforcement (No need to repeat instructions)
        if art_mode == "Classic Line Art (Tracing & Coloring Books)":
            style_suffix = ", minimalist coloring book page, pure white background, crisp black outlines, thick vector line art, no shading, zero gradients, ideal for kids tracing and printing."
        elif art_mode == "Color Tracing & Vector Illustration":
            style_suffix = ", clean vector illustration, vibrant flat colors, crisp outlines, pure white background, high quality educational children book art."
        else: # Flat Colors with 3D Depth Feel
            style_suffix = ", vector art with smooth clean flat colors, subtle soft vector shading giving a tactile 3D depth feel, pure crisp white background, high resolution studio quality."

        final_prompt = f"{user_prompt}{style_suffix}"
        
        st.markdown(f"### 📦 Generating {num_images} High-Quality Image(s) in Bulk...")
        
        cols = st.columns(num_images if num_images <= 3 else 3)
        
        try:
            for i in range(num_images):
                with st.spinner(f"Rendering variant {i+1} of {num_images}..."):
                    # Unique seed for gorgeous bulk variations
                    seed = 2026 + i
                    encoded_prompt = urllib.parse.quote(final_prompt)
                    
                    # High-performance robust image rendering endpoint
                    image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed={seed}&nologo=true"
                    
                    response = requests.get(image_url, timeout=60)
                    
                    if response.status_code == 200:
                        image = Image.open(io.BytesIO(response.content))
                        
                        target_col = cols[i % len(cols)]
                        with target_col:
                            st.image(image, caption=f"Variant {i+1}: {user_prompt}", use_container_width=True)
                            
                            # Prepare download bytes
                            buf = io.BytesIO()
                            image.save(buf, format="PNG")
                            byte_im = buf.getvalue()
                            
                            st.download_button(
                                label=f"📥 Download #{i+1}",
                                data=byte_im,
                                file_name=f"{user_prompt.replace(' ', '_')}_variant_{i+1}.png",
                                mime="image/png",
                                key=f"dl_{i}_{seed}"
                            )
                    else:
                        st.error(f"Error on image {i+1}: Could not render from server.")
        except Exception as ex:
            st.error(f"Generation error: {ex}")
