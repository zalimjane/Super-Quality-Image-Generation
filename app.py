import streamlit as st
import requests
import io
from PIL import Image
import urllib.parse
import time

# Page Configuration & Professional Styling
st.set_page_config(
    page_title="NexusArt Pro Studio | AI Tracing & Vector Generator", 
    page_icon="🎨", 
    layout="wide"
)

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
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("🎛️ Studio Control Panel")
st.sidebar.markdown("---")
st.sidebar.success("✨ Engine Status: Active & Optimized")

art_mode = st.sidebar.selectbox(
    "Select Art Style:", 
    [
        "Classic Line Art (Tracing & Coloring Books)", 
        "Color Tracing & Vector Illustration", 
        "Flat Colors with 3D Depth Feel"
    ]
)

num_images = st.sidebar.slider("Bulk Quantity (Images):", min_value=1, max_value=5, value=1)

st.title("🎨 NexusArt Pro Studio")
st.write("Professional-grade bulk image generator for preschool curricula, worksheets, coloring books, and vector tracing.")
st.markdown("---")

col1, col2 = st.columns([3, 1])
with col1:
    user_prompt = st.text_input(
        "Enter your creative prompt or object:", 
        placeholder="e.g., Cute cartoon dinosaur, alphabet letter A, space rocket..."
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("🚀 Generate Bulk Art", use_container_width=True)

if generate_btn:
    if not user_prompt:
        st.error("⚠️ Barahbani kisi object ya theme ka naam likhein.")
    else:
        # Prompt ko safe length aur format mein rakhna taaki URL error na aaye
        clean_prompt = user_prompt[:150]
        
        if art_mode == "Classic Line Art (Tracing & Coloring Books)":
            style_suffix = ", minimalist coloring book page, pure white background, crisp black outlines, vector line art, no shading, ideal for kids tracing."
        elif art_mode == "Color Tracing & Vector Illustration":
            style_suffix = ", clean vector illustration, vibrant flat colors, crisp outlines, pure white background, kids book art."
        else:
            style_suffix = ", vector art with smooth clean flat colors, soft vector shading giving 3D depth feel, pure white background."

        final_prompt = f"{clean_prompt}{style_suffix}"
        
        st.markdown(f"### 📦 Generating {num_images} High-Quality Image(s)...")
        
        cols = st.columns(num_images if num_images <= 3 else 3)
        
        for i in range(num_images):
            with st.spinner(f"Rendering variant {i+1}..."):
                seed = 5000 + (i * 15)
                encoded_prompt = urllib.parse.quote(final_prompt)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed={seed}&nologo=true"
                
                success = False
                image = None
                
                for attempt in range(3):
                    try:
                        response = requests.get(image_url, timeout=45)
                        if response.status_code == 200 and len(response.content) > 1000:
                            image = Image.open(io.BytesIO(response.content))
                            success = True
                            break
                    except Exception:
                        time.sleep(1.5)
                
                target_col = cols[i % len(cols)]
                with target_col:
                    if success and image:
                        st.image(image, caption=f"Variant {i+1}", use_column_width=True)
                        
                        buf = io.BytesIO()
                        image.save(buf, format="PNG")
                        byte_im = buf.getvalue()
                        
                        st.download_button(
                            label=f"📥 Download #{i+1}",
                            data=byte_im,
                            file_name=f"artwork_v{i+1}.png",
                            mime="image/png",
                            key=f"dl_{i}_{seed}"
                        )
                    else:
                        st.error(f"Variant {i+1} load nahi ho saka. Dobara koshish karein.")
