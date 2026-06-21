import streamlit as st
import database as db
import speech
import components
import time

# Set streamlit page configuration
st.set_page_config(
    page_title="LaborLink - Professional Network for Migrant Workers",
    page_icon="👷‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize database
db.init_db()

# Initialize session state variables
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'
if 'is_voice_guided' not in st.session_state:
    st.session_state.is_voice_guided = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'show_login' not in st.session_state:
    st.session_state.show_login = False
if 'login_step' not in st.session_state:
    st.session_state.login_step = 'phone'

# Inject premium global CSS styling
components.inject_global_css()

# Views Imports
import views.landing as landing
import views.profile_wizard as profile_wizard
import views.worker_dashboard as worker_dashboard
import views.employer_dashboard as employer_dashboard

# App Header / Navbar
col_logo, col_voice, col_user = st.columns([8, 2, 2])

with col_logo:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
        <div style="width: 44px; height: 44px; border-radius: 50%; background: #ffd700; color: #0a192f; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 22px; box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);">
            L
        </div>
        <div>
            <h1 style="margin: 0; font-size: 28px; line-height: 1; font-weight: 900; background: linear-gradient(135deg, #ffd700, #ff9f43); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">LaborLink</h1>
            <span style="font-size: 10px; color: #a0aec0; letter-spacing: 0.1em; text-transform: uppercase;">DIGNIFIED NETWORKING FOR WORKFORCE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_voice:
    st.write("") # spacer
    voice_label = "🔊 Voice Assistant: ON" if st.session_state.is_voice_guided else "🔇 Voice Assistant: OFF"
    if st.button(voice_label, key="toggle_voice_guided_btn", use_container_width=True):
        st.session_state.is_voice_guided = not st.session_state.is_voice_guided
        if st.session_state.is_voice_guided:
            st.toast("🔊 Voice Assistant Activated!")
            time.sleep(0.1)
            speech.speak("Voice assistant mode is active. Tap speaker to hear, or microphone to speak.", st.session_state.lang)
        else:
            st.toast("🔇 Voice Assistant Deactivated")
        st.rerun()

with col_user:
    st.write("") # spacer
    if st.session_state.user:
        user_role = "Worker" if st.session_state.user['role'] == 'worker' else "Employer"
        profile = st.session_state.user.get('workerProfile') or st.session_state.user.get('employerProfile')
        display_name = profile.get('name', st.session_state.user['phone']) if profile else st.session_state.user['phone']
        
        st.write(f"👤 **{display_name}** ({user_role})")
        if st.button("Sign Out", key="sign_out_btn", use_container_width=True):
            st.session_state.user = None
            st.session_state.show_login = False
            st.session_state.login_step = 'phone'
            st.toast("Logged out successfully")
            st.rerun()

# Rerouting based on Auth State
if not st.session_state.user:
    landing.show_landing()
else:
    role = st.session_state.user['role']
    if role == 'worker':
        profile = st.session_state.user.get('workerProfile')
        if not profile:
            profile_wizard.show_profile_wizard()
        else:
            worker_dashboard.show_worker_dashboard()
    else:
        employer_dashboard.show_employer_dashboard()

# Footer
st.write("---")
st.markdown("""
<div style="text-align: center; color: #718096; font-size: 12px; padding: 20px 0;">
    © 2026 LaborLink. Built with dignity for Indian workforce. Supporting English + 5 Indian languages.
</div>
""", unsafe_allow_html=True)
