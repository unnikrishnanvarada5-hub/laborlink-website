import streamlit as st
import database as db
import speech
import time

def show_worker_dashboard():
    lang = st.session_state.get('lang', 'en')
    user = st.session_state.user
    profile = user.get('workerProfile')

    # Load data
    jobs = db.get_all_jobs()
    applications = db.get_applications_for_worker(user['id'])

    # Header Card
    st.markdown(f"""
    <div class="glass-panel" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <div style="font-size: 32px; display: inline-block; vertical-align: middle; margin-right: 12px;">👷‍♂️</div>
            <div style="display: inline-block; vertical-align: middle;">
                <h2 style="margin: 0; font-size: 24px; font-weight: 800; color: white;">
                    Welcome back / स्वागत है, {profile['name_native'] if profile else user['phone']}!
                </h2>
                <p style="margin: 4px 0 0 0; font-size: 13px; color: #a0aec0;">
                    Bilingual Resume Status: Active | Selected Location: {profile['location_native'] if profile else 'Not Set'}
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")

    # View Resume Button
    if st.button("📄 View My Resume (मेरा प्रोफाइल देखें)", key="worker_view_resume_btn"):
        st.session_state.worker_show_resume = True
        st.rerun()

    if st.session_state.get('worker_show_resume'):
        render_resume_dialog(profile, lang)

    # Grid columns
    col_filters, col_jobs = st.columns([1, 2])

    # Left Column: FILTERS & APPLICATIONS TRACKER
    with col_filters:
        with st.container(border=True):
            st.markdown("### 🔍 Filter Work / काम चुनें")
            categories = ['All', 'Construction', 'Plumbing', 'Electrical', 'Agriculture', 'Housekeeping', 'Driving', 'Security']
            
            selected_cat = st.selectbox(
                "Select Category / काम की श्रेणी:",
                options=categories,
                index=0,
                key="worker_filter_cat"
            )
            
            search_loc = st.text_input(
                "Search City / शहर खोजें:",
                placeholder="e.g. Mumbai, Pune",
                key="worker_filter_loc"
            )
            
        st.write("")
        
        # My Applications Tracker
        with st.container(border=True):
            st.markdown(f"### 📩 My Applications ({len(applications)}) / मेरे आवेदन")
            if not applications:
                st.write("You have not applied for any jobs yet. / आपने अभी तक किसी काम के लिए आवेदन नहीं किया है।")
            else:
                for app in applications:
                    status_color = "#ffd700" if app['status'] == 'pending' else "#2ed573"
                    job_title_display = app['title'] if lang == 'en' else app['title_native']
                    
                    st.markdown(f"""
                    <div style="padding: 12px; background: #0f2244; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 8px;">
                        <div style="font-weight: bold; font-size: 14px; color: white;">{job_title_display}</div>
                        <div style="font-size: 11px; color: #a0aec0;">{app['company_name']}</div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
                            <span style="font-size: 10px; color: #718096;">{app['applied_date']}</span>
                            <span style="font-size: 11px; font-weight: bold; color: {status_color}; text-transform: uppercase;">
                                {app['status']}
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # Right Column: JOBS LIST BOARD
    with col_jobs:
        st.markdown("### 💼 Available Job Openings / उपलब्ध नौकरियां")
        
        # Filter jobs
        filtered_jobs = []
        for job in jobs:
            matches_cat = (selected_cat == 'All' or job['category'] == selected_cat)
            matches_loc = (not search_loc or 
                           search_loc.lower() in job['location'].lower() or 
                           search_loc.lower() in job['location_native'].lower())
            if matches_cat and matches_loc:
                filtered_jobs.append(job)
                
        if not filtered_jobs:
            st.info("No job openings match your filter settings. / आपकी खोज के अनुसार कोई नौकरी नहीं मिली।")
        else:
            for job in filtered_jobs:
                already_applied = any(app['job_id'] == job['id'] for app in applications)
                
                with st.container(border=True):
                    # Header
                    title_display = job['title'] if lang == 'en' else job['title_native']
                    loc_display = job['location'] if lang == 'en' else job['location_native']
                    sal_display = job['salary'] if lang == 'en' else job['salary_native']
                    desc_display = job['description'] if lang == 'en' else job['description_native']
                    
                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                        <div>
                            <h4 style="margin: 0; font-size: 18px; font-weight: 800; color: #ffd700;">{title_display}</h4>
                            <div style="font-size: 12px; color: #a0aec0; font-weight: 600;">{job['company_name']} ({job['employer_name']})</div>
                        </div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 13px; color: #a0aec0; margin-bottom: 12px;">
                        <div>📍 Location: <strong>{loc_display}</strong></div>
                        <div>💰 Salary: <strong>{sal_display}</strong></div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style="background: #0f2244; padding: 12px; border-radius: 6px; font-size: 13px; border-left: 3px solid #ffd700; color: white;">
                        {desc_display}
                        {f"<div style='margin-top: 8px; border-top: 1px solid rgba(255,255,255,0.05); padding-top:6px; color:#718096; font-style:italic;'>English: {job['description']}</div>" if lang != 'en' else ""}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.write("")
                    
                    # Buttons col
                    col_play, col_apply = st.columns([1, 1])
                    
                    with col_play:
                        if st.button("🔊 Listen Details", key=f"job_spk_{job['id']}", use_container_width=True):
                            speech_desc = f"Job opening for {job['title']} at {job['company_name']}. Salary is {job['salary']}. Description is {job['description']}" if lang == 'en' else f"नौकरी की जानकारी: {job['title_native']}. कंपनी: {job['company_name']}. वेतन: {job['salary_native']}. विवरण: {job['description_native']}."
                            speech.speak(speech_desc, lang)
                            
                    with col_apply:
                        btn_apply_label = "✓ Applied" if already_applied else "Apply (आवेदन करें)"
                        if st.button(btn_apply_label, key=f"job_app_{job['id']}", disabled=already_applied, use_container_width=True):
                            db.apply_for_job(user['id'], job['id'])
                            st.toast("✅ Applied successfully!")
                            speech.speak_prompt('applied', lang)
                            time.sleep(1.0)
                            st.rerun()

def render_resume_dialog(profile: dict, lang: str):
    st.write("")
    st.markdown("### 📄 My Bilingual Resume / मेरा प्रोफाइल")
    
    with st.container(border=True):
        col_close_btn = st.columns([12, 1])[1]
        if col_close_btn.button("✕", key="close_res_btn"):
            st.session_state.worker_show_resume = False
            st.rerun()
            
        if not profile:
            st.warning("Resume details not complete. Please fill out details.")
            return

        col_nat, col_eng = st.columns(2)
        with col_nat:
            st.markdown(f"""
            <div style="padding: 16px; background: rgba(255,215,0,0.02); border-radius: 8px; border: 1px solid #ffd700; min-height: 250px;">
                <div style="font-size: 10px; font-weight: 800; color: #ffd700; text-transform: uppercase;">Native Language ({lang.upper()})</div>
                <h4 style="font-size: 18px; margin-top: 4px;">{profile['name_native']}</h4>
                <div style="font-size: 13px; color: #a0aec0;">🛠️ Category: {profile['category_native']}</div>
                <div style="font-size: 13px; color: #a0aec0;">💼 Experience: {profile['experience_years']} वर्ष</div>
                <div style="font-size: 13px; color: #a0aec0;">📍 Location: {profile['location_native']}</div>
                <p style="font-size: 13px; margin-top: 8px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 6px; color: white;">
                    <strong>परिचय:</strong> {profile['bio_native']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        with col_eng:
            st.markdown(f"""
            <div style="padding: 16px; background: rgba(255,255,255,0.01); border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); min-height: 250px;">
                <div style="font-size: 10px; font-weight: 800; color: #a0aec0; text-transform: uppercase;">English Resume</div>
                <h4 style="font-size: 18px; margin-top: 4px;">{profile['name']}</h4>
                <div style="font-size: 13px; color: #a0aec0;">🛠️ Category: {profile['category']}</div>
                <div style="font-size: 13px; color: #a0aec0;">💼 Experience: {profile['experience_years']} Years</div>
                <div style="font-size: 13px; color: #a0aec0;">📍 Location: {profile['location']}</div>
                <p style="font-size: 13px; margin-top: 8px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 6px; color: white;">
                    <strong>Bio:</strong> {profile['bio']}
                </p>
            </div>
            """, unsafe_allow_html=True)
