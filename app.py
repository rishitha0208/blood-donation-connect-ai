import streamlit as st
import pandas as pd
import datetime
import io
import os
from PIL import Image, ImageDraw, ImageFont

# Import backend modules
import database as db
import ai_assistant as ai

# Set page configuration
st.set_page_config(
    page_title="RaktDaan Connect AI 🩸🇮🇳",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
db.init_db()

# Load Custom CSS styling
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# Initialize session state for navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home"

# Function to change pages from CTAs
def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# ----------------- SIDEBAR NAVIGATION -----------------
st.sidebar.markdown(
    "<div style='text-align: center; margin-bottom: 20px;'>"
    "<span style='font-size: 3.5rem;'>🩸</span>"
    "<h2 style='margin-top: 10px; color: #e74c3c; font-weight: 800;'>RaktDaan Connect</h2>"
    "<p style='font-size: 0.85rem; color: #a0a0a0;'>India's Smart Blood Network</p>"
    "</div>",
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

# Navigation buttons
pages = [
    "🏠 Home",
    "➕ Register as Donor",
    "🔍 Search Blood Donors",
    "🚨 Emergency Request",
    "🤖 AI Assistant Agent",
    "📊 Impact Dashboard"
]

for p in pages:
    if st.sidebar.button(
        p, 
        key=f"nav_{p}", 
        use_container_width=True, 
        type="primary" if st.session_state.current_page == p else "secondary"
    ):
        st.session_state.current_page = p
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='font-size: 0.8rem; color: #888888; text-align: center;'>"
    "LifeConnect AI © 2026<br>Secure & Local persistence<br>No AI API keys needed"
    "</div>",
    unsafe_allow_html=True
)

# Load layout components based on active page
current_page = st.session_state.current_page

# ----------------- 1. HOME PAGE -----------------
if current_page == "🏠 Home":
    # Hero Section
    st.markdown(
        "<div style='background: linear-gradient(135deg, #1e272e 0%, #0f0c20 100%); padding: 40px; border-radius: 20px; border: 1px solid rgba(255, 153, 51, 0.3); margin-bottom: 30px; text-align: center;'>"
        "<h1 style='color: #ffffff; font-weight: 800; font-size: 3.2rem; margin-bottom: 10px;'>RaktDaan Connect <span style='color: #ff9933;'>AI</span> 🩸</h1>"
        "<h4 style='color: #2ecc71; margin-top: 0; font-weight: 600; font-style: italic; letter-spacing: 1px;'>\"Raktdaan Mahadaan - Pledging Lives, Connecting Hope\"</h4>"
        "<p style='color: #d1d1d1; font-size: 1.15rem; font-weight: 400; max-width: 800px; margin: 15px auto 25px auto;'>"
        "India's intelligent emergency blood donation and coordination network. Instantly match patient cases with compatible local donors, verify criteria under NBTC guidelines, and coordinate real-time dispatch routes."
        "</p>"
        "</div>",
        unsafe_allow_html=True
    )
    
    # Quick action metrics row
    stats = db.get_dashboard_stats()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val">{stats['total_donors']}</div>
            <div class="metric-lbl">Registered Donors</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val">{stats['available_donors']}</div>
            <div class="metric-lbl">Available Now</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val" style="color: #f1c40f;">{stats['active_emergencies']}</div>
            <div class="metric-lbl">Active Emergencies</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val" style="color: #2ecc71;">{stats['resolved_emergencies']}</div>
            <div class="metric-lbl">Cases Resolved</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # CTA columns
    cta_col1, cta_col2 = st.columns(2)
    with cta_col1:
        st.markdown(
            "<div style='background: rgba(255,255,255,0.03); padding: 30px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.05); height: 100%;'>"
            "<h3 style='color: #e74c3c; margin-top: 0;'>🚨 Emergency Blood Request</h3>"
            "<p style='color: #bfbfbf; font-size: 0.95rem; margin-bottom: 20px; min-height: 50px;'>"
            "Need blood urgently? Submit a patient emergency file. The system will immediately compute compatible local blood matching groups and simulate real-time routing distances."
            "</p>"
            "</div>",
            unsafe_allow_html=True
        )
        if st.button("File Emergency Request Now", type="primary", use_container_width=True):
            navigate_to("🚨 Emergency Request")
            
    with cta_col2:
        st.markdown(
            "<div style='background: rgba(255,255,255,0.03); padding: 30px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.05); height: 100%;'>"
            "<h3 style='color: #2ecc71; margin-top: 0;'>➕ Become a Blood Donor</h3>"
            "<p style='color: #bfbfbf; font-size: 0.95rem; margin-bottom: 20px; min-height: 50px;'>"
            "Your single donation can save up to 3 lives. Register your profile, configure your availability, and earn rank badges as you commit to lifesaving acts."
            "</p>"
            "</div>",
            unsafe_allow_html=True
        )
        if st.button("Register as a Donor Now", use_container_width=True):
            navigate_to("➕ Register as Donor")
            
    # Live Emergencies Section
    st.markdown("<br><h3 class='section-title'>Active Emergency Alerts</h3>", unsafe_allow_html=True)
    emergencies_df = db.get_emergencies_df()
    active_emergencies = emergencies_df[emergencies_df['status'] == 'Pending']
    
    if active_emergencies.empty:
        st.info("No active emergencies currently. The community is well-supported!")
    else:
        for idx, row in active_emergencies.head(3).iterrows():
            urgency_color = "#e74c3c" if row['urgency'] == 'High' else ("#f1c40f" if row['urgency'] == 'Medium' else "#3498DB")
            st.markdown(
                f"<div style='background: rgba(231, 76, 60, 0.08); border-left: 5px solid {urgency_color}; padding: 15px; border-radius: 8px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;'>"
                f"<div>"
                f"<strong style='font-size: 1.1rem; color: #ffffff;'>Blood Required: {row['blood_group']}</strong> (Urgency: <span style='color: {urgency_color}; font-weight: bold;'>{row['urgency']}</span>)<br>"
                f"<span style='font-size: 0.85rem; color: #a0a0a0;'>Patient: {row['patient_name']} | Hospital: {row['hospital']} in {row['city']}</span>"
                f"</div>"
                f"<span style='font-size: 0.8rem; color: #888; text-align: right;'>Reported: {row['created_at']}</span>"
                f"</div>",
                unsafe_allow_html=True
            )
            
# ----------------- 2. DONOR REGISTRATION -----------------
elif current_page == "➕ Register as Donor":
    st.markdown("<h2 class='section-title'>Become a Registered Donor</h2>", unsafe_allow_html=True)
    st.write("Complete the form below to register yourself in the local SQLite directory. Your contact details will only be visible for verified compatibility search queries.")
    
    reg_col1, reg_col2 = st.columns([2, 1])
    
    with reg_col1:
        with st.form("donor_registration_form"):
            name = st.text_input("Full Name *", placeholder="Enter your full name")
            age = st.number_input("Age *", min_value=1, max_value=120, value=25)
            blood_group = st.selectbox("Blood Group *", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
            phone = st.text_input("Phone Number *", placeholder="e.g. +91 98765 43210")
            city = st.selectbox("City *", ["Mumbai", "Delhi NCR", "Bangalore", "Kolkata", "Chennai", "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Chandigarh", "Kochi", "Other"])
            if city == "Other":
                city = st.text_input("Specify City Name *", placeholder="Enter city name")
            
            abha_id = st.text_input("ABHA ID (Ayushman Bharat Health Account)", placeholder="e.g. 91-1234-5678-9012 (Optional)")
            
            never_donated = st.checkbox("I have never donated blood before")
            if never_donated:
                last_donation_date = None
            else:
                last_donation_date = st.date_input("Last Donation Date", value=datetime.date.today() - datetime.timedelta(days=100))
                
            donation_count = st.number_input("Total Past Donations (to initialize Badge Level)", min_value=0, max_value=100, value=1 if not never_donated else 0)
            availability = st.selectbox("Available for Emergencies Now?", ["Yes", "No"])
            
            submit_reg = st.form_submit_button("Submit Registration Profile", type="primary")
            
            if submit_reg:
                import re
                phone_clean = phone.strip()
                is_phone_valid = re.match(r'^(?:\+91[\s-]?)?[6-9]\d{9}$', phone_clean) or re.match(r'^\d{10}$', phone_clean)
                
                abha_clean = abha_id.strip()
                is_abha_valid = not abha_clean or re.match(r'^\d{2}-\d{4}-\d{4}-\d{4}$', abha_clean)
                
                # Validation rules
                if not name.strip():
                    st.error("Name field is required.")
                elif not phone.strip():
                    st.error("Phone number is required.")
                elif not is_phone_valid:
                    st.error("Please enter a valid 10-digit Indian phone number (optionally prefixed with +91).")
                elif not is_abha_valid:
                    st.error("Please enter a valid 14-digit ABHA ID in the format: 91-XXXX-XXXX-XXXX.")
                elif age < 18 or age > 65:
                    st.error("Eligibility Warning: Age must be between 18 and 65 to register as a donor.")
                else:
                    avail_val = 1 if availability == "Yes" else 0
                    date_str = last_donation_date.strftime("%Y-%m-%d") if last_donation_date else None
                    
                    # Call database registration
                    donor_id = db.register_donor(name, age, blood_group, phone, city, date_str, avail_val, donation_count, abha_id=abha_clean if abha_clean else None)
                    
                    st.success(f"Donor profile for '{name}' successfully submitted/updated in SQLite database! (Donor ID: RDC-{donor_id:04d})")
                    
                    # Store ID for card generator
                    st.session_state.last_registered_donor = {
                        "id": donor_id,
                        "name": name,
                        "blood_group": blood_group,
                        "phone": phone,
                        "city": city,
                        "donation_count": donation_count,
                        "abha_id": abha_clean if abha_clean else "Not Registered"
                    }
                    st.rerun()

    with reg_col2:
        st.markdown(
            "<div style='background: rgba(255, 255, 255, 0.02); padding: 20px; border-radius: 12px; border: 1px dashed rgba(255, 255, 255, 0.1);'>"
            "<h4>💡 Did you know?</h4>"
            "<ul style='font-size: 0.85rem; color: #b0b0b0; padding-left: 20px;'>"
            "<li><strong>O-</strong> is the universal donor group. O- blood is highly requested during emergencies because anyone can receive it.</li>"
            "<li><strong>AB+</strong> is the universal recipient, meaning patients with this blood type can safely receive blood from any group.</li>"
            "<li>A single donation of blood takes only about 8-10 minutes and can help up to three different individuals.</li>"
            "</ul>"
            "</div>",
            unsafe_allow_html=True
        )
        
        # Display Card Generator if registered
        if "last_registered_donor" in st.session_state:
            d_info = st.session_state.last_registered_donor
            st.markdown("### 🪪 Digital Donor Card")
            st.info("Your ABHA-Aligned Digital Donor Card is ready for download!")
            
            # Generate PIL Card
            badge_details = ai.get_donor_badge(d_info['donation_count'])
            
            # Card image creation
            card_w, card_h = 500, 300
            card = Image.new('RGB', (card_w, card_h), color='#0f172a') # Slate-900 background
            draw = ImageDraw.Draw(card)
            
            # Draw premium tricolor ribbons at top and bottom
            # Top Ribbon: Saffron, White, Green
            draw.rectangle([0, 0, card_w, 5], fill='#FF9933')
            draw.rectangle([0, 5, card_w, 10], fill='#FFFFFF')
            draw.rectangle([0, 10, card_w, 15], fill='#138808')
            
            # Bottom Ribbon: Saffron, White, Green
            draw.rectangle([0, card_h-15, card_w, card_h-10], fill='#FF9933')
            draw.rectangle([0, card_h-10, card_w, card_h-5], fill='#FFFFFF')
            draw.rectangle([0, card_h-5, card_w, card_h], fill='#138808')
            
            # Inner frame
            draw.rectangle([10, 22, card_w-10, card_h-22], outline='#FF9933', width=1)
            
            # Draw standard font details
            try:
                # Pillow >= 10.0 allows specifying size in load_default()
                font_title = ImageFont.load_default(size=18)
                font_subtitle = ImageFont.load_default(size=13)
                font_body = ImageFont.load_default(size=12)
                font_bg = ImageFont.load_default(size=36)
            except TypeError:
                # Fallback if older Pillow version
                font_title = ImageFont.load_default()
                font_subtitle = ImageFont.load_default()
                font_body = ImageFont.load_default()
                font_bg = ImageFont.load_default()
            
            # Text outputs
            draw.text((30, 35), "RAKTDAAN CONNECT AI", fill='#ffffff', font=font_title)
            draw.text((30, 58), "National Health Authority - ABHA Aligned", fill='#60a5fa', font=font_subtitle)
            
            # Details
            draw.text((30, 95), f"ABHA ID: {d_info.get('abha_id', 'Not Registered')}", fill='#10b981', font=font_subtitle)
            draw.text((30, 125), f"DONOR ID: RDC-{d_info['id']:04d}", fill='#f59e0b', font=font_body)
            draw.text((30, 150), f"NAME: {d_info['name'].upper()}", fill='#ffffff', font=font_body)
            draw.text((30, 175), f"CITY: {d_info['city'].upper()}", fill='#cbd5e1', font=font_body)
            draw.text((30, 200), f"PHONE: {d_info['phone']}", fill='#cbd5e1', font=font_body)
            draw.text((30, 225), f"RANK: {badge_details['emoji']} {badge_details['title']}", fill='#f1c40f', font=font_body)
            draw.text((30, 248), "STATUS: VERIFIED DONOR", fill='#10b981', font=font_body)
            
            # Blood group stamp on right side
            draw.rectangle([340, 95, 460, 205], fill='#ef4444', outline='#ffffff', width=1) # Blood Group box
            draw.text((362, 105), "BLOOD GP", fill='#ffffff', font=font_subtitle)
            draw.text((375, 130), d_info['blood_group'], fill='#ffffff', font=font_bg)
            
            # Draw mock QR Code box
            qr_x, qr_y, qr_size = 405, 215, 45
            draw.rectangle([qr_x, qr_y, qr_x + qr_size, qr_y + qr_size], fill='#ffffff')
            # Draw some mock QR patterns inside
            for i in range(0, qr_size, 5):
                for j in range(0, qr_size, 5):
                    if (i * j + d_info['id']) % 3 == 0:
                        draw.rectangle([qr_x + i, qr_y + j, qr_x + i + 4, qr_y + j + 4], fill='#000000')
            
            # Convert to PNG bytes
            img_byte_arr = io.BytesIO()
            card.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Display image
            st.image(img_byte_arr, caption=f"Digital Card Preview for {d_info['name']}")
            
            st.download_button(
                label="📥 Download Donor Card (PNG)",
                data=img_byte_arr,
                file_name=f"RDC_donor_card_{d_info['id']}.png",
                mime="image/png",
                use_container_width=True
            )

# ----------------- 3. SEARCH BLOOD DONORS -----------------
elif current_page == "🔍 Search Blood Donors":
    st.markdown("<h2 class='section-title'>Search Local Blood Directory</h2>", unsafe_allow_html=True)
    st.write("Query the SQLite active donor base by specifying the blood type and city required.")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        s_group = st.selectbox("Required Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    with col_s2:
        # Load unique cities from database or default options
        all_donors = db.get_all_donors_df()
        cities = list(all_donors['city'].unique()) if not all_donors.empty else ["Mumbai", "Delhi NCR", "Bangalore", "Kolkata", "Chennai", "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Chandigarh", "Kochi"]
        s_city = st.selectbox("City", sorted(cities))
        
    search_clicked = st.button("Search Active Donors", type="primary", use_container_width=True)
    
    if search_clicked or "last_search" in st.session_state:
        # Save query in session state to persist on actions
        st.session_state.last_search = (s_group, s_city)
        
        matches = db.search_donors(s_group, s_city)
        
        st.markdown(f"### Results for **{s_group}** in **{s_city}**")
        
        if not matches:
            st.warning(f"No exact matches found for {s_group} donors in {s_city}.")
            
            # AI Compatibility Suggestions
            st.markdown("#### 🤖 Rule-Based AI Suggestions")
            alternatives = ai.find_alternative_blood_groups(s_group)
            
            if alternatives:
                st.info(
                    f"An exact blood type match is unavailable. However, medically, a recipient of blood group **{s_group}** "
                    f"can safely receive blood from these compatible groups: **{', '.join(alternatives)}**."
                )
                
                # Dynamic buttons to search for alternatives
                st.write("Quick-search compatible blood groups in this city:")
                alt_cols = st.columns(len(alternatives))
                for idx, alt_g in enumerate(alternatives):
                    with alt_cols[idx]:
                        if st.button(f"Search {alt_g}", key=f"alt_btn_{alt_g}"):
                            st.session_state.last_search = (alt_g, s_city)
                            st.rerun()
            else:
                st.error("No compatibility alternatives resolved.")
                
        else:
            st.success(f"Found {len(matches)} matching donor(s) available in your city!")
            
            # Export to CSV option
            match_df = pd.DataFrame(matches)
            # Reorder clean columns for display
            clean_df = match_df[['name', 'age', 'blood_group', 'phone', 'city', 'last_donation_date', 'donation_count']]
            
            csv_bytes = clean_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Matching Donors List as CSV",
                data=csv_bytes,
                file_name=f"BDC_Donors_{s_group}_{s_city}.csv",
                mime="text/csv"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            # Display Cards
            for m in matches:
                badge = ai.get_donor_badge(m['donation_count'])
                avail_status = "<span class='avail-tag-yes'>Available Now</span>" if m['availability'] == 1 else "<span class='avail-tag-no'>On Hold</span>"
                abha_display = f" | 💳 ABHA ID: <code>{m['abha_id']}</code>" if m.get('abha_id') else " | 💳 ABHA ID: <code>Not Registered</code>"
                
                st.markdown(
                    f"<div class='donor-card'>"
                    f"  <div class='donor-header'>"
                    f"    <strong style='font-size: 1.25rem; color:#ffffff;'>{m['name']} (Age: {m['age']})</strong>"
                    f"    <span class='blood-tag'>{m['blood_group']}</span>"
                    f"  </div>"
                    f"  <div class='donor-details'>"
                    f"    📞 Phone: <code>{m['phone']}</code> | 📍 City: {m['city']}{abha_display}<br>"
                    f"    📅 Last Donated: {m['last_donation_date'] if m['last_donation_date'] else 'Never'}<br>"
                    f"    🏆 Rank: <span style='color:{badge['color']}; font-weight:bold;'>{badge['emoji']} {badge['title']}</span> ({m['donation_count']} donations)<br>"
                    f"    💡 Availability: {avail_status}"
                    f"  </div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

# ----------------- 4. EMERGENCY REQUEST -----------------
elif current_page == "🚨 Emergency Request":
    st.markdown("<h2 class='section-title'>Emergency Blood Request Portal</h2>", unsafe_allow_html=True)
    st.write("File an emergency case file immediately. The matching engine computes routing ETAs and alerts potential active donors.")
    
    tab_e1, tab_e2 = st.tabs(["🆕 File Request", "📋 Active Requests & Matches"])
    
    with tab_e1:
        with st.form("emergency_request_form"):
            e_name = st.text_input("Patient Full Name *", placeholder="Enter patient's name")
            e_group = st.selectbox("Required Blood Group *", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
            e_hospital = st.text_input("Hospital Name & Branch *", placeholder="e.g. Apollo Hospital, Main St")
            e_city = st.selectbox("Hospital City *", ["Mumbai", "Delhi NCR", "Bangalore", "Kolkata", "Chennai", "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Chandigarh", "Kochi"])
            e_urgency = st.select_slider("Urgency Severity Level *", options=["Low", "Medium", "High"], value="High")
            
            submit_err = st.form_submit_button("Broadcast Emergency Alert", type="primary")
            
            if submit_err:
                if not e_name.strip() or not e_hospital.strip():
                    st.error("Please fill in all required (*) fields.")
                else:
                    db.create_emergency_request(e_name, e_group, e_hospital, e_city, e_urgency)
                    st.success(f"Emergency alert filed successfully for patient **{e_name}** ({e_group}) at **{e_hospital}**, **{e_city}**!")
                    
                    # Store variables for immediate redirection view
                    st.session_state.selected_emergency_group = e_group
                    st.session_state.selected_emergency_city = e_city
                    st.session_state.selected_emergency_hospital = e_hospital
                    
                    # Switch tabs using helper
                    # In streamlit tabs can't be set programmatically easily, but we can display the results directly below!
                    st.markdown("---")
                    st.subheader("🔍 Immediate Match Result")
                    
    with tab_e2:
        emergencies = db.get_emergencies_df()
        pending_emergencies = emergencies[emergencies['status'] == 'Pending']
        
        if pending_emergencies.empty:
            st.info("No active emergency requests in the system. Everything is resolved!")
        else:
            for idx, r in pending_emergencies.iterrows():
                st.markdown(
                    f"<div style='border: 1px solid rgba(231, 76, 60, 0.4); background: rgba(231,76,60,0.03); padding: 18px; border-radius: 10px; margin-bottom: 15px;'>"
                    f"  <div style='display:flex; justify-content:space-between; align-items:center;'>"
                    f"    <h4 style='margin:0; color:#ffffff;'>Patient: {r['patient_name']} ({r['blood_group']})</h4>"
                    f"    <span style='background:#e74c3c; color:white; padding:3px 10px; border-radius:10px; font-size:0.8rem; font-weight:bold;'>Urgency: {r['urgency']}</span>"
                    f"  </div>"
                    f"  <p style='margin: 8px 0; font-size:0.9rem; color:#d1d1d1;'>"
                    f"    📍 Hospital: <strong>{r['hospital']}, {r['city']}</strong> | Filed at: {r['created_at']}"
                    f"  </p>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                
                # Fetch matching and compatible donors
                compat_groups = ai.get_compatible_groups(r['blood_group'])
                
                all_d = db.get_all_donors_df()
                if not all_d.empty:
                    # Filter active compatible donors in the same city
                    city_donors = all_d[(all_d['city'].str.lower() == r['city'].lower()) & (all_d['availability'] == 1)]
                    city_donors = city_donors[city_donors['blood_group'].isin(compat_groups)]
                else:
                    city_donors = pd.DataFrame()
                
                # Display matches with routing
                st.markdown("**Nearest Available Donors (Sorted by simulated Proximity ETA):**")
                
                if city_donors.empty:
                    st.warning("⚠️ No active compatible donors found in the immediate city. Try expanding the search manually or contact regional blood banks.")
                else:
                    donor_list_with_routing = []
                    for d_idx, d_row in city_donors.iterrows():
                        dist, eta = ai.simulate_proximity_and_eta(d_row['name'], d_row['city'], r['hospital'], r['city'])
                        donor_list_with_routing.append({
                            **dict(d_row),
                            "distance": dist,
                            "eta": eta
                        })
                    
                    # Sort closest first
                    donor_list_with_routing = sorted(donor_list_with_routing, key=lambda x: x['eta'])
                    
                    # Render donor rows
                    for item in donor_list_with_routing:
                        is_exact = item['blood_group'] == r['blood_group']
                        match_badge = "<span style='background:#2ecc71; color:white; padding:2px 8px; border-radius:8px; font-size:0.75rem; font-weight:bold;'>Exact Match</span>" if is_exact else "<span style='background:#f1c40f; color:black; padding:2px 8px; border-radius:8px; font-size:0.75rem; font-weight:bold;'>Compatible Match</span>"
                        
                        col_m1, col_m2 = st.columns([3, 1])
                        with col_m1:
                            st.markdown(
                                f"<div style='background:rgba(255,255,255,0.03); padding:12px; border-radius:6px; border-left:4px solid #3498db; margin-bottom:8px;'>"
                                f"  <strong>{item['name']}</strong> ({item['blood_group']}) {match_badge}<br>"
                                f"  📱 Phone: <code>{item['phone']}</code> | Proximity: <strong>{item['distance']} km</strong> | Est. Arrival: <strong style='color:#e74c3c;'>{item['eta']} mins</strong>"
                                f"</div>",
                                unsafe_allow_html=True
                            )
                        with col_m2:
                            # Contact / Pledge simulator
                            if st.button("Contact & Pledge", key=f"pledge_{r['id']}_{item['id']}", use_container_width=True):
                                st.balloons()
                                # Simulate dispatching emergency response
                                st.success(f"Success! Dispatch message simulated to {item['name']}. Donor has accepted the request. Simulating routing tracker details!")
                                
                # Action button to resolve request
                if st.button("Mark Case Resolved ✓", key=f"resolve_{r['id']}", type="secondary"):
                    db.resolve_emergency(r['id'])
                    st.success("Emergency case marked as resolved. Thank you to the donor community!")
                    st.rerun()

# ----------------- 5. AI ASSISTANT AGENT -----------------
elif current_page == "🤖 AI Assistant Agent":
    st.markdown("<h2 class='section-title'>Rule-Based AI Assistant Agent</h2>", unsafe_allow_html=True)
    st.write("An intelligent, locally run assistant loaded with WHO and Red Cross guidelines. Get rapid guidance on blood compatibility, eligibility verification, and pre-donation checks.")
    
    ai_mode = st.radio("Select Assistant Module", ["🩸 Blood Group Compatibility", "📋 Smart Eligibility Quiz", "🚨 Emergency Response Steps", "🛡️ Donation Safety Tips"], horizontal=True)
    
    if ai_mode == "🩸 Blood Group Compatibility":
        st.subheader("Blood Group Compatibility Matrix")
        st.write("Select a blood group to inspect who can receive from this donor, or who this patient can receive from.")
        
        c_group = st.selectbox("Choose Blood Group to Analyze", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        
        can_receive_from = ai.get_compatible_groups(c_group)
        can_give_to = ai.get_recipients_for_donor(c_group)
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown(
                f"<div style='background:rgba(46, 204, 113, 0.1); border:1px solid #2ecc71; padding:20px; border-radius:12px; min-height:220px;'>"
                f"  <h4 style='color:#2ecc71; margin-top:0;'>📥 Can Receive From (Compatible Donors)</h4>"
                f"  <p style='font-size:1.1rem; font-weight:bold;'>{c_group} patients can receive blood from:</p>"
                f"  <div style='display:flex; gap:8px; flex-wrap:wrap; margin-top:15px;'>"
                + "".join([f"<span class='blood-tag' style='background:#2ecc71;'>{g}</span>" for g in can_receive_from]) +
                f"  </div>"
                f"  <p style='font-size:0.85rem; color:#a0a0a0; margin-top:20px;'>"
                f"    {'Universal Recipient Alert: AB+ can receive blood from any blood group.' if c_group == 'AB+' else 'O- is the universal backup matching type.'}"
                f"  </p>"
                f"</div>",
                unsafe_allow_html=True
            )
            
        with col_c2:
            st.markdown(
                f"<div style='background:rgba(231, 76, 60, 0.1); border:1px solid #e74c3c; padding:20px; border-radius:12px; min-height:220px;'>"
                f"  <h4 style='color:#e74c3c; margin-top:0;'>📤 Can Give To (Compatible Patients)</h4>"
                f"  <p style='font-size:1.1rem; font-weight:bold;'>{c_group} donors can donate blood to:</p>"
                f"  <div style='display:flex; gap:8px; flex-wrap:wrap; margin-top:15px;'>"
                + "".join([f"<span class='blood-tag' style='background:#e74c3c;'>{g}</span>" for g in can_give_to]) +
                f"  </div>"
                f"  <p style='font-size:0.85rem; color:#a0a0a0; margin-top:20px;'>"
                f"    {'Universal Donor Alert: O- can donate blood to all recipients during emergencies.' if c_group == 'O-' else 'Can safely be processed by compatible blood centers.'}"
                f"  </p>"
                f"</div>",
                unsafe_allow_html=True
            )
            
    elif ai_mode == "📋 Smart Eligibility Quiz":
        st.subheader("Smart Donor Eligibility Evaluation")
        st.write("Answer these quick medical pre-screening check questions to assess your eligibility to donate blood based on NBTC (National Blood Transfusion Council) guidelines in India.")
        
        quiz_col1, quiz_col2 = st.columns([2, 1])
        
        with quiz_col1:
            q_age = st.number_input("What is your age?", min_value=1, max_value=120, value=25)
            q_weight = st.number_input("What is your weight (in kg)?", min_value=10, max_value=250, value=65)
            q_hemoglobin = st.slider("What is your Hemoglobin level (in g/dL)?", min_value=8.0, max_value=18.0, value=13.0, step=0.1)
            q_gender = st.selectbox("What is your gender?", ["Male", "Female"])
            
            q_ever_donated = st.selectbox("Have you donated blood before?", ["Yes", "No"])
            if q_ever_donated == "Yes":
                q_days = st.number_input("How many days ago was your last donation?", min_value=1, max_value=1000, value=120)
            else:
                q_days = None
                
            q_symptoms = st.selectbox("Do you currently experience any cold, flu, sore throat or active infection?", ["No", "Yes"])
            q_travel = st.selectbox("Have you travelled to any malaria-endemic zones in the last 12 months?", ["No", "Yes"])
            q_tattoo = st.selectbox("Have you received a tattoo, body piercing, or undergone a major surgery in the last 6 months?", ["No", "Yes"])
            
            trigger_quiz = st.button("Evaluate Eligibility Profile", type="primary", use_container_width=True)
            
        with quiz_col2:
            if trigger_quiz:
                symptoms_val = q_symptoms == "Yes"
                travel_val = q_travel == "Yes"
                tattoo_val = q_tattoo == "Yes"
                
                is_eligible, reasons = ai.check_eligibility(
                    q_age, q_weight, q_gender, q_days, symptoms_val, travel_val, tattoo_val, hemoglobin=q_hemoglobin
                )
                
                st.markdown("### 🧬 NBTC Eligibility Verdict")
                if is_eligible:
                    st.success("✅ **ELIGIBLE TO DONATE!**\nYou meet all standard medical criteria for blood donation. Thank you for your commitment to saving lives!")
                    st.info("💡 **Pre-donation tip:** Ensure you stay hydrated and consume a nutritious, low-fat meal before arriving at the donation center.")
                else:
                    st.error("❌ **TEMPORARILY DEFERRED**\nBased on your responses, you are currently deferred from donating due to the following criteria:")
                    for r in reasons:
                        st.markdown(f"- {r}")
                    st.warning("⚠️ *Note: These are standard guidelines. Please consult a qualified medical professional at the donation camp for a definitive evaluation.*")
            else:
                st.info("Complete the quiz on the left and click **Evaluate Eligibility Profile** to see the system analysis output.")
                
    elif ai_mode == "🚨 Emergency Response Steps":
        st.subheader("Emergency Coordination Steps")
        st.write("Are you waiting for blood to arrive at a hospital? Follow these checklist protocols recommended by blood bank coordinators:")
        
        guidelines = ai.get_emergency_guidance()
        for idx, g in enumerate(guidelines):
            st.markdown(f"**Step {idx+1}:** {g}")
            
    elif ai_mode == "🛡️ Donation Safety Tips":
        st.subheader("Blood Donation Safety Protocols")
        tips = ai.get_safety_tips()
        
        tab_t1, tab_t2, tab_t3 = st.tabs(["🍎 Pre-Donation (Before)", "🛋️ During Donation", "🥤 Post-Donation (After)"])
        
        with tab_t1:
            st.write("Ensure your body is prepared to donate blood safely:")
            for item in tips['pre']:
                st.markdown(f"- {item}")
        with tab_t2:
            st.write("Maintain maximum safety during the drawing process:")
            for item in tips['during']:
                st.markdown(f"- {item}")
        with tab_t3:
            st.write("Maximize recovery and hydration post-donation:")
            for item in tips['post']:
                st.markdown(f"- {item}")

# ----------------- 6. IMPACT DASHBOARD -----------------
elif current_page == "📊 Impact Dashboard":
    st.markdown("<h2 class='section-title'>System Impact & Metrics Dashboard</h2>", unsafe_allow_html=True)
    
    stats = db.get_dashboard_stats()
    
    # Render indicators
    d_col1, d_col2, d_col3, d_col4 = st.columns(4)
    with d_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val">{stats['total_donors']}</div>
            <div class="metric-lbl">Total Registered</div>
        </div>
        """, unsafe_allow_html=True)
    with d_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val">{stats['available_donors']}</div>
            <div class="metric-lbl">Active Available</div>
        </div>
        """, unsafe_allow_html=True)
    with d_col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val" style="color: #f1c40f;">{stats['active_emergencies']}</div>
            <div class="metric-lbl">Open Emergencies</div>
        </div>
        """, unsafe_allow_html=True)
    with d_col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val" style="color: #2ecc71;">{stats['resolved_emergencies']}</div>
            <div class="metric-lbl">Resolved Cases</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    dash_col1, dash_col2 = st.columns(2)
    
    all_donors = db.get_all_donors_df()
    
    with dash_col1:
        st.subheader("Blood Group Distribution")
        if all_donors.empty:
            st.write("No data available.")
        else:
            group_counts = all_donors['blood_group'].value_counts()
            # Streamlit bar chart
            st.bar_chart(group_counts, color="#e74c3c")
            
    with dash_col2:
        st.subheader("Donor Availability Ratio")
        if all_donors.empty:
            st.write("No data available.")
        else:
            avail_counts = all_donors['availability'].value_counts()
            # Rename for display
            avail_counts.index = ['Available Now' if x == 1 else 'On Hold' for x in avail_counts.index]
            st.bar_chart(avail_counts, color="#2ecc71")
            
    st.markdown("---")
    
    # Leaderboard & Gamification
    st.subheader("🏆 Lifesaver Leaderboard (Gamification)")
    st.write("Connecting the community's champions. Donors receive badges for the frequency of their donations.")
    
    if all_donors.empty:
        st.write("No donors registered yet.")
    else:
        # Sort donors by donation count
        leaderboard = all_donors.sort_values(by="donation_count", ascending=False).head(5)
        
        rank = 1
        for idx, row in leaderboard.iterrows():
            badge = ai.get_donor_badge(row['donation_count'])
            st.markdown(
                f"<div class='leaderboard-row'>"
                f"  <div style='display:flex; align-items:center; gap:15px;'>"
                f"    <span style='font-size:1.5rem; font-weight:bold; color:#f1c40f;'>#{rank}</span>"
                f"    <div>"
                f"      <strong style='color:#ffffff; font-size:1.1rem;'>{row['name']}</strong>"
                f"      <span style='color:#a0a0a0; font-size:0.85rem;'> ({row['city']})</span>"
                f"    </div>"
                f"  </div>"
                f"  <div style='text-align:right;'>"
                f"    <span class='blood-tag' style='background:{badge['color']};'>{badge['emoji']} {badge['title']}</span>"
                f"    <div style='font-size:0.8rem; color:#d1d1d1; margin-top:4px;'>Donations: <strong>{row['donation_count']}</strong></div>"
                f"  </div>"
                f"</div>",
                unsafe_allow_html=True
            )
            rank += 1
