import streamlit as st
import requests
import io
from PIL import Image
import urllib.parse

# Page Configuration
st.set_page_config(
    page_title="Meigen-Style AI Studio & Prompt Gallery", 
    page_icon="✨", 
    layout="wide"
)

# Custom Styling for Clean Look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        border: none;
    }
    .card {
        padding: 15px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🌟 Navigation")
page = st.sidebar.radio("Go to:", ["🎨 Live Generator", "📚 Prompt Gallery"])

if page == "🎨 Live Generator":
    st.title("✨ Free AI Image & Vector Studio")
    st.write("Meigen.ai ki tarah apnay pasandida prompts likhein aur foran free high-quality images generate karein.")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_prompt = st.text_area("Enter your prompt:", placeholder="e.g., Cute 3D isometric room, minimalist vector illustration, product photography...")
        art_style = st.selectbox("Select Style Mode:", ["Default / Realistic", "Minimalist Line Art", "Flat 3D Vector", "Vibrant Digital Art"])
        
        if st.button("🚀 Generate Image", use_container_width=True):
            if not user_prompt:
                st.error("Barahbani prompt darj karein.")
            else:
                style_map = {
                    "Default / Realistic": "",
                    "Minimalist Line Art": ", minimalist coloring book line art, pure white background, crisp outlines",
                    "Flat 3D Vector": ", smooth flat colors, subtle 3D depth, clean studio background",
                    "Vibrant Digital Art": ", vibrant colors, high contrast, digital illustration masterpiece"
                }
                
                final_prompt = user_prompt + style_map[art_style]
                
                with st.spinner("Generating your image..."):
                    try:
                        encoded = urllib.parse.quote(final_prompt)
                        url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"
                        response = requests.get(url, timeout=60)
                        
                        if response.status_code == 200:
                            img = Image.open(io.BytesIO(response.content))
                            st.success("Image successfully generated!")
                            st.image(img, caption=user_prompt, use_column_width=True)
                            
                            # Download option
                            buf = io.BytesIO()
                            img.save(buf, format="PNG")
                            st.download_button("📥 Download Image", data=buf.getvalue(), file_name="generated_art.png", mime="image/png")
                        else:
                            st.error("Server busy hai, dobara koshish karein.")
                    except Exception as e:
                        st.error(f"Error: {e}")

elif page == "📚 Prompt Gallery":
    st.title("📌 Community Prompt Gallery")
    st.write("Yahan aap tayyar shuda prompts dekh sakte hain aur unhe copy karke generator mein istemal kar sakte hain.")
    st.markdown("---")
    
    # Sample Gallery Cards (Jaise Meigen par hota hai)
    gallery_items = [
        {"title": "3D Isometric Tiny House", "prompt": "Cute 3D isometric tiny house, cozy lighting, soft pastel colors, clean white background", "cat": "3D & Illustration"},
        {"title": "Alphabet Tracing Letter A", "prompt": "Minimalist black and white outline letter A with an apple for kids coloring book, clean vector", "cat": "Education"},
        {"title": "Product Perfume Bottle", "prompt": "Luxury perfume bottle mockup floating in water splash, vibrant studio lighting, commercial photography", "cat": "Ads & Product"}
    ]
    
    for item in gallery_items:
        st.markdown(f"""
            <div class='card'>
                <h4>📌 {item['title']}</h4>
                <p><b>Category:</b> {item['cat']}</p>
                <p><code>{item['prompt']}</code></p>
            </div>
        """, unsafe_allow_html=True)
