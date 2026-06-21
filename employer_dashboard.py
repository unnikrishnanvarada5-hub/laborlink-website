import streamlit as st
import database as db
import speech
import time

def show_employer_dashboard():
    user = st.session_state.user
    emp_profile = user.get('employerProfile')
    
    # Navigation tabs
    tab_jobs, tab_workers, tab_applications, tab_profile = st.tabs([
        "💼 My Job Openings",
        "👷‍♂️ Candidate Registry",
        "📩 Received Applications",
        "🏢 Company Profile"
    ])
    
    # Reload data
    jobs = [j for j in db.get_all_jobs() if j['employer_id'] == user['id']]
    workers = db.get_all_workers()
    applications = db.get_job_applications_for_employer(user['id'])

    # 1. JOB OPENINGS TAB
    with tab_jobs:
        col_title, col_post = st.columns([3, 1])
        with col_title:
            st.markdown("### My Posted Openings")
        with col_post:
            if st.button("➕ Post New Opening", key="post_opening_trigger_btn", use_container_width=True):
                st.session_state.emp_show_post_modal = True
                st.rerun()

        # Job post modal overlay
        if st.session_state.get('emp_show_post_modal'):
            render_post_job_form(user['id'])

        if not jobs:
            st.info("You have not posted any job openings yet. Click 'Post New Opening' to start.")
        else:
            for job in jobs:
                with st.container(border=True):
                    col_det, col_langs = st.columns([4, 1])
                    with col_det:
                        st.markdown(f"#### {job['title']}")
                        st.write(f"Category: **{job['category']}** | Posted: **{job['posted_date']}**")
                    with col_langs:
                        st.write(f"Languages: **{job['languages']}**")
                        
                    col_en, col_nat = st.columns(2)
                    with col_en:
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.01); padding: 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.05); min-height: 120px;">
                            <strong style="font-size: 11px; color: #a0aec0;">ENGLISH DETAILS</strong><br/>
                            📍 {job['location']} <br/>
                            💰 {job['salary']} <br/>
                            📝 {job['description']}
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with col_nat:
                        st.markdown(f"""
                        <div style="background: rgba(255,215,0,0.02); padding: 12px; border-radius: 6px; border: 1px solid #ffd70030; min-height: 120px;">
                            <strong style="font-size: 11px; color: #ffd700;">NATIVE TRANSLATION</strong><br/>
                            शीर्षक: {job['title_native']} <br/>
                            स्थान: {job['location_native']} <br/>
                            वेतन: {job['salary_native']} <br/>
                            विवरण: {job['description_native']}
                        </div>
                        """, unsafe_allow_html=True)

    # 2. CANDIDATE TALENT REGISTRY
    with tab_workers:
        st.markdown("### Talent Registry (Bilingual Workers)")
        if not workers:
            st.info("No worker profiles are registered on the platform yet.")
        else:
            for worker in workers:
                with st.container(border=True):
                    col_info, col_actions = st.columns([3, 1])
                    with col_info:
                        st.markdown(f"#### {worker['name']} ({worker['name_native']})")
                        st.write(f"🛠️ Category: **{worker['category']} ({worker['category_native']})** | Experience: **{worker['experience_years']} Years**")
                        st.write(f"📍 Location: **{worker['location']} ({worker['location_native']})**")
                    with col_actions:
                        # Simulated greeting speak
                        if st.button("🔊 Listen Greeting", key=f"speak_candidate_{worker['user_id']}", use_container_width=True):
                            speech_bio = f"Candidate {worker['name']}. Category {worker['category']}. Experience {worker['experience_years']} years. Bio is: {worker['bio']}."
                            speech.speak(speech_bio, 'en')
                            
                        # Call candidate link
                        st.markdown(f"""
                        <a href="tel:{worker['phone']}" style="display:block; text-align:center; background:#ffd700; color:#0a192f; font-weight:bold; padding:8px; border-radius:8px; text-decoration:none; margin-top:8px;">
                            📞 Call: {worker['phone']}
                        </a>
                        """, unsafe_allow_html=True)
                        
                    col_bio_nat, col_bio_en = st.columns(2)
                    with col_bio_nat:
                        st.markdown(f"""
                        <div style="background: rgba(255,215,0,0.01); padding: 10px; border-radius: 6px; border: 1px solid #ffd70020; font-size:13px;">
                            <strong>Native Bio ({worker['native_language']}):</strong> {worker['bio_native']}
                        </div>
                        """, unsafe_allow_html=True)
                    with col_bio_en:
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.01); padding: 10px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.05); font-size:13px;">
                            <strong>English Bio:</strong> {worker['bio']}
                        </div>
                        """, unsafe_allow_html=True)

    # 3. APPLICATIONS RECEIVED TAB
    with tab_applications:
        st.markdown("### Job Applicants Reviews")
        if not applications:
            st.info("No candidates have applied for your posted jobs yet.")
        else:
            for app in applications:
                with st.container(border=True):
                    col_app_info, col_app_actions = st.columns([3, 1])
                    with col_app_info:
                        st.markdown(f"<span style='background:#ffd70020; color:#ffd700; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:bold;'>APPLIED FOR: {app['job_title']}</span>", unsafe_allow_html=True)
                        st.markdown(f"#### {app['worker_name']} ({app['worker_name_native']})")
                        st.write(f"Applied Date: **{app['applied_date']}** | Phone: **{app['worker_phone']}**")
                    with col_app_actions:
                        st.markdown(f"""
                        <a href="tel:{app['worker_phone']}" style="display:block; text-align:center; background:#ffd700; color:#0a192f; font-weight:bold; padding:10px; border-radius:8px; text-decoration:none;">
                            📞 Call Candidate
                        </a>
                        """, unsafe_allow_html=True)
                        
                    col_app_nat, col_app_en = st.columns(2)
                    with col_app_nat:
                        st.write("**Worker Profile (Native):**")
                        st.write(f"Location: {app['worker_location_native']}")
                        st.write(f"Bio: {app['worker_bio_native']}")
                    with col_app_en:
                        st.write("**Worker Profile (English):**")
                        st.write(f"Location: {app['worker_location']}")
                        st.write(f"Bio: {app['worker_bio']}")

    # 4. COMPANY PROFILE TAB
    with tab_profile:
        st.markdown("### Company Profile details")
        with st.form("company_profile_form"):
            c_name = st.text_input("Contact Person Name", value=emp_profile.get('name', '') if emp_profile else '')
            c_company = st.text_input("Company / Firm Name", value=emp_profile.get('company', '') if emp_profile else '')
            c_loc = st.text_input("Office City", value=emp_profile.get('location', '') if emp_profile else '')
            c_desc = st.text_area("About Company", value=emp_profile.get('description', '') if emp_profile else '')
            
            if st.form_submit_button("Save Profile"):
                prof_data = {
                    'name': c_name,
                    'company': c_company,
                    'phone': user['phone'],
                    'location': c_loc,
                    'description': c_desc
                }
                updated_user = db.update_employer_profile(user['id'], prof_data)
                st.session_state.user = updated_user
                st.success("Profile saved successfully!")
                time.sleep(0.8)
                st.rerun()

def render_post_job_form(employer_id: str):
    st.write("")
    st.markdown("### 💼 Create Job Opening")
    
    with st.container(border=True):
        col_form, col_close = st.columns([12, 1])
        with col_close:
            if st.button("✕", key="close_post_job_btn"):
                st.session_state.emp_show_post_modal = False
                st.rerun()
                
        with col_form:
            # Form setup
            j_title = st.text_input("Job Title (English)", placeholder="e.g. Mason / Plumber Helper")
            
            j_cat = st.selectbox("Job Category", options=[
                "Construction", "Plumbing", "Electrical", "Agriculture", "Housekeeping", "Driving", "Security"
            ])
            
            j_loc = st.text_input("Job Location (English)", placeholder="e.g. Pune, MH")
            j_sal = st.text_input("Salary / Wage (English)", placeholder="e.g. ₹18,000 / month")
            j_desc = st.text_area("Job Description (English)", placeholder="Describe roles, provisions...")
            
            # Target language
            target_langs = st.multiselect(
                "Select Target Languages for Workers",
                options=["hi", "bn", "ta", "te", "mr"],
                default=["hi"]
            )
            
            # Live translation preview calculation
            primary_lang = target_langs[0] if target_langs else "hi"
            j_title_nat = db.translate_text(j_title, primary_lang)
            j_loc_nat = db.translate_text(j_loc, primary_lang)
            j_sal_nat = db.translate_text(j_sal, primary_lang)
            j_desc_nat = db.translate_text(j_desc, primary_lang)
            
            st.write("---")
            st.markdown("#### Live Bilingual Preview")
            col_pr_en, col_pr_nat = st.columns(2)
            with col_pr_en:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.01); padding: 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.05); min-height: 120px; font-size: 13px;">
                    <strong style="color: #a0aec0;">ENGLISH VIEW</strong><br/>
                    <strong>Title:</strong> {j_title if j_title else '...'} <br/>
                    <strong>Location:</strong> {j_loc if j_loc else '...'} <br/>
                    <strong>Salary:</strong> {j_sal if j_sal else '...'} <br/>
                    <strong>Desc:</strong> {j_desc if j_desc else '...'}
                </div>
                """, unsafe_allow_html=True)
            with col_pr_nat:
                st.markdown(f"""
                <div style="background: rgba(255,215,0,0.02); padding: 12px; border-radius: 6px; border: 1px solid #ffd70030; min-height: 120px; font-size: 13px;">
                    <strong style="color: #ffd700;">NATIVE PREVIEW ({primary_lang.upper()})</strong><br/>
                    <strong>शीर्षक:</strong> {j_title_nat if j_title_nat else '...'} <br/>
                    <strong>स्थान:</strong> {j_loc_nat if j_loc_nat else '...'} <br/>
                    <strong>वेतन:</strong> {j_sal_nat if j_sal_nat else '...'} <br/>
                    <strong>विवरण:</strong> {j_desc_nat if j_desc_nat else '...'}
                </div>
                """, unsafe_allow_html=True)
                
            st.write("")
            if st.button("Publish Bilingual Job Posting", key="submit_post_job_btn", use_container_width=True):
                if not j_title or not j_loc or not j_sal or not j_desc:
                    st.error("Please fill in all English fields. Translations are auto-generated.")
                else:
                    db.post_job(employer_id, {
                        'title': j_title,
                        'titleNative': j_title_nat,
                        'category': j_cat,
                        'location': j_loc,
                        'locationNative': j_loc_nat,
                        'salary': j_sal,
                        'salaryNative': j_sal_nat,
                        'description': j_desc,
                        'descriptionNative': j_desc_nat,
                        'languages': target_langs
                    })
                    st.toast("✅ Job Opening Published!")
                    speech.speak_prompt('jobPosted', 'en')
                    st.session_state.emp_show_post_modal = False
                    time.sleep(0.8)
                    st.rerun()
ZOOM_CARD_STYLE = """
"""
