import streamlit as st
import database as db
import speech
import components
import time

LANGUAGES = [
    {'code': 'en', 'name': 'English', 'native': 'English', 'flag': '🇬🇧'},
    {'code': 'hi', 'name': 'Hindi', 'native': 'हिन्दी', 'flag': '🇮🇳'},
    {'code': 'bn', 'name': 'Bengali', 'native': 'বাংলা', 'flag': '🇮🇳'},
    {'code': 'ta', 'name': 'Tamil', 'native': 'தமிழ்', 'flag': '🇮🇳'},
    {'code': 'te', 'name': 'Telugu', 'native': 'తెలుగు', 'flag': '🇮🇳'},
    {'code': 'mr', 'name': 'Marathi', 'native': 'मराठी', 'flag': '🇮🇳'}
]

def show_landing():
    lang = st.session_state.get('lang', 'en')
    
    # Render slide carousel
    components.render_carousel(lang)
    
    st.write("---")
    
    # 1. Language selector grid
    st.markdown(f"<h3 style='text-align: center;'>🌐 Choose Your Language / अपनी भाषा चुनें</h3>", unsafe_allow_html=True)
    
    # Renders columns for language cards
    cols = st.columns(6)
    for idx, lang_opt in enumerate(LANGUAGES):
        with cols[idx]:
            # Highlight current selection
            is_active = (lang == lang_opt['code'])
            label = f"{lang_opt['flag']} {lang_opt['native']}"
            
            # Interactive click card
            if st.button(label, key=f"lang_btn_{lang_opt['code']}", help=lang_opt['name']):
                st.session_state.lang = lang_opt['code']
                
                # Speak confirmation
                speak_greetings = {
                    'en': "Language changed to English.",
                    'hi': "भाषा बदलकर हिंदी हो गई है।",
                    'bn': "ভাষা পরিবর্তন করে বাংলা করা হয়েছে।",
                    'ta': "மொழி தமிழுக்கு மாற்றப்பட்டது.",
                    'te': "భాష తెలుగులోకి మార్చబడింది.",
                    'mr': "भाषा बदलून मराठी झाली आहे."
                }
                speech.speak(speak_greetings.get(lang_opt['code'], ""), lang_opt['code'])
                st.rerun()

    st.write("---")

    # 2. Main Role Selection
    st.markdown("<h3 style='text-align: center; margin-bottom: 24px;'>I want to... / मैं चाहता हूँ...</h3>", unsafe_allow_html=True)
    
    col_worker, col_employer = st.columns(2)
    
    with col_worker:
        st.markdown("""
        <div class="glass-panel zoom-card" style="text-align: center; border-radius: 12px; height: 320px; display: flex; flex-direction: column; justify-content: space-between; align-items: center;">
            <div style="font-size: 54px; margin-top: 16px;">👷‍♂️</div>
            <div>
                <h3 style="color: #ffd700; font-size: 24px; font-weight: 800; margin-bottom: 8px;">I Need Work / मुझे काम चाहिए</h3>
                <p style="font-size: 13px; color: #a0aec0; padding: 0 10px;">Create your bilingual profile via easy voice prompts. Find verified local job openings, contracts, and daily wages.</p>
            </div>
            <div style="margin-bottom: 16px;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        btn_label_w = "Find Jobs (काम खोजें)" if lang != 'en' else "Find Jobs"
        if st.button(btn_label_w, key="role_worker_btn", use_container_width=True):
            st.session_state.auth_role = 'worker'
            st.session_state.show_login = True
            speech.speak("You selected Worker. Let's verify your phone number.", lang)
            st.rerun()
            
    with col_employer:
        st.markdown("""
        <div class="glass-panel zoom-card" style="text-align: center; border-radius: 12px; height: 320px; display: flex; flex-direction: column; justify-content: space-between; align-items: center;">
            <div style="font-size: 54px; margin-top: 16px;">💼</div>
            <div>
                <h3 style="color: #ffffff; font-size: 24px; font-weight: 800; margin-bottom: 8px;">I Want to Hire / मुझे कामगार चाहिए</h3>
                <p style="font-size: 13px; color: #a0aec0; padding: 0 10px;">Post job openings, browse bilingual resumes, and hire skilled laborers, craftsmen, farm workers, and construction majors.</p>
            </div>
            <div style="margin-bottom: 16px;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        btn_label_e = "Post Openings (विज्ञापन पोस्ट करें)" if lang != 'en' else "Post Openings"
        if st.button(btn_label_e, key="role_employer_btn", use_container_width=True):
            st.session_state.auth_role = 'employer'
            st.session_state.show_login = True
            speech.speak("You selected Employer. Let's verify your recruiter account.", lang)
            st.rerun()

    # 3. OTP Login Modal Overlay Simulator
    if st.session_state.get('show_login'):
        render_login_modal(lang)

def render_login_modal(lang: str):
    role = st.session_state.auth_role
    role_title = "Worker (कामगार)" if role == 'worker' else "Employer (नियोक्ता)"
    
    st.write("")
    st.markdown(f"### 🔐 {role_title} Verification SMS Portal")
    
    with st.container(border=True):
        col_form, col_close = st.columns([12, 1])
        with col_close:
            if st.button("✕", key="close_login_btn"):
                st.session_state.show_login = False
                st.session_state.login_step = 'phone'
                st.rerun()
                
        with col_form:
            # Login Step 1: Input Phone
            if st.session_state.get('login_step', 'phone') == 'phone':
                st.write("Enter your 10-digit mobile number below. / नीचे अपना १० अंकों का मोबाइल नंबर दर्ज करें।")
                
                # Speech integrated input
                phone_val = speech.speech_input(
                    label="Mobile Number (मोबाइल नंबर)",
                    key="login_phone_input",
                    placeholder="e.g. 9876543210",
                    lang_code=lang
                )
                
                if st.button("Send Verification Code (सत्यापन कोड भेजें)", key="send_otp_btn", use_container_width=True):
                    clean_phone = "".join([c for c in phone_val if c.isdigit()])
                    if len(clean_phone) != 10:
                        err = "Please enter a valid 10-digit mobile number. / कृपया सही १० अंकों का फोन नंबर डालें।"
                        st.error(err)
                        speech.speak(err, lang)
                    else:
                        with st.spinner("Requesting Verification SMS..."):
                            otp_code = db.request_otp(clean_phone)
                            st.session_state.login_otp_sent = otp_code
                            st.session_state.login_phone = clean_phone
                            st.session_state.login_step = 'otp'
                            
                            # Trigger custom Toast & Info representing Mock SMS delivery
                            st.toast(f"💬 SMS Mock Alert: Your verification code is {otp_code}")
                            st.success(f"🔑 [MOCK SMS RECEIVED] Login code is: {otp_code}")
                            
                            time.sleep(1.0)
                            speech.speak(f"Verification code sent. Code is {', '.join(list(otp_code))}", lang)
                            st.rerun()
                            
            # Login Step 2: Verify OTP code
            else:
                st.write(f"Verification SMS sent to / कोड भेजा गया है: **{st.session_state.login_phone}**")
                
                otp_val = speech.speech_input(
                    label="Enter 6-Digit OTP (६ अंकों का कोड दर्ज करें)",
                    key="login_otp_input",
                    placeholder="Enter verification code",
                    mock_type="salary", # salary mock outputs numerical values like 15,000, perfect for OTP mock numbers!
                    lang_code=lang
                )
                
                # Resend option
                col_verify, col_change = st.columns([2, 1])
                
                with col_change:
                    if st.button("Change Number", key="change_num_btn"):
                        st.session_state.login_step = 'phone'
                        st.rerun()
                        
                with col_verify:
                    if st.button("Verify & Log In (कोड सत्यापित करें)", key="verify_otp_btn", use_container_width=True):
                        clean_otp = "".join([c for c in otp_val if c.isdigit()])
                        try:
                            # Verify and authenticate user
                            user = db.verify_otp(
                                st.session_state.login_phone,
                                clean_otp,
                                role
                            )
                            st.session_state.user = user
                            st.session_state.show_login = False
                            st.session_state.login_step = 'phone'
                            
                            st.toast("✅ Logged in successfully!")
                            speech.speak("Verification successful. Logged in.", lang)
                            time.sleep(0.5)
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
                            speech.speak(str(e), lang)
                            
                # Mock helper box displaying code again for ease
                st.info(f"💡 Mock SMS: Code is {st.session_state.login_otp_sent}. Type it above or use bypass code 123456.")
