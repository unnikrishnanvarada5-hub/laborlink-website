import streamlit as st
import streamlit.components.v1 as components

CAROUSEL_SLIDES = {
  'en': [
    {
      'imageUrl': 'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?q=80&w=1200',
      'title': 'Dignity of Labor',
      'desc': 'Connecting skilled workers directly with trusted employers across India.'
    },
    {
      'imageUrl': 'https://images.unsplash.com/photo-1595974482597-4b8da8879bc5?q=80&w=1200',
      'title': 'Empowering Agriculture',
      'desc': 'Access seasonal harvesting jobs, daily wage opportunities, and farm contracts.'
    },
    {
      'imageUrl': 'https://images.unsplash.com/photo-1590069261209-f8e9b8642343?q=80&w=1200',
      'title': 'Safe & Verified Work',
      'desc': 'Transparent salary details and on-site lodging information pre-listed.'
    }
  ],
  'hi': [
    {
      'imageUrl': 'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?q=80&w=1200',
      'title': 'श्रम की गरिमा',
      'desc': 'कुशल श्रमिकों को पूरे भारत में सीधे भरोसेमंद नियोक्ताओं से जोड़ना।'
    },
    {
      'imageUrl': 'https://images.unsplash.com/photo-1595974482597-4b8da8879bc5?q=80&w=1200',
      'title': 'कृषि को बढ़ावा',
      'desc': 'फसल कटाई के काम, दैनिक वेतन के अवसर और कृषि अनुबंध प्राप्त करें।'
    },
    {
      'imageUrl': 'https://images.unsplash.com/photo-1590069261209-f8e9b8642343?q=80&w=1200',
      'title': 'सुरक्षित और प्रमाणित कार्य',
      'desc': 'पारदर्शी वेतन विवरण और साइट पर रहने की व्यवस्था की जानकारी पहले से उपलब्ध।'
    }
  ],
  'bn': [
    {
      'imageUrl': 'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?q=80&w=1200',
      'title': 'শ্রমের মর্যাদা',
      'desc': 'দক্ষ শ্রমিকদের সরাসরি নির্ভরযোগ্য নিয়োগকর্তাদের সাথে যুক্ত করা।'
    },
    {
      'imageUrl': 'https://images.unsplash.com/photo-1595974482597-4b8da8879bc5?q=80&w=1200',
      'title': 'কৃষির ক্ষমতায়ন',
      'desc': 'মরসুমী ফসল কাটা এবং দৈনিক মজুরির সুযোগ অ্যাক্সেস করুন।'
    },
    {
      'imageUrl': 'https://images.unsplash.com/photo-1590069261209-f8e9b8642343?q=80&w=1200',
      'title': 'নিরাপদ ও যাচাইকৃত কাজ',
      'desc': 'স্বচ্ছ বেতনের বিবরণ এবং থাকার ব্যবস্থার তথ্য আগে থেকেই পান।'
    }
  ],
  'ta': [
    {
      'imageUrl': 'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?q=80&w=1200',
      'title': 'உழைப்பின் கண்ணியம்',
      'desc': 'திறமையான தொழிலாளர்களை நம்பகமான முதலாளிகளுடன் நேரடியாக இணைக்கிறது.'
    },
    {
      'imageUrl': 'https://images.unsplash.com/photo-1595974482597-4b8da8879bc5?q=80&w=1200',
      'title': 'விவசாய மேம்பாடு',
      'desc': 'அறுவடை வேலைகள் மற்றும் தினசரி கூலி வாய்ப்புகளைப் பெறுங்கள்.'
    },
    {
      'imageUrl': 'https://images.unsplash.com/photo-1590069261209-f8e9b8642343?q=80&w=1200',
      'title': 'பாதுகாப்பான மற்றும் சரிபார்க்கப்பட்ட வேலை',
      'desc': 'வெளிப்படையான சம்பள விவரங்கள் மற்றும் தங்கும் வசதி விவரங்கள்.'
    }
  ],
  'te': [
    {
      'imageUrl': 'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?q=80&w=1200',
      'title': 'శ్రమ గౌరవం',
      'desc': 'నైపుణ్యం కలిగిన కార్మికులను నేరుగా నమ్మకమైన యజమానులతో కనెక్ట్ చేయడం.'
    },
    {
      'imageUrl': 'https://images.unsplash.com/photo-1595974482597-4b8da8879bc5?q=80&w=1200',
      'title': 'వ్యవసాయ సాయం',
      'desc': 'కోత పనులు మరియు రోజువారీ కూలీ అవకాశాలను పొందండి.'
    },
    {
      'imageUrl': 'https://images.unsplash.com/photo-1590069261209-f8e9b8642343?q=80&w=1200',
      'title': 'సురక్షితమైన మరియు ధృవీకరించబడిన పని',
      'desc': 'పారదర్శక జీతం వివరాలు మరియు వసతి సమాచారం ముందే లభిస్తాయి.'
    }
  ],
  'mr': [
    {
      'imageUrl': 'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?q=80&w=1200',
      'title': 'श्रमाची प्रतिष्ठा',
      'desc': 'कुशल कामगारांना थेट विश्वासू मालकांशी जोडणे.'
    },
    {
      'imageUrl': 'https://images.unsplash.com/photo-1595974482597-4b8da8879bc5?q=80&w=1200',
      'title': 'कृषी सक्षमीकरण',
      'desc': 'हंगामी कापणी कामे आणि दैनिक रोजगाराच्या संधी मिळवा.'
    },
    {
      'imageUrl': 'https://images.unsplash.com/photo-1590069261209-f8e9b8642343?q=80&w=1200',
      'title': 'सुरक्षित आणि सत्यापित काम',
      'desc': 'स्पष्ट पगार तपशील आणि राहण्याच्या सुविधेची माहिती.'
    }
  ]
}

def render_carousel(lang_code: str = "en"):
    slides = CAROUSEL_SLIDES.get(lang_code, CAROUSEL_SLIDES['en'])
    
    # HTML + CSS for a beautiful sliding carousel
    html_content = f"""
    <style>
        * {{ box-sizing: border-box; margin:0; padding:0; }}
        .slider-container {{
            position: relative;
            width: 100%;
            height: 380px;
            overflow: hidden;
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            font-family: system-ui, -apple-system, sans-serif;
        }}
        .slide {{
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-size: cover;
            background-position: center;
            opacity: 0;
            transition: opacity 1.5s ease-in-out;
            display: flex;
            align-items: flex-end;
        }}
        .slide.active {{
            opacity: 1;
        }}
        .overlay {{
            width: 100%;
            height: 60%;
            background: linear-gradient(to top, rgba(10, 25, 47, 0.95) 20%, rgba(10, 25, 47, 0));
            padding: 30px;
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
        }}
        .title {{
            font-size: 28px;
            font-weight: 800;
            color: #ffd700;
            margin-bottom: 8px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }}
        .desc {{
            font-size: 15px;
            color: #f8f9fa;
            line-height: 1.5;
            max-width: 700px;
        }}
        .dots {{
            position: absolute;
            bottom: 20px;
            right: 30px;
            display: flex;
            gap: 8px;
            z-index: 10;
        }}
        .dot {{
            width: 10px; height: 10px;
            border-radius: 50%;
            background: rgba(255,255,255,0.4);
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .dot.active {{
            width: 25px;
            border-radius: 5px;
            background: #ffd700;
        }}
    </style>

    <div class="slider-container">
        <div class="slide active" style="background-image: url('{slides[0]['imageUrl']}')">
            <div class="overlay">
                <h2 class="title">{slides[0]['title']}</h2>
                <p class="desc">{slides[0]['desc']}</p>
            </div>
        </div>
        <div class="slide" style="background-image: url('{slides[1]['imageUrl']}')">
            <div class="overlay">
                <h2 class="title">{slides[1]['title']}</h2>
                <p class="desc">{slides[1]['desc']}</p>
            </div>
        </div>
        <div class="slide" style="background-image: url('{slides[2]['imageUrl']}')">
            <div class="overlay">
                <h2 class="title">{slides[2]['title']}</h2>
                <p class="desc">{slides[2]['desc']}</p>
            </div>
        </div>
        
        <div class="dots">
            <span class="dot active" onclick="setSlide(0)"></span>
            <span class="dot" onclick="setSlide(1)"></span>
            <span class="dot" onclick="setSlide(2)"></span>
        </div>
    </div>

    <script>
        let index = 0;
        const slides = document.querySelectorAll('.slide');
        const dots = document.querySelectorAll('.dot');
        
        function setSlide(n) {{
            slides[index].classList.remove('active');
            dots[index].classList.remove('active');
            index = n;
            slides[index].classList.add('active');
            dots[index].classList.add('active');
        }}
        
        setInterval(() => {{
            let next = (index + 1) % slides.length;
            setSlide(next);
        }}, 5000);
    </script>
    """
    components.html(html_content, height=400)

def inject_global_css():
    st.markdown("""
    <style>
    /* Glassmorphism panel styles */
    .glass-panel {
        background: rgba(15, 34, 68, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
    }
    
    /* Elegant gradient text */
    .gradient-text {
        background: linear-gradient(135deg, #ffd700, #ff9f43);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    
    /* Interactive Card Zoom */
    .zoom-card {
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .zoom-card:hover {
        transform: translateY(-5px);
        border-color: #ffd700 !important;
        box-shadow: 0 10px 20px rgba(255, 215, 0, 0.1) !important;
    }
    
    /* Custom button enhancements */
    div.stButton > button {
        background-color: #0f2244;
        color: #ffd700;
        border: 1px solid #ffd700;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #ffd700;
        color: #0a192f;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 215, 0, 0.2);
    }
    
    /* Active primary button class */
    .st-emotion-cache-12w0qpk {
        border-color: #ffd700 !important;
    }
    </style>
    """, unsafe_allow_html=True)
