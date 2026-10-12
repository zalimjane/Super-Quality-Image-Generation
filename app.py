import streamlit as st
import requests
import io
from PIL import Image
import urllib.parse

# Page Configuration & Layout
st.set_page_config(
    page_title="MeigenX Studio | Professional AI Art & Vector Generator", 
    page_icon="✨", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Website CSS Styling (App ki bajaye web look dene ke liye)
st.markdown("""
    <style>
    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main {
        background-color: #0f172a;
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Navbar Style */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem 3rem;
        background: rgba(15, 23, 42, 0.9);
        border-bottom: 1px solid #1e293b;
        position: sticky;
        top: 0;
        z-index: 999;
        backdrop-filter: blur(10px);
    }
    .logo {
        font-size: 1.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 4rem 1rem 2rem 1rem;
    }
    .hero-title {
        font-size: 3.2rem;
        font-weight: 900;
        color: #ffffff;
        line-height: 1.2;
        margin-bottom: 1rem;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #94a3b8;
        max-width: 700px;
        margin: 0 auto 2rem auto;
    }
    
    /* Gallery Card Style */
    .gallery-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.2rem;
        transition: transform 0.3s ease;
        margin-bottom: 1.5rem;
    }
    .gallery-card:hover {
        transform: translateY(-5px);
        border-color: #6366f1;
    }
    .badge {
        background: #312e81;
        color: #818cf8;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    /* Custom Inputs & Buttons */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white;
        font-weight: 700;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        border: none;
        width: 100%;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    .stButton>button:hover {
        opacity: 0.9;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 3rem;
        color: #64748b;
        border-top: 1px solid #1e293b;
        margin-top: 4rem;
    }
    </style>
""", unsafe_allow_html=True)

# 🌐 Website Navigation Header
st.markdown("""
    <div class="navbar">
        <div class="logo">✨ MeigenX Studio</div>
        <div style="color: #94a3b8; font-size: 0.9rem;">Professional AI Engine • Free & Live</div>
    </div>
""", unsafe_allow_html=True)

# 🌟 Hero Section
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Transform Ideas into Pro Vectors & Artwork</div>
        <div class="hero-subtitle">Generate high-resolution vector illustrations, preschool tracing pages, and commercial digital art instantly with zero friction.</div>
    </div>
""", unsafe_allow_html=True)

# Website Navigation Tabs (Website Style)
tab1, tab2 = st.tabs(["🚀 Live Studio Generator", "📚 Curated Prompt Gallery"])

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.2, 1])
    
    with col_left:
        st.markdown("### 🎛️ Generation Workspace")
        user_prompt = st.text_area(
            "Enter your detailed prompt:", 
            placeholder="e.g., Cute cartoon dinosaur for children textbook, minimalist line art, vector style...",
            height=120
        )
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            art_style = st.selectbox(
                "Design Style", 
                ["Classic Line Art (Tracing)", "Vector Illustration", "3D Flat Depth", "Vibrant Digital Art"]
            )
        with col_s2:
            resolution = st.selectbox("Resolution Quality", ["1024x1024 (HD Studio)", "768x768 (Standard)"])
            
        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("✨ Generate Professional Artwork")

    with col_right:
        st.markdown("### 🖼️ Live Output Studio")
        
        if generate_btn:
            if not user_prompt:
                st.warning("⚠️ Barahbani prompt darj karein.")
            else:
                style_suffixes = {
                    "Classic Line Art (Tracing)": ", minimalist coloring book page, pure white background, crisp black vector outlines, no shading, ideal for tracing.",
                    "Vector Illustration": ", clean flat vector illustration, vibrant colors, crisp outlines, pure white background, professional book art.",
                    "3D Flat Depth": ", smooth clean flat colors, subtle soft vector shading giving tactile 3D depth feel, crisp studio background.",
                    "Vibrant Digital Art": ", masterpiece digital artwork, high contrast, commercial design standard."
                }
                
                final_prompt = user_prompt + style_suffixes[art_style]
                
                with st.spinner("🎨 Crafting your professional artwork..."):
                    try:
                        encoded = urllib.parse.quote(final_prompt)
                        url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"
                        response = requests.get(url, timeout=60)
                        
                        if response.status_code == 200:
                            img = Image.open(io.BytesIO(response.content))
                            st.image(img, caption=user_prompt, use_column_width=True)
                            
                            buf = io.BytesIO()
                            img.save(buf, format="PNG")
                            st.download_button(
                                label="📥 Download High-Res Asset",
                                data=buf.getvalue(),
                                file_name="MeigenX_Artwork.png",
                                mime="image/png",
                                use_container_width=True
                            )
                        else:
                            st.error("Server busy hai, dobara koshish karein.")
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.info("👈 Left side par prompt likh kar 'Generate' button par click karein.")

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📌 Featured Professional Prompts")
    st.write("Meigen.ai ki tarah in curated prompts ko explore karein aur aik click mein inspiration hasil karein.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_g1, col_g2, col_g3 = st.columns(3)
    
    with col_g1:
        st.markdown("""
            <div class="gallery-card">
                <span class="badge">Education</span>
                <h4 style="margin-top: 10px; color: white;">Alphabet Tracing Page</h4>
                <p style="color: #94a3b8; font-size: 0.9rem;">Minimalist black and white outline letter A with an apple for kindergarten worksheet.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col_g2:
        st.markdown("""
            <div class="gallery-card">
                <span class="badge">3D Illustration</span>
                <h4 style="margin-top: 10px; color: white;">Isometric Creative Room</h4>
                <p style="color: #94a3b8; font-size: 0.9rem;">Cute 3D isometric designer studio room, pastel aesthetic, clean studio lighting.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col_g3:
        st.markdown("""
            <div class="gallery-card">
                <span class="badge">Commercial</span>
                <h4 style="margin-top: 10px; color: white;">Luxury Product Splash</h4>
                <p style="color: #94a3b8; font-size: 0.9rem;">Perfume bottle mockup floating in water splash, commercial advertising photography.</p>
            </div>
        """, unsafe_allow_html=True)

# 🌐 Website Footer
st.markdown("""
    <div class="footer">
        <p>© 2026 MeigenX Studio. Powered by Advanced Free AI Infrastructure.<br>Designed for Creators, Educators, and Professional Designers Worldwide.</p>
    </div>
""", unsafe_allow_html=True)
