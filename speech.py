import streamlit as st
import streamlit.components.v1 as components
import time

VOICE_PROMPTS = {
    'en': {
        'welcome': "Welcome to Labor Link. Your connection to good jobs. Please choose your language.",
        'chooseRole': "Are you looking for work, or are you hiring? Select Worker or Employer.",
        'enterPhone': "Please enter your ten digit mobile number below to login.",
        'enterOtp': "We sent an authorization code to your mobile. Please enter the six digit code.",
        'profileWizard': "Let's build your profile. It will be built in English and your language.",
        'inputName': "Please enter your full name.",
        'inputCategory': "Select the work you do. For example, construction, plumbing, or driving.",
        'inputExperience': "How many years of experience do you have?",
        'inputLocation': "Where do you want to work? Enter your current city.",
        'inputBio': "Tell employers about your skills, or record a voice greeting.",
        'profileCreated': "Excellent! Your profile is created in both English and your native language. You can now apply for jobs.",
        'jobPosted': "Your job opening has been posted successfully.",
        'applied': "Congratulations! You have applied for this job. The employer will call you soon.",
        'listenHelper': "Tap speaker to hear instructions, or tap microphone to speak your answer.",
    },
    'hi': {
        'welcome': "लेबर लिंक में आपका स्वागत है। अच्छे काम का पुल। कृपया अपनी भाषा चुनें।",
        'chooseRole': "क्या आप काम ढूंढ रहे हैं, या आप काम दे रहे हैं? मजदूर या नियोक्ता चुनें।",
        'enterPhone': "लॉगिन करने के लिए कृपया अपना दस अंकों का मोबाइल नंबर नीचे दर्ज करें।",
        'enterOtp': "हमने आपके मोबाइल पर एक कोड भेजा है। कृपया छह अंकों का कोड दर्ज करें।",
        'profileWizard': "आइए आपका प्रोफाइल बनाएं। यह अंग्रेजी और आपकी भाषा दोनों में बनेगा।",
        'inputName': "कृपया अपना पूरा नाम दर्ज करें।",
        'inputCategory': "वह काम चुनें जो आप करते हैं। जैसे राजमिस्त्री, प्लंबर, या ड्राइवर।",
        'inputExperience': "आपके पास कितने वर्षों का अनुभव है?",
        'inputLocation': "आप कहां काम करना चाहते हैं? अपने शहर का नाम दर्ज करें।",
        'inputBio': "मालिकों को अपने हुनर के बारे में बताएं, या अपनी आवाज में कुछ रिकॉर्ड करें।",
        'profileCreated': "बहुत बढ़िया! आपकी प्रोफाइल अंग्रेजी और हिंदी दोनों में बन गई है। अब आप नौकरियों के लिए आवेदन कर सकते हैं।",
        'jobPosted': "आपकी नौकरी का विज्ञापन सफलतापूर्वक पोस्ट कर दिया गया है।",
        'applied': "बधाई हो! आपने इस नौकरी के लिए आवेदन कर दिया है। मालिक जल्द ही आपको फोन करेंगे।",
        'listenHelper': "सुनने के लिए स्पीकर पर टैप करें। उत्तर देने के लिए माइक पर टैप करें।",
    },
    'bn': {
        'welcome': "লেবার লিঙ্কে আপনাকে স্বাগত। ভালো কাজের সেতু। অনুগ্রহ করে আপনার ভাষা বেছে নিন।",
        'chooseRole': "আপনি কি কাজ খুঁজছেন, নাকি কর্মী খুঁজছেন? শ্রমিক বা নিয়োগকর্তা নির্বাচন করুন।",
        'enterPhone': "লগইন করতে নিচে আপনার দশ সংখ্যার মোবাইল নম্বরটি লিখুন।",
        'enterOtp': "আমরা আপনার মোবাইলে একটি ভেরিফিকেশন কোড পাঠিয়েছি। ছয় সংখ্যার কোডটি এখানে লিখুন।",
        'profileWizard': "চলুন আপনার প্রোফাইল তৈরি করি। এটি ইংরেজি এবং বাংলা উভয় ভাষাতেই তৈরি হবে।",
        'inputName': "অনুগ্রহ করে আপনার পুরো নাম লিখুন।",
        'inputCategory': "আপনি যে কাজ করেন তা বেছে নিন। যেমন রাজমিস্ত্রি, প্লাম্বার বা ড্রাইভার।",
        'inputExperience': "আপনার কত বছরের অভিজ্ঞতা আছে?",
        'inputLocation': "আপনি কোথায় কাজ করতে চান? আপনার শহরের নাম লিখুন।",
        'inputBio': "মালিকদের আপনার কাজ সম্পর্কে বলুন, অথবা একটি ভয়েস রেকর্ড করুন।",
        'profileCreated': "চমৎকার! আপনার প্রোফাইল ইংরেজি এবং বাংলা দুই ভাষাতেই তৈরি হয়ে গেছে। এবার আপনি কাজের আবেদন করতে পারেন।",
        'jobPosted': "আপনার কাজের বিজ্ঞপ্তিটি সফলভাবে পোস্ট করা হয়েছে।",
        'applied': "অভিনন্দন! আপনি এই কাজটির জন্য আবেদন করেছেন। মালিক শীঘ্রই আপনাকে ফোন করবেন।",
        'listenHelper': "শোনার জন্য স্পীকারে ট্যাপ করুন। উত্তর দিতে মাইকে ট্যাপ করুন।",
    },
    'ta': {
        'welcome': "லேபர் லிங்க் தளத்திற்கு வரவேற்கிறோம். நல்ல வேலைக்கான இணைப்பு. உங்கள் மொழியைத் தேர்ந்தெடுக்கவும்.",
        'chooseRole': "நீங்கள் வேலை தேடுகிறீர்களா அல்லது வேலை தருகிறீர்களா? தொழிலாளி அல்லது முதலாளி என்பதைத் தேர்ந்தெடுக்கவும்.",
        'enterPhone': "உள்நுழைய உங்கள் பத்து இலக்க மொபைல் எண்ணை கீழே உள்ளிடவும்.",
        'enterOtp': "உங்கள் மொபைலுக்கு ஒரு சரிபார்ப்பு குறியீட்டை அனுப்பியுள்ளோம். ஆறு இலக்க குறியீட்டை உள்ளிடவும்.",
        'profileWizard': "உங்கள் சுயவிவரத்தை உருவாக்குவோம். இது ஆங்கிலம் மற்றும் உங்கள் மொழியில் உருவாக்கப்படும்.",
        'inputName': "உங்கள் முழுப் பெயரை உள்ளிடவும்.",
        'inputCategory': "நீங்கள் செய்யும் வேலையைத் தேர்ந்தெடுக்கவும். உதாரணமாக, கொத்தனார், பிளம்பர் அல்லது டிரைவர்.",
        'inputExperience': "உங்களுக்கு எத்தனை வருட அனுபவம் உள்ளது?",
        'inputLocation': "நீங்கள் எங்கு வேலை செய்ய விரும்புகிறீர்கள்? உங்கள் தற்போதைய நகரத்தை உள்ளிடவும்.",
        'inputBio': "முதலாளிகளுக்கு உங்கள் திறமைகளைப் பற்றி சொல்லுங்கள் அல்லது குரல் வாழ்த்துப் பதிவு செய்யுங்கள்.",
        'profileCreated': "அருமை! உங்கள் சுயவிவரம் ஆங்கிலம் மற்றும் தமிழ் இரண்டிலும் உருவாக்கப்பட்டுள்ளது. இப்போது நீங்கள் வேலைகளுக்கு விண்ணப்பிக்கலாம்.",
        'jobPosted': "உங்கள் வேலை அறிவிப்பு வெற்றிகரமாக வெளியிடப்பட்டது.",
        'applied': "வாழ்த்துகள்! நீங்கள் இந்த வேலைக்கு விண்ணப்பித்துவிட்டீர்கள். முதலாளி விரைவில் உங்களை அழைப்பார்.",
        'listenHelper': "உரையைக் கேட்க ஸ்பீக்கரைத் தட்டவும். உங்கள் பதிலைப் பேச மைக்ரோஃபோனைத் தட்டவும்.",
    },
    'te': {
        'welcome': "లేబర్ లింక్‌కి స్వాగతం. మంచి పనులకు వంతెన. దయచేసి మీ భాషను ఎంచుకోండి.",
        'chooseRole': "మీరు పని కోసం చూస్తున్నారా, లేదా పని ఇస్తున్నారా? కార్మికుడు లేదా యజమాని ఎంచుకోండి.",
        'enterPhone': "లాగిన్ చేయడానికి దయచేసి క్రింద మీ పది అంకెల మొబైల్ నంబర్‌ను నమోదు చేయండి.",
        'enterOtp': "మేము మీ మొబైల్‌కు ఒక కోడ్‌ని పంపాము. దయచేసి ఆరు అంకెల కోడ్‌ను నమోదు చేయండి.",
        'profileWizard': "రండి మీ ప్రొఫైల్‌ను తయారు చేద్దాం. ఇది ఇంగ్లీష్ మరియు మీ భాషలో తయారవుతుంది.",
        'inputName': "దయచేసి మీ పూర్తి పేరును టైప్ చేయండి.",
        'inputCategory': "మీరు చేసే పనిని ఎంచుకోండి. ఉదాహరణకు, తాపీ మేస్త్రీ, ప్లంబర్ లేదా డ్రైవర్.",
        'inputExperience': "మీకు ఎన్ని సంవత్సరాల అనుభవం ఉంది?",
        'inputLocation': "మీరు ఎక్కడ పని చేయాలనుకుంటున్నారు? మీ నగరం పేరు టైప్ చేయండి.",
        'inputBio': "యజమానులకు మీ నైపుణ్యాల గురించి చెప్పండి లేదా మీ వాయిస్ రिकార్డ్ చేయండి.",
        'profileCreated': "అద్భుతం! మీ ప్రొఫైల్ ఇంగ్లీష్ మరియు తెలుగు రెండింటిలోనూ సృష్టించబడింది. ఇప్పుడు మీరు ఉద్యోగాలకు దరఖాస్తు చేసుకోవచ్చు.",
        'jobPosted': "మీ ఉద్యోగ ప్రకటన విజయవంతంగా పోస్ట్ చేయబడింది.",
        'applied': "అభినందనలు! మీరు ఈ ఉద్యోగం కోసం దరఖాస్తు చేసుకున్నారు. యజమాని త్వరలోనే మీకు ఫోన్ చేస్తారు.",
        'listenHelper': "వినడానికి స్పీకర్ నొక్కండి. మీ సమాధానం మాట్లాడటానికి మైక్రోఫోన్ నొక్కండి.",
    },
    'mr': {
        'welcome': "लेबर लिंकमध्ये आपले स्वागत आहे. चांगल्या कामाचा पूल. कृपया तुमची भाषा निवडा.",
        'chooseRole': "तुम्ही काम शोधत आहात की काम देत आहात? कामगार किंवा मालक निवडा.",
        'enterPhone': "लॉगिन करण्यासाठी कृपया तुमचा दहा अंकी मोबाईल नंबर खाली टाका.",
        'enterOtp': "आम्ही तुमच्या मोबाईलवर एक कोड पाठवला आहे. कृपया सहा अंकी कोड टाका.",
        'profileWizard': "चला तुमची प्रोफाइल तयार करूया. हे इंग्रजी आणि तुमच्या भाषेत तयार होईल.",
        'inputName': "कृपया तुमचे पूर्ण नाव टाका.",
        'inputCategory': "तुम्ही करत असलेले काम निवडा. उदा. गवंडी, प्लंबर किंवा ड्रायव्हर.",
        'inputExperience': "तुम्हाला किती वर्षांचा अनुभव आहे?",
        'inputLocation': "तुम्हाला कुठे काम करायचे आहे? तुमच्या शहराचे नाव टाका.",
        'inputBio': "मालकांना तुमच्या कौशल्यांबद्दल सांगा, किंवा तुमचा आवाज रेकॉर्ड करा.",
        'profileCreated': "उत्कृष्ट! तुमची प्रोफाइल इंग्रजी आणि मराठी दोन्ही भाषेत तयार झाली आहे. आता तुम्ही नोकऱ्यांसाठी अर्ज करू शकता.",
        'jobPosted': "तुमची नोकरीची जाहिरात यशस्वीरित्या पोस्ट केली गेली आहे.",
        'applied': "अभिनंदन! तुम्ही या नोकरीसाठी अर्ज केला आहे. मालक तुम्हाला लवकरच फोन करतील.",
        'listenHelper': "ऐकण्यासाठी स्पीकरवर टॅप करा. उत्तर बोलण्यासाठी माईकवर टॅप करा.",
    }
}

# Speak out using browser text-to-speech API via javascript injection
def speak(text: str, lang_code: str = "en"):
    if not text:
        return
        
    locales = {
        'en': 'en-IN',
        'hi': 'hi-IN',
        'bn': 'bn-IN',
        'ta': 'ta-IN',
        'te': 'te-IN',
        'mr': 'mr-IN'
    }
    locale = locales.get(lang_code, "en-IN")
    escaped_text = text.replace('"', '\\"').replace('\n', ' ')
    
    js_code = f"""
    <script>
    if ('speechSynthesis' in window) {{
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance("{escaped_text}");
        utterance.lang = "{locale}";
        utterance.rate = 0.9;
        
        // Load voice
        const voices = window.speechSynthesis.getVoices();
        const voice = voices.find(v => v.lang.startsWith("{locale}") || v.lang.includes("{lang_code}"));
        if (voice) utterance.voice = voice;
        
        window.speechSynthesis.speak(utterance);
    }}
    </script>
    """
    # Write empty div with script
    components.html(js_code, height=0, width=0)

def speak_prompt(key: str, lang_code: str = "en"):
    prompt = VOICE_PROMPTS.get(lang_code, VOICE_PROMPTS['en']).get(key, "")
    if prompt:
        speak(prompt, lang_code)

# Interactive Speech Input Component
# Renders a Text Input with floating buttons to read aloud and speak to input
def speech_input(label: str, key: str, placeholder: str = "", type: str = "text", mock_type: str = "name", lang_code: str = "en"):
    col_input, col_speak, col_mic = st.columns([12, 1, 1])
    
    # Session state initialization for value
    if key not in st.session_state:
        st.session_state[key] = ""
        
    with col_input:
        if type == "textarea":
            val = st.text_area(label, value=st.session_state[key], placeholder=placeholder, key=f"inp_{key}")
        else:
            val = st.text_input(label, value=st.session_state[key], placeholder=placeholder, key=f"inp_{key}")
        st.session_state[key] = val
        
    with col_speak:
        st.write("") # spacer
        st.write("")
        if st.button("🔊", key=f"spk_btn_{key}", help="Listen to label"):
            speak(f"{label}. {placeholder}", lang_code)
            
    with col_mic:
        st.write("") # spacer
        st.write("")
        if st.button("🎤", key=f"mic_btn_{key}", help="Speak to fill"):
            # Trigger Speech recognition helper or simulator
            trigger_speech_recognition(key, mock_type, lang_code)
            
    return st.session_state[key]

# Mock Speech recognition and dynamic fill simulation
def trigger_speech_recognition(key: str, mock_type: str, lang_code: str):
    # Render simulated spinner
    with st.spinner("Listening... बोलिए..."):
        time.sleep(1.5)
        
    # Standard mocks based on language and type
    mock_values = {
        'name': {
            'en': 'Ramesh Kumar',
            'hi': 'रमेश कुमार',
            'bn': 'রমেশ কুমার',
            'ta': 'ரமேஷ் குமார்',
            'te': 'రమేష్ కుమార్',
            'mr': 'रमेश कुमार'
        },
        'location': {
            'en': 'Mumbai, Maharashtra',
            'hi': 'मुंबई, महाराष्ट्र',
            'bn': 'মুম্বাই, মহারাষ্ট্র',
            'ta': 'மும்பை, மகாராஷ்டிரா',
            'te': 'ముంబై, మహారాష్ట్ర',
            'mr': 'मुंबई, महाराष्ट्र'
        },
        'bio': {
            'en': 'I am a hard worker with five years construction experience. I specialize in bricklaying.',
            'hi': 'मुझे ५ साल का कंस्ट्रक्शन अनुभव है। मैं ईंट जोड़ने का काम अच्छे से करता हूँ।',
            'bn': 'আমি ৫ বছরের কাজের অভিজ্ঞতা সম্পন্ন একজন রাজমিস্ত্রি।',
            'ta': 'எனக்கு 5 வருட கட்டுமான வேலை अनुभव உள்ளது.',
            'te': 'నాకు భవన నిర్మాణంలో 5 సంవత్సరాల అనుభవం ఉంది.',
            'mr': 'मला ५ वर्षांचा गवंडी कामाचा अनुभव आहे.'
        },
        'salary': {
            'en': '₹15,000 / month',
            'hi': '₹15,000 / महीना',
            'bn': '₹১৫,০০০ / মাস',
            'ta': '₹15,000 / மாதம்',
            'te': '₹15,000 / నెల',
            'mr': '₹१५,००० / महिना'
        },
        'title': {
            'en': 'Construction Mason',
            'hi': 'कंस्ट्रक्शन मिस्त्री',
            'bn': 'কনস্ট্রাকশন মিস্ত্রি',
            'ta': 'கட்டுமான மேஸ்திரி',
            'te': 'తాపీ మేస్త్రీ',
            'mr': 'बांधकाम गवंडी'
        }
    }
    
    val = mock_values.get(mock_type, {}).get(lang_code, "Simulated voice input")
    st.session_state[key] = val
    
    # Speak out feedback
    speak(f"Recorded: {val}", lang_code)
    st.rerun()

# Renders browser-native WebkitSpeechRecognition component in an iframe for real mic capability
def web_speech_recognizer_widget(lang_code: str = "en"):
    locales = {'en': 'en-IN', 'hi': 'hi-IN', 'bn': 'bn-IN', 'ta': 'ta-IN', 'te': 'te-IN', 'mr': 'mr-IN'}
    locale = locales.get(lang_code, 'en-IN')
    
    html_code = f"""
    <div style="font-family: sans-serif; background: #0f2244; color: white; padding: 12px; border-radius: 8px; border: 1px solid #ffd700; display: flex; align-items: center; justify-content: space-between;">
        <span style="font-size: 14px; font-weight: bold;">🎙️ Real Microphone Assistant</span>
        <button id="rec-btn" onclick="startRecognition()" style="background: #ffd700; border: none; color: #0a192f; font-weight: bold; padding: 8px 16px; border-radius: 4px; cursor: pointer;">Start Speaking</button>
    </div>
    <div id="result-box" style="margin-top: 8px; background: #0a192f; color: #a0aec0; font-size: 13px; padding: 8px; border-radius: 4px; min-height: 40px; border: 1px solid #ffffff10;">
        Transcribed text will appear here. Click copy and paste into inputs.
    </div>

    <script>
    function startRecognition() {{
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {{
            document.getElementById('result-box').innerText = "Speech recognition not supported in this browser. Try Chrome/Edge.";
            return;
        }}
        
        const rec = new SpeechRecognition();
        rec.lang = "{locale}";
        rec.continuous = false;
        rec.interimResults = false;
        
        document.getElementById('rec-btn').innerText = "Listening...";
        document.getElementById('rec-btn').style.background = "#ff4757";
        document.getElementById('rec-btn').style.color = "white";
        
        rec.onresult = function(event) {{
            const text = event.results[0][0].transcript;
            document.getElementById('result-box').innerHTML = '<strong>Recorded:</strong> ' + text + '<br/><button onclick="navigator.clipboard.writeText(\''+text+'\')" style="margin-top:6px; background:#ffd700; border:none; padding:4px 8px; border-radius:4px; font-size:11px; cursor:pointer;">📋 Copy Text</button>';
        }};
        
        rec.onerror = function(e) {{
            document.getElementById('result-box').innerText = "Error: " + e.error;
        }};
        
        rec.onend = function() {{
            document.getElementById('rec-btn').innerText = "Start Speaking";
            document.getElementById('rec-btn').style.background = "#ffd700";
            document.getElementById('rec-btn').style.color = "#0a192f";
        }};
        
        rec.start();
    }}
    </script>
    """
    components.html(html_code, height=130)
