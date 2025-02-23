# ✨ Doodle Magic Maker | Transform Your Sketches into Art

![Doodle Magic Maker](https://img.shields.io/badge/AI-Art%20Generator-C850C0)
![Python](https://img.shields.io/badge/Python-3.8%2B-4158D0)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Transform your simple doodles into stunning artwork using the power of AI! Doodle Magic Maker combines Stable Diffusion, ControlNet, and Google's Gemini Vision to turn your sketches into professional-looking artworks in various styles.

## ✨ Features

- 🎨 Interactive drawing canvas with multiple tools
- 🔄 Real-time drawing preview
- 🎯 Multiple drawing modes (freedraw, line, rect, circle, transform)
- 🖼️ Three art styles: realistic, painting, and digital
- 🤖 AI-powered artwork generation using Stable Diffusion and ControlNet
- 📝 Intelligent sketch interpretation using Google's Gemini Vision
- 💾 Easy artwork download functionality
- 🎪 Beautiful, responsive UI with gradient animations

## 🚀 Getting Started

### Prerequisites

```bash
python 3.8+
CUDA-compatible GPU (recommended)
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/doodle-magic-maker.git
cd doodle-magic-maker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
export GEMINI_API_KEY="your_gemini_api_key"
```

4. Run the application:
```bash
streamlit run app.py
```

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI Models**: 
  - Stable Diffusion v1.5
  - ControlNet Scribble
  - Google Gemini Vision
- **Drawing Interface**: Streamlit-drawable-canvas
- **Image Processing**: Pillow, NumPy
- **UI Enhancement**: Custom CSS with animations

## 🎨 Usage

1. Open the application in your web browser
2. Use the sidebar to customize your drawing settings:
   - Select your preferred art style
   - Choose drawing tools
   - Adjust stroke width and colors
   - Set canvas dimensions
3. Create your doodle on the canvas
4. Click "Generate Enhanced Art" to transform your doodle
5. Download your created artwork using the "Save Creation" button

## 🌟 Art Style Options

- **Realistic**: Transforms your doodle into a hyperrealistic photograph
- **Painting**: Converts your sketch into a masterful oil painting
- **Digital**: Creates a modern digital artwork with cinematic lighting

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the awesome web framework
- [Stable Diffusion](https://github.com/CompVis/stable-diffusion) for the image generation
- [ControlNet](https://github.com/lllyasviel/ControlNet) for sketch control
- [Google Gemini](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini) for vision AI capabilities

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/doodle-magic-maker/issues).

---

Made with 💖 and ✨ extra sass ✨
