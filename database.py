import sqlite3
import os
import time
import random

DB_FILE = "laborlink.db"

# Translation Dictionary for Auto-Filling Bilingual Profiles
TRANSLATIONS = {
    'hi': {
        'Construction': 'राजमिस्त्री / निर्माण कार्य',
        'Plumbing': 'नलसाज (Plumber)',
        'Electrical': 'बिजली मिस्त्री (Electrician)',
        'Agriculture': 'खेती / किसान',
        'Housekeeping': 'घरेलू सहायक / साफ-सफाई',
        'Driving': 'चालक / ड्राइवर',
        'Security': 'सुरक्षा गार्ड',
        'experience': 'साल का अनुभव',
        'years': 'वर्ष',
        'location': 'स्थान',
        'skills': 'कौशल',
        'bio': 'मेरे बारे में',
        'Mason': 'राजमिस्त्री',
        'Plumber': 'नलसाज',
        'Electrician': 'बिजली मिस्त्री',
        'Helper': 'सहायक / मजदूर',
        'Farm Laborer': 'खेत मजदूर',
        'Housekeeper': 'हाउसकीपर',
        'Delivery Rider': 'डिलीवरी राइडर',
        'Security Guard': 'सुरक्षा गार्ड',
    },
    'bn': {
        'Construction': 'নির্মাণ কর্মী / রাজমিস্ত্রি',
        'Plumbing': 'কল মিস্ত্রি (Plumber)',
        'Electrical': 'বিদ্যুৎ মিস্ত্রি (Electrician)',
        'Agriculture': 'কৃষি কাজ / কৃষক',
        'Housekeeping': 'গৃহকর্মী / পরিষ্কারক',
        'Driving': 'চালক / ড্রাইভার',
        'Security': 'নিরাপত্তা কর্মী',
        'experience': 'বছরের অভিজ্ঞতা',
        'years': 'বছর',
        'location': 'স্থান',
        'skills': 'দক্ষতা',
        'bio': 'আমার সম্পর্কে',
        'Mason': 'রাজমিস্ত্রি',
        'Plumber': 'কল মিস্ত্রি',
        'Electrician': 'বিদ্যুৎ মিস্ত্রি',
        'Helper': 'সহকারী কর্মী',
        'Farm Laborer': 'কৃষি শ্রমিক',
        'Housekeeper': 'গৃহকর্মী',
        'Delivery Rider': 'ডেলিভারি রাইডার',
        'Security Guard': 'নিরাপত্তা রক্ষী',
    },
    'ta': {
        'Construction': 'கட்டுமானப் பணி / மேஸ்திரி',
        'Plumbing': 'குழாய் பழுதுபார்ப்பவர் (Plumber)',
        'Electrical': 'மின்சார வல்லுநர் (Electrician)',
        'Agriculture': 'விவசாயம் / பண்ணை வேலை',
        'Housekeeping': 'வீட்டு உதவியாளர்',
        'Driving': 'ஓட்டுநர் / டிரைவர்',
        'Security': 'பாதுகாப்பு காவலர்',
        'experience': 'வருட அனுபவம்',
        'years': 'வருடங்கள்',
        'location': 'இடம்',
        'skills': 'திறன்கள்',
        'bio': 'என்னைப் பற்றி',
        'Mason': 'கொத்தனார் / மேஸ்திரி',
        'Plumber': 'பிளம்பர்',
        'Electrician': 'எலக்ட்ரீஷியன்',
        'Helper': 'உதவியாளர்',
        'Farm Laborer': 'விவசாய தொழிலாளி',
        'Housekeeper': 'வீட்டு வேலைக்காரர்',
        'Delivery Rider': 'டெலிவரி ரைடர்',
        'Security Guard': 'பாதுகாப்பு காவலர்',
    },
    'te': {
        'Construction': 'తాపీ మేస్త్రీ / భవన నిర్మాణం',
        'Plumbing': 'ప్లంబర్ (Plumbing)',
        'Electrical': 'ఎలక్ట్రీషియన్ (Electrician)',
        'Agriculture': 'వ్యవసాయం / రైతు కూలీ',
        'Housekeeping': 'ఇంటి సహాయకుడు / సేవకుడు',
        'Driving': 'డ్రైవర్',
        'Security': 'సెక్యూరిటీ గార్డు',
        'experience': 'సంవత్సరాల అనుభవం',
        'years': 'సంవత్సరాలు',
        'location': 'స్థలం',
        'skills': 'నైపుణ్యాలు',
        'bio': 'నా గురించి',
        'Mason': 'తాపీ మేస్త్రీ',
        'Plumber': 'ప్లंबर',
        'Electrician': 'ఎలక్ట్రీషియన్',
        'Helper': 'సహాయకుడు',
        'Farm Laborer': 'వ్యవసాయ కూలీ',
        'Housekeeper': 'ఇంటి పనిమనిషి',
        'Delivery Rider': 'డెలివరీ బాయ్',
        'Security Guard': 'సెక్యూరిటీ గార్డు',
    },
    'mr': {
        'Construction': 'बांधकाम कामगार / गवंडी',
        'Plumbing': 'नळ कारागीर (Plumber)',
        'Electrical': 'वीज मिस्त्री (Electrician)',
        'Agriculture': 'शेती / शेतमजूर',
        'Housekeeping': 'घरगुती कामगार',
        'Driving': 'चालक / ड्रायव्हर',
        'Security': 'सुरक्षा रक्षक',
        'experience': 'वर्षांचा अनुभव',
        'years': 'वर्षे',
        'location': 'ठिकाण',
        'skills': 'कौशल्ये',
        'bio': 'माझ्याबद्दल',
        'Mason': 'गवंडी',
        'Plumber': 'प्लंबर',
        'Electrician': 'इलेक्ट्रिशियन',
        'Helper': 'मदतनीस',
        'Farm Laborer': 'शेतमजूर',
        'Housekeeper': 'घरकामगार',
        'Delivery Rider': 'डिलिव्हरी बॉय',
        'Security Guard': 'सुरक्षा रक्षक',
    }
}

# Auto-translation logic
def translate_text(text: str, target_lang: str) -> str:
    if not text:
        return ""
    clean = text.strip()
    
    # Direct dictionary lookup
    lang_dict = TRANSLATIONS.get(target_lang)
    if lang_dict:
        if clean in lang_dict:
            return lang_dict[clean]
        
        # Check subwords
        for en_key, native_val in lang_dict.items():
            if clean.lower() == en_key.lower():
                return native_val
            if en_key.lower() in clean.lower():
                return native_val

    # Reverse lookup (translating Native to English)
    for lang, lang_dict in TRANSLATIONS.items():
        if lang == target_lang:
            continue
        for en_key, native_val in lang_dict.items():
            if clean == native_val or native_val in clean:
                return en_key
                
    return text

def get_connection():
    # SQLite connection with dictionary factory
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        phone TEXT,
        role TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS worker_profiles (
        user_id TEXT PRIMARY KEY,
        name TEXT,
        name_native TEXT,
        native_language TEXT,
        category TEXT,
        category_native TEXT,
        experience_years INTEGER,
        location TEXT,
        location_native TEXT,
        bio TEXT,
        bio_native TEXT,
        voice_greeting TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employer_profiles (
        user_id TEXT PRIMARY KEY,
        name TEXT,
        company TEXT,
        phone TEXT,
        location TEXT,
        description TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY,
        employer_id TEXT,
        employer_name TEXT,
        company_name TEXT,
        title TEXT,
        title_native TEXT,
        category TEXT,
        location TEXT,
        location_native TEXT,
        salary TEXT,
        salary_native TEXT,
        description TEXT,
        description_native TEXT,
        posted_date TEXT,
        languages TEXT,
        FOREIGN KEY(employer_id) REFERENCES users(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id TEXT PRIMARY KEY,
        job_id TEXT,
        worker_id TEXT,
        applied_date TEXT,
        status TEXT,
        FOREIGN KEY(job_id) REFERENCES jobs(id),
        FOREIGN KEY(worker_id) REFERENCES users(id)
    )
    """)
    
    conn.commit()
    
    # Seed Job Openings if none exist
    cursor.execute("SELECT COUNT(*) FROM jobs")
    if cursor.fetchone()[0] == 0:
        seed_jobs = [
            ('job-1', 'emp-1', 'Rajesh Mehta', 'Mehta Infrastructure Ltd.', 'Experienced Mason', 'अनुभवी राजमिस्त्री', 'Construction', 'Mumbai, MH', 'मुंबई, महाराष्ट्र', '₹18,000 - ₹24,000 / month', '₹18,000 - ₹24,000 / महीना', 'Looking for a skilled mason with 3+ years experience in bricklaying and plastering. Accommodation provided near site.', 'ईंट बिछाने और प्लास्टर करने में 3+ साल के अनुभव वाले कुशल राजमिस्त्री की तलाश है। साइट के पास रहने की जगह दी जाएगी।', '2026-06-18', 'hi,mr'),
            ('job-2', 'emp-2', 'Amit Roy', 'Green Valley Organic Farms', 'Farm Workers (Harvesting)', 'কৃষি শ্রমিক (ফসল কাটা)', 'Agriculture', 'Hooghly, WB', 'হুগলী, পশ্চিমবঙ্গ', '₹400 / day + Meals', '₹৪০০ / দিন + খাবার', 'Require 5 farm helpers for paddy harvesting season. Short term contract (30 days). Daily wages.', 'ধান কাটার মরসুমের জন্য ৫ জন কৃষি সহকারী প্রয়োজন। স্বল্পমেয়াদী চুক্তি (৩০ দিন)। দৈনিক মজুরি।', '2026-06-20', 'bn'),
            ('job-3', 'emp-3', 'Karthik Raja', 'Narayana Apartments Association', 'Residential Plumber', 'குடியிருப்பு பிளம்பர்', 'Plumbing', 'Chennai, TN', 'சென்னை, தமிழ்நாடு', '₹15,000 / month + Incentives', '₹15,000 / மாதம் + ஊக்கத்தொகை', 'Full time plumber needed for apartment maintenance. Should know water lines, pumps and pipe repair.', 'அபார்ட்மெண்ட் பராமரிப்புக்கு முழு நேர பிளம்பர் தேவை. தண்ணீர் லைன்கள், பம்புகள் மற்றும் குழாய் பழுதுபார்க்க தெரிந்திருக்க வேண்டும்.', '2026-06-19', 'ta'),
            ('job-4', 'emp-4', 'Venkata Rao', 'Rao Logistics', 'Commercial Truck Driver', 'కమర్షియల్ ట్రక్ డ్రైవర్', 'Driving', 'Vijayawada, AP', 'విజయవాడ, ఆంధ్రప్రదేశ్', '₹22,000 - ₹28,000 / month', '₹22,000 - ₹28,000 / నెల', 'Heavy vehicle driving license required. Experience in driving interstate. Accommodation provided.', 'హెవీ వెహికల్ డ్రైవింగ్ లైసెన్స్ అవసరం. అంతర్ రాష్ట్ర డ్రైవింగ్ లో అనుభవం. వసతి కల్పించబడుతుంది.', '2026-06-21', 'te'),
            ('job-5', 'emp-5', 'Sanjay Deshmukh', 'Apex Security Solutions', 'Industrial Security Guard', 'औद्योगिक सुरक्षा रक्षक', 'Security', 'Pune, MH', 'पुणे, महाराष्ट्र', '₹16,500 / month (12hr shift)', '₹१६,५०० / महिना (१२ तास शिफ्ट)', 'Requires physically fit guards for a factory. English or Hindi understanding is a plus. Uniform provided.', 'कारखान्यासाठी शारीरिकदृष्ट्या तंदुरुस्त रक्षकांची गरज आहे। युनिफॉर्म दिला जाईल।', '2026-06-21', 'mr,hi')
        ]
        
        cursor.executemany("""
        INSERT INTO jobs (
            id, employer_id, employer_name, company_name, title, title_native, 
            category, location, location_native, salary, salary_native, 
            description, description_native, posted_date, languages
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, seed_jobs)
        conn.commit()
        
    conn.close()

# Database CRUD Operations
def request_otp(phone: str) -> str:
    # Generates code and saves to environment or logs to mock it
    otp = str(random.randint(100000, 999999))
    # Save code to disk / session to verify
    with open(f"otp_{phone}.tmp", "w") as f:
        f.write(otp)
    return otp

def verify_otp(phone: str, otp: str, role: str) -> dict:
    # Code check
    otp_file = f"otp_{phone}.tmp"
    valid = False
    
    if os.path.exists(otp_file):
        with open(otp_file, "r") as f:
            saved_otp = f.read().strip()
        if saved_otp == otp or otp == "123456": # 123456 as bypass code
            valid = True
            os.remove(otp_file)
            
    if not valid and otp != "123456":
        raise Exception("Invalid verification code. Please try again.")
        
    # Get or create user
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE phone = ? AND role = ?", (phone, role))
    user = cursor.fetchone()
    
    if not user:
        user_id = f"user-{int(time.time() * 1000)}"
        cursor.execute("INSERT INTO users (id, phone, role) VALUES (?, ?, ?)", (user_id, phone, role))
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
    user_dict = dict(user)
    
    # Load profile details
    if role == 'worker':
        cursor.execute("SELECT * FROM worker_profiles WHERE user_id = ?", (user_dict['id'],))
        profile = cursor.fetchone()
        user_dict['workerProfile'] = dict(profile) if profile else None
    else:
        cursor.execute("SELECT * FROM employer_profiles WHERE user_id = ?", (user_dict['id'],))
        profile = cursor.fetchone()
        user_dict['employerProfile'] = dict(profile) if profile else None
        
    conn.close()
    return user_dict

def update_worker_profile(user_id: str, profile: dict) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT OR REPLACE INTO worker_profiles (
        user_id, name, name_native, native_language, category, category_native,
        experience_years, location, location_native, bio, bio_native, voice_greeting
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, profile['name'], profile['nameNative'], profile['nativeLanguage'],
        profile['category'], profile['categoryNative'], profile['experienceYears'],
        profile['location'], profile['locationNative'], profile['bio'], profile['bioNative'],
        profile.get('voiceGreetingUrl')
    ))
    conn.commit()
    
    # Reload user
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = dict(cursor.fetchone())
    cursor.execute("SELECT * FROM worker_profiles WHERE user_id = ?", (user_id,))
    user['workerProfile'] = dict(cursor.fetchone())
    conn.close()
    return user

def update_employer_profile(user_id: str, profile: dict) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT OR REPLACE INTO employer_profiles (
        user_id, name, company, phone, location, description
    ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id, profile['name'], profile['company'], profile['phone'],
        profile['location'], profile['description']
    ))
    conn.commit()
    
    # Reload user
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = dict(cursor.fetchone())
    cursor.execute("SELECT * FROM employer_profiles WHERE user_id = ?", (user_id,))
    user['employerProfile'] = dict(cursor.fetchone())
    conn.close()
    return user

def post_job(employer_id: str, job_data: dict) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    
    # Find recruiter company name
    cursor.execute("SELECT * FROM employer_profiles WHERE user_id = ?", (employer_id,))
    emp = cursor.fetchone()
    employer_name = emp['name'] if emp else "Employer"
    company_name = emp['company'] if emp else "Company Inc."
    
    job_id = f"job-{int(time.time() * 1000)}"
    posted_date = time.strftime("%Y-%m-%d")
    languages_str = ",".join(job_data['languages'])
    
    cursor.execute("""
    INSERT INTO jobs (
        id, employer_id, employer_name, company_name, title, title_native,
        category, location, location_native, salary, salary_native,
        description, description_native, posted_date, languages
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        job_id, employer_id, employer_name, company_name, job_data['title'], job_data['titleNative'],
        job_data['category'], job_data['location'], job_data['locationNative'], job_data['salary'],
        job_data['salaryNative'], job_data['description'], job_data['descriptionNative'], posted_date, languages_str
    ))
    conn.commit()
    conn.close()
    return {"id": job_id}

def get_all_jobs() -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs ORDER BY posted_date DESC")
    rows = cursor.fetchall()
    jobs = []
    for r in rows:
        job = dict(r)
        job['languages'] = r['languages'].split(',') if r['languages'] else []
        jobs.append(job)
    conn.close()
    return jobs

def apply_for_job(worker_id: str, job_id: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if duplicate exists
    cursor.execute("SELECT * FROM applications WHERE worker_id = ? AND job_id = ?", (worker_id, job_id))
    app = cursor.fetchone()
    
    if not app:
        app_id = f"app-{int(time.time() * 1000)}"
        applied_date = time.strftime("%Y-%m-%d")
        cursor.execute("""
        INSERT INTO applications (id, job_id, worker_id, applied_date, status)
        VALUES (?, ?, ?, ?, ?)
        """, (app_id, job_id, worker_id, applied_date, "pending"))
        conn.commit()
        app_dict = {"id": app_id, "jobId": job_id, "workerId": worker_id, "appliedDate": applied_date, "status": "pending"}
    else:
        app_dict = dict(app)
        
    conn.close()
    return app_dict

def get_applications_for_worker(worker_id: str) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT a.*, j.title, j.title_native, j.company_name 
    FROM applications a 
    JOIN jobs j ON a.job_id = j.id
    WHERE a.worker_id = ?
    """, (worker_id,))
    rows = cursor.fetchall()
    apps = [dict(r) for r in rows]
    conn.close()
    return apps

def get_job_applications_for_employer(employer_id: str) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT a.*, j.title as job_title, j.title_native as job_title_native, 
           w.name as worker_name, w.name_native as worker_name_native, w.location as worker_location,
           w.location_native as worker_location_native, w.bio as worker_bio, w.bio_native as worker_bio_native,
           w.category as worker_category, w.category_native as worker_category_native, w.experience_years as worker_exp,
           u.phone as worker_phone
    FROM applications a
    JOIN jobs j ON a.job_id = j.id
    JOIN worker_profiles w ON a.worker_id = w.user_id
    JOIN users u ON w.user_id = u.id
    WHERE j.employer_id = ?
    """, (employer_id,))
    rows = cursor.fetchall()
    apps = [dict(r) for r in rows]
    conn.close()
    return apps

def get_all_workers() -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT w.*, u.phone 
    FROM worker_profiles w
    JOIN users u ON w.user_id = u.id
    """)
    rows = cursor.fetchall()
    workers = [dict(r) for r in rows]
    conn.close()
    return workers
