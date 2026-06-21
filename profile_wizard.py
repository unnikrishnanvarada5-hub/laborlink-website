import streamlit as st
import database as db
import speech
import time

CATEGORIES = [
  { 'id': 'Construction', 'label': 'Construction', 'labelNative': 'राजमिस्त्री / निर्माण कार्य', 'icon': '🏗️' },
  { 'id': 'Plumbing', 'label': 'Plumbing', 'labelNative': 'नलसाज (Plumber)', 'icon': '🚰' },
  { 'id': 'Electrical', 'label': 'Electrical', 'labelNative': 'बिजली मिस्त्री (Electrician)', 'icon': '⚡' },
  { 'id': 'Agriculture', 'label': 'Agriculture', 'labelNative': 'खेती / किसान', 'icon': '🌾' },
  { 'id': 'Housekeeping', 'label': 'Housekeeping', 'labelNative': 'घरेलू सहायक / साफ-सफाई', 'icon': '🧹' },
  { 'id': 'Driving', 'label': 'Driving', 'labelNative': 'चालक / ड्राइवर', 'icon': '🚗' },
  { 'id': 'Security', 'label': 'Security', 'labelNative': 'सुरक्षा गार्ड', 'icon': '🛡️' }
]

def show_profile_wizard():
    lang = st.session_state.get('lang', 'en')
    user = st.session_state.user
    
    # Initialize wizard steps
    if 'wiz_step' not in st.session_state:
        st.session_state.wiz_step = 1
        speech.speak_prompt('profileWizard', lang)
        
    step = st.session_state.wiz_step

    st.markdown(f"<h2 style='text-align: center;'>Create Your Resume / अपना प्रोफाइल बनाएं</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #a0aec0;'>Step {step} of 6</p>", unsafe_allow_html=True)
    
    # Progress Bar
    st.progress(step / 6.0)
    st.write("")

    # STEP 1: Introduce Wizard details
    if step == 1:
        st.markdown("""
        <div class="glass-panel" style="text-align: center; padding: 40px;">
            <div style="font-size: 64px; margin-bottom: 16px;">🗣️📱</div>
            <h3 style="font-size: 22px; font-weight: 700; margin-bottom: 16px;">Dual-Language & Voice Guided Profile</h3>
            <p style="color: #a0aec0; font-size: 15px; line-height: 1.6; margin-bottom: 24px;">
                We help you build your profile in both English and your native language. 
                This makes it easy for major employers nationwide to understand your expertise.
                You can use the 🎙️ (microphone) buttons at any time to speak your answers.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Let's Start (शुरू करें)", key="wiz_start_btn", use_container_width=True):
            st.session_state.wiz_step = 2
            speech.speak_prompt('inputName', lang)
            st.rerun()

    # STEP 2: Name Input
    elif step == 2:
        st.markdown("### What is your full name? / आपका पूरा नाम क्या है?")
        
        name_native = speech.speech_input(
            label="Enter Name in Native Language (अपना नाम दर्ज करें)",
            key="wiz_name_native",
            placeholder="e.g. रमेश कुमार",
            mock_type="name",
            lang_code=lang
        )
        
        # Auto translation simulation
        name_en = name_native # duplicate name in English profile for ease of reading
        st.session_state.wiz_name_en = name_en
        
        st.write("")
        st.markdown(f"""
        <div style="padding: 16px; background: #0f2244; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
            <div style="font-size: 11px; color: #a0aec0; font-weight: 600; text-transform: uppercase;">English Profile Autotranslation</div>
            <div style="font-size: 18px; color: #ffd700; margin-top: 4px; font-weight: bold;">
                {name_en if name_en else 'English translation will appear here...'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        render_nav_buttons(disabled=not name_native)

    # STEP 3: Job Category Selection
    elif step == 3:
        st.markdown("### What work do you specialize in? / आप किस काम में कुशल हैं?")
        st.write("Select one skill: / एक विकल्प चुनें:")
        
        # Grid of category cards
        selected_cat = st.session_state.get('wiz_category', '')
        
        cols = st.columns(3)
        for idx, cat in enumerate(CATEGORIES):
            col_idx = idx % 3
            with cols[col_idx]:
                label = f"{cat['icon']} {cat['labelNative'] if lang != 'en' else cat['label']}"
                is_selected = (selected_cat == cat['id'])
                
                # Dynamic style
                btn_type = "primary" if is_selected else "secondary"
                
                if st.button(label, key=f"cat_btn_{cat['id']}", use_container_width=True):
                    st.session_state.wiz_category = cat['id']
                    st.session_state.wiz_category_native = cat['labelNative']
                    
                    speech.speak(f"Selected {cat['label'] if lang == 'en' else cat['labelNative']}", lang)
                    st.rerun()
                    
        render_nav_buttons(disabled=not selected_cat)

    # STEP 4: Experience & Location
    elif step == 4:
        st.markdown("### Experience & Preferred Location / अनुभव और शहर")
        
        # Experience slider
        exp_years = st.slider(
            "Years of experience / कार्य अनुभव (वर्ष):",
            min_value=0, max_value=20, value=st.session_state.get('wiz_exp', 1), step=1,
            key="wiz_exp_slider"
        )
        st.session_state.wiz_exp = exp_years
        
        # Location input
        loc_native = speech.speech_input(
            label="Which city do you want to work in? (आप किस शहर में काम करना चाहते हैं?)",
            key="wiz_loc_native",
            placeholder="जैसे: मुंबई, दिल्ली, पुणे",
            mock_type="location",
            lang_code=lang
        )
        
        # Auto-translation lookup
        loc_en = db.translate_text(loc_native, 'en')
        st.session_state.wiz_loc_en = loc_en
        
        st.markdown(f"**English Location:** {loc_en if loc_en else 'Autotranslation pending...'}")
        
        render_nav_buttons(disabled=not loc_native)

    # STEP 5: Bio details & Voice Greeting Simulator
    elif step == 5:
        st.markdown("### Introduce Yourself / अपना परिचय दें")
        
        bio_native = speech.speech_input(
            label="Tell employers about your skills (Optional) / अपने कौशल के बारे में बताएं",
            key="wiz_bio_native",
            placeholder="जैसे: मुझे छत ढलाई और प्लास्टर का पूरा काम आता है।",
            type="textarea",
            mock_type="bio",
            lang_code=lang
        )
        
        bio_en = db.translate_text(bio_native, 'en')
        st.session_state.wiz_bio_en = bio_en
        
        st.write("---")
        
        # Voice Greeting Simulation
        st.markdown("#### 🎤 Record Voice Greeting / अपनी आवाज़ रिकॉर्ड करें")
        st.write("Employers love to hear your voice directly. Record a 10 second greeting.")
        
        col_rec, col_status = st.columns([1, 2])
        
        # Simulated recording trigger
        with col_rec:
            if st.button("Start Recording", key="wiz_rec_btn", use_container_width=True):
                st.session_state.wiz_recording = True
                speech.speak("Recording voice greeting. Speak now.", lang)
                
                # Animate progress bar simulation
                progress_text = "Recording... / रिकॉर्डिंग हो रही है..."
                my_bar = st.progress(0, text=progress_text)
                for percent_complete in range(100):
                    time.sleep(0.02)
                    my_bar.progress(percent_complete + 1, text=progress_text)
                
                my_bar.empty()
                st.session_state.wiz_recording = False
                st.session_state.wiz_voice_attached = True
                speech.speak("Voice greeting saved successfully.", lang)
                st.toast("✅ Voice Greeting Recorded!")
                st.rerun()
                
        with col_status:
            if st.session_state.get('wiz_voice_attached'):
                st.success("✓ Voice message successfully recorded! (mock-greeting.wav)")
            else:
                st.info("No audio greeting attached yet.")

        # Real audio recorder widget
        st.write("Or use the real microphone to transcribe custom text:")
        speech.web_speech_recognizer_widget(lang)
        
        render_nav_buttons()

    # STEP 6: Side-by-Side Bilingual Verification
    elif step == 6:
        st.markdown("### Verify Your Resume / अपने प्रोफाइल की जांच करें")
        st.write("Here is how your profile will look to local and national employers:")
        
        name_native = st.session_state.wiz_name_native
        name_en = st.session_state.get('wiz_name_en', name_native)
        cat_id = st.session_state.wiz_category
        cat_native = st.session_state.wiz_category_native
        exp = st.session_state.wiz_exp
        loc_native = st.session_state.wiz_loc_native
        loc_en = st.session_state.wiz_loc_en
        bio_native = st.session_state.wiz_bio_native
        bio_en = st.session_state.wiz_bio_en
        voice_greeting = "mock-audio-file.mp3" if st.session_state.get('wiz_voice_attached') else None
        
        col_native_card, col_english_card = st.columns(2)
        
        with col_native_card:
            st.markdown(f"""
            <div style="padding: 24px; background: rgba(255,215,0,0.03); border-radius: 12px; border: 2px solid #ffd700; height: 350px;">
                <div style="font-size: 11px; font-weight: 800; color: #ffd700; text-transform: uppercase; margin-bottom: 8px;">Native Language Profile ({lang.upper()})</div>
                <h4 style="font-size: 20px; font-weight: 800; color: white; margin-bottom: 4px;">{name_native}</h4>
                <div style="font-size: 14px; color: #a0aec0;">🛠️ {cat_native}</div>
                <div style="font-size: 14px; color: #a0aec0;">💼 {exp} वर्ष का अनुभव</div>
                <div style="font-size: 14px; color: #a0aec0;">📍 {loc_native}</div>
                <div style="font-size: 14px; color: #f8f9fa; margin-top: 16px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 12px; height: 120px; overflow: hidden;">
                    <strong>परिचय:</strong> {bio_native if bio_native else 'कुशल कामगार।'}
                </div>
                {"<div style='font-size:12px; color:#2ed573; font-weight:bold; margin-top:10px;'>🎤 आवाज संदेश उपलब्ध है</div>" if voice_greeting else ""}
            </div>
            """, unsafe_allow_html=True)
            
        with col_english_card:
            st.markdown(f"""
            <div style="padding: 24px; background: rgba(255,255,255,0.02); border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); height: 350px;">
                <div style="font-size: 11px; font-weight: 800; color: #a0aec0; text-transform: uppercase; margin-bottom: 8px;">English Profile View</div>
                <h4 style="font-size: 20px; font-weight: 800; color: white; margin-bottom: 4px;">{name_en}</h4>
                <div style="font-size: 14px; color: #a0aec0;">🛠️ {cat_id} Worker</div>
                <div style="font-size: 14px; color: #a0aec0;">💼 {exp} Years of Experience</div>
                <div style="font-size: 14px; color: #a0aec0;">📍 {loc_en}</div>
                <div style="font-size: 14px; color: #f8f9fa; margin-top: 16px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 12px; height: 120px; overflow: hidden;">
                    <strong>Bio:</strong> {bio_en if bio_en else 'Skilled worker.'}
                </div>
                {"<div style='font-size:12px; color:#a0aec0; margin-top:10px;'>🎤 Voice greeting attached</div>" if voice_greeting else ""}
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        if st.button("Finish & Save Profile (सहेजें और समाप्त करें)", key="wiz_save_btn", use_container_width=True):
            # Save in database
            profile_data = {
                'name': name_en,
                'nameNative': name_native,
                'nativeLanguage': lang,
                'category': cat_id,
                'categoryNative': cat_native,
                'experienceYears': exp,
                'location': loc_en,
                'locationNative': loc_native,
                'bio': bio_en if bio_en else f"Hi, my name is {name_en}. I specialize in {cat_id} work in {loc_en}.",
                'bioNative': bio_native if bio_native else f"{name_native} नाम है। मैं {loc_native} में {cat_native} काम ढूंढ रहा हूँ।",
                'voiceGreetingUrl': voice_greeting
            }
            
            updated_user = db.update_worker_profile(user['id'], profile_data)
            st.session_state.user = updated_user
            
            st.toast("✅ Profile Created!")
            speech.speak_prompt('profileCreated', lang)
            time.sleep(1.0)
            st.rerun()

        # Prev button
        if st.button("← Back", key="wiz_prev_btn_final"):
            st.session_state.wiz_step = 5
            st.rerun()

def render_nav_buttons(disabled: bool = False):
    st.write("")
    col_prev, col_next = st.columns([1, 1])
    step = st.session_state.wiz_step
    lang = st.session_state.get('lang', 'en')
    
    with col_prev:
        if st.button("← Back", key=f"wiz_prev_btn_{step}"):
            st.session_state.wiz_step = step - 1
            st.rerun()
            
    with col_next:
        if st.button("Continue →", key=f"wiz_next_btn_{step}", disabled=disabled):
            st.session_state.wiz_step = step + 1
            
            # Speak prompt for next step
            next_prompts = {
                3: 'inputCategory',
                4: 'inputExperience',
                5: 'inputBio'
            }
            next_step = step + 1
            if next_step in next_prompts:
                speech.speak_prompt(next_prompts[next_step], lang)
                
            st.rerun()
