import streamlit as st
from streamlit_drawable_canvas import st_canvas
import io
from datetime import datetime
from PIL import Image
import torch
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
import numpy as np
import google.generativeai as genai
from google.cloud import vision
import base64

def configure_gemini():
    st.session_state.gemini_api_key = "AIzaSyBAOVgJs6kO4577NIlFtbNGGpPLaLhrsQc"
    genai.configure(api_key=st.session_state.gemini_api_key)

def load_stable_diffusion_model():
    if "sd_model" not in st.session_state:
        model_id = "runwayml/stable-diffusion-v1-5"
        controlnet_id = "lllyasviel/control_v11p_sd15_scribble"

        # Load ControlNet model
        controlnet = ControlNetModel.from_pretrained(
            controlnet_id, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )

        # Load Stable Diffusion with ControlNet
        st.session_state.sd_model = StableDiffusionControlNetPipeline.from_pretrained(
            model_id,
            controlnet=controlnet,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        ).to("cuda" if torch.cuda.is_available() else "cpu")

    return st.session_state.sd_model


def get_gemini_description(image):
    """Get detailed description of the doodle using Gemini Vision."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Convert PIL image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Create Gemini image input
    gemini_image = {'mime_type': 'image/png', 'data': base64.b64encode(img_byte_arr).decode()}
    
    # Prompt for detailed analysis
    prompt = """
    Analyze this doodle and provide a concise, visual description.
    Focus only on what you see: the main subjects, their appearance, and the setting.
    Describe it as if you're instructing an artist to paint it.
    Important: Avoid mentioning that it's a doodle or sketch.
    Respond in 1-2 clear sentences only.
    """
    
    response = model.generate_content([prompt, gemini_image])
    return response.text

def process_doodle_to_art(image, style_preset="realistic"):
    # Convert the image to RGB if it's RGBA
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    
    # Resize image for processing
    max_size = 1024  # Increased for better detail
    width, height = image.size
    if width > max_size or height > max_size:
        ratio = max_size / max(width, height)
        image = image.resize((int(width * ratio), int(height * ratio)), Image.LANCZOS)
    
    # Get doodle description from Gemini
    doodle_description = get_gemini_description(image)
    
    # Enhanced style presets with more detailed prompts
    style_prompts = {
        "realistic": "hyperrealistic photograph, masterful photography, 8k UHD, incredible detail, professional lighting, shallow depth of field, shot on Phase One, perfect composition, award-winning photograph",
        "painting": "masterpiece oil painting, museum quality, intricate brushwork detail, perfect lighting, professional fine art, exhibited in prestigious galleries, painted by world-renowned artist",
        "digital": "masterful digital artwork, cinematic lighting, octane render, unreal engine 5, volumetric lighting, ray tracing, ultra detailed, featured on ArtStation HQ, incredible detail"
    }
    
    # Construct enhanced prompt with more detail and context
    style_prompt = style_prompts.get(style_preset, style_prompts["realistic"])
    base_prompt = f"Transform this simple sketch into a {style_preset} masterpiece. The image shows {doodle_description}."
    negative_prompt = "sketch, drawing, doodle, cartoon, anime, illustration, low quality, blurry, grainy"
    
    # Load model with better settings
    pipe = load_stable_diffusion_model()
    
    # Initial generation with higher guidance
    result = pipe(
        prompt=base_prompt,
        negative_prompt=negative_prompt,
        image=image,
        strength=0.85,  # Slightly higher strength for more transformation
        guidance_scale=12.0,  # Higher guidance scale for better adherence to prompt
        num_inference_steps=100,  # More steps for better quality
    ).images[0]
    
    # Second pass for refinement
    result = pipe(
        prompt=f"{base_prompt} {style_prompt}",
        negative_prompt=negative_prompt,
        image=result,
        strength=0.3,  # Lower strength to preserve first pass details
        guidance_scale=8.0,
        num_inference_steps=50,
    ).images[0]
    
    return result, doodle_description

def main():
    st.set_page_config(page_title="✨Doodle Magic Maker", layout="wide", initial_sidebar_state="collapsed")
    configure_gemini()

    st.markdown("""
        <style>
        /* Reset and Base Styles */
        .main {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            font-family: 'Poppins', sans-serif;
        }
        
        /* Sassy Header */
        .sassy-header {
            background: linear-gradient(300deg, #4158D0, #C850C0, #FFCC70);
            background-size: 180% 180%;
            animation: gradient-animation 8s ease infinite;
            padding: 2.5rem;
            border-radius: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            margin: 1rem 0 2rem 0;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .sassy-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(rgba(255,255,255,0.1), transparent);
            pointer-events: none;
        }
        
        @keyframes gradient-animation {
            0% { background-position: 0% 50% }
            50% { background-position: 100% 50% }
            100% { background-position: 0% 50% }
        }
        
        .sassy-header h1 {
            color: white;
            font-size: 4rem !important;
            font-weight: 800;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
            margin: 0 !important;
            letter-spacing: 2px;
        }
        
        .sassy-header p {
            color: white;
            font-size: 1.3rem;
            margin-top: 1rem;
            opacity: 0.9;
            font-style: italic;
        }
        
        /* Floating Elements */
        @keyframes float {
            0% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(10deg); }
            100% { transform: translateY(0px) rotate(0deg); }
        }
        
        .float-element {
            animation: float 6s ease-in-out infinite;
            display: inline-block;
            font-size: 3.5rem;
        }
        
        /* Canvas Container */
        .stCanvas {
            background: transparent !important;
            border-radius: 20px;
            overflow: hidden;
        }
        
        /* Enhanced Buttons */
        .stButton>button {
            background: linear-gradient(300deg, #4158D0, #C850C0, #FFCC70) !important;
            background-size: 180% 180% !important;
            animation: gradient-animation 8s ease infinite !important;
            border-radius: 30px !important;
            padding: 1.2rem 2.5rem !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 10px 30px rgba(65,88,208,0.3) !important;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }
        
        .stButton>button:hover {
            transform: translateY(-5px) scale(1.02) !important;
            box-shadow: 0 15px 40px rgba(65,88,208,0.4) !important;
        }
        
        /* Sidebar Styling */
        .css-1d391kg {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-right: 1px solid rgba(255,255,255,0.1);
        }
        
        .sidebar-title {
            background: linear-gradient(300deg, #4158D0, #C850C0, #FFCC70);
            background-size: 180% 180%;
            animation: gradient-animation 8s ease infinite;
            color: white;
            padding: 1.5rem;
            border-radius: 20px;
            margin-bottom: 1.5rem;
            text-align: center;
            font-size: 1.5rem;
            font-weight: 600;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        /* Form Controls */
        .stSlider>div>div>div {
            background: linear-gradient(90deg, #4158D0, #C850C0) !important;
        }
        
        .stSelectbox>div>div {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            border: 1px solid rgba(255,255,255,0.2);
            color: white !important;
        }
        
        /* Sassy Footer */
        .sassy-footer {
            background: linear-gradient(135deg, rgba(65,88,208,0.1), rgba(200,80,192,0.1));
            border-radius: 30px;
            padding: 2.5rem;
            text-align: center;
            margin-top: 3rem;
            box-shadow: 0 -10px 30px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }
        
        .sassy-footer::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #4158D0, #C850C0, #FFCC70);
        }
        
        .achievement {
            background: linear-gradient(45deg, #4158D0, #C850C0);
            color: white;
            padding: 0.8rem 1.5rem;
            border-radius: 25px;
            display: inline-block;
            margin: 0.7rem;
            font-weight: bold;
            box-shadow: 0 5px 20px rgba(65,88,208,0.3);
            transition: all 0.3s ease;
        }
        
        .achievement:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(65,88,208,0.4);
        }
        
        /* Text Selection */
        ::selection {
            background: rgba(65,88,208,0.3);
            color: white;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            background: transparent;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(45deg, #4158D0, #C850C0);
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sassy Header
    st.markdown("""
        <div class="sassy-header">
            <h1>
                <span class="float-element">✨</span> 
                Doodle Magic Maker 
                <span class="float-element">🎨</span>
            </h1>
            <p>Honey, let's make some fabulous art! *hair flip* ✨</p>
        </div>
    """, unsafe_allow_html=True)

    # Enhanced Sidebar
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-title">
                🎨 Customize Your Creation
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🎨 Art Style", expanded=True):
            style_preset = st.selectbox(
                "Choose Your Style:",
                ("realistic", "painting", "digital"),
                help="Pick how you want your doodle transformed!"
            )
        
        with st.expander("💅 Style Your Strokes", expanded=True):
            drawing_mode = st.selectbox(
                "Choose Your Weapon:",
                ("freedraw", "line", "rect", "circle", "transform"),
                help="Work it, honey! Pick your creative tool!"
            )
            
            stroke_width = st.slider("Thickness:", 1, 25, 3)
            
            if drawing_mode == 'freedraw':
                point_display_radius = st.slider("Point Size:", 1, 25, 3)
            else:
                point_display_radius = 0

        with st.expander("🌈 Color Drama", expanded=True):
            stroke_color = st.color_picker("Stroke Color:", "#C850C0")
            bg_color = st.color_picker("Background:", "#1a1a2e")
        
        with st.expander("📏 Canvas Dimensions", expanded=True):
            canvas_width = st.slider("Width:", 500, 1200, 800)
            canvas_height = st.slider("Height:", 300, 800, 400)
            realtime_update = st.checkbox("Live Updates", True)

    # Initialize session state
    if 'generated_art' not in st.session_state:
        st.session_state.generated_art = None
    if 'doodle_description' not in st.session_state:
        st.session_state.doodle_description = None

    # Canvas Area
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=canvas_height,
        width=canvas_width,
        drawing_mode=drawing_mode,
        point_display_radius=point_display_radius,
        key="canvas",
        update_streamlit=realtime_update
    )

    # Action Buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💫 Start Fresh", help="Clear the canvas"):
            st.session_state.clear_canvas = True
            st.session_state.generated_art = None
            st.session_state.doodle_description = None
    
    with col2:
        if canvas_result.image_data is not None:
            if st.button("✨ Generate Enhanced Art", help="Transform your doodle with AI magic!"):
                with st.spinner("🔮 Analyzing your doodle and creating art..."):
                    # Convert numpy array to PIL Image
                    img_array = canvas_result.image_data
                    if len(img_array.shape) == 3 and img_array.shape[2] == 4:
                        img_pil = Image.fromarray(img_array.astype('uint8'), 'RGBA')
                    else:
                        img_pil = Image.fromarray(img_array.astype('uint8'), 'RGB')
                    
                    # Generate art with description
                    st.session_state.generated_art, st.session_state.doodle_description = process_doodle_to_art(img_pil, style_preset)
    
    with col3:
        if st.session_state.generated_art is not None:
            # Convert to bytes
            img_bytes = io.BytesIO()
            st.session_state.generated_art.save(img_bytes, format='PNG')
            
            st.download_button(
                label="💖 Save Creation",
                data=img_bytes.getvalue(),
                file_name=f"enhanced_art_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png",
                help="Download your masterpiece!"
            )

    # Display Gemini's interpretation and generated art
    if st.session_state.doodle_description is not None:
        st.markdown("""
            <div style="background: rgba(200,80,192,0.1); padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3>🔮 AI's Interpretation of Your Doodle:</h3>
                <p style="font-style: italic;">
        """, unsafe_allow_html=True)
        st.write(st.session_state.doodle_description)
        st.markdown("</p></div>", unsafe_allow_html=True)

    if st.session_state.generated_art is not None:
        st.markdown("""
            <div style="text-align: center; margin: 2rem 0;">
                <h2 style="color: #C850C0; font-size: 2rem;">✨ Your Enhanced Creation ✨</h2>
            </div>
        """, unsafe_allow_html=True)
        st.image(st.session_state.generated_art, use_container_width=True)

    # Sassy Footer
    st.markdown("""
        <div class="sassy-footer">
            <h3 style="font-size: 2.5rem; margin-bottom: 1.5rem; background: linear-gradient(45deg, #4158D0, #C850C0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                💅 Werk It, Artist! 💅
            </h3>
            <div class="achievement">👑 Style Icon</div>
            <div class="achievement">💫 Art Diva</div>
            <div class="achievement">✨ Fierce Creator</div>
            <p style="font-size: 1.3em; margin: 2rem 0; color: #C850C0;">
                Show off your fab creations with <span style="color:
                Show off your fab creations with <span style="color: #4158D0; font-weight: bold;">#SassyDoodleMagic</span>
            </p>
            <p style="color: #fff; font-style: italic; opacity: 0.8;">
                Crafted with 💖 and extra sass ✨
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()