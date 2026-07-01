import hashlib

# Blood compatibility matrices
COMPATIBILITY_RECEIVE = {
    "O-": ["O-"],
    "O+": ["O-", "O+"],
    "A-": ["O-", "A-"],
    "A+": ["O-", "O+", "A-", "A+"],
    "B-": ["O-", "B-"],
    "B+": ["O-", "O+", "B-", "B+"],
    "AB-": ["O-", "A-", "B-", "AB-"],
    "AB+": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]
}

COMPATIBILITY_GIVE = {
    "O-": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
    "O+": ["O+", "A+", "B+", "AB+"],
    "A-": ["A-", "A+", "AB-", "AB+"],
    "A+": ["A+", "AB+"],
    "B-": ["B-", "B+", "AB-", "AB+"],
    "B+": ["B+", "AB+"],
    "AB-": ["AB-", "AB+"],
    "AB+": ["AB+"]
}

def get_compatible_groups(recipient_group):
    """Returns compatible donor blood groups for a given recipient blood group."""
    return COMPATIBILITY_RECEIVE.get(recipient_group, [])

def get_recipients_for_donor(donor_group):
    """Returns blood groups that can receive blood from a given donor group."""
    return COMPATIBILITY_GIVE.get(donor_group, [])

def find_alternative_blood_groups(desired_group):
    """Suggests alternative compatible blood types in order of preference (excluding exact match)."""
    compatibles = get_compatible_groups(desired_group).copy()
    if desired_group in compatibles:
        compatibles.remove(desired_group)
    # Return reversed list so O- (universal) or closest is listed with correct context
    return list(reversed(compatibles))

def check_eligibility(age, weight, gender, days_since_last, symptoms, travel, tattoo_surgery, hemoglobin=13.0):
    """
    Evaluates donation eligibility based on NBTC and Indian guidelines.
    Returns: (is_eligible, reasons_list)
    """
    is_eligible = True
    reasons = []
    
    if age < 18 or age > 65:
        is_eligible = False
        reasons.append("Donor age must be between 18 and 65 years.")
        
    if weight < 45:
        is_eligible = False
        reasons.append("Donor weight must be at least 45 kg (NBTC Guideline).")
        
    if hemoglobin is not None and hemoglobin < 12.5:
        is_eligible = False
        reasons.append("Hemoglobin levels must be at least 12.5 g/dL (NBTC Guideline).")
        
    min_days = 90 if gender == "Male" else 120
    if days_since_last is not None and days_since_last < min_days:
        is_eligible = False
        reasons.append(f"For {gender.lower()} donors, the minimum gap is {min_days} days. Your gap is {days_since_last} days.")
        
    if symptoms:
        is_eligible = False
        reasons.append("Cannot donate if feeling unwell, having active cold, flu, sore throat or infection.")
        
    if travel:
        is_eligible = False
        reasons.append("Recent travel to malaria-endemic zones requires a waiting period of at least 3-12 months.")
        
    if tattoo_surgery:
        is_eligible = False
        reasons.append("Tattoos, piercings, or major surgeries within the last 6 months carry temporary deferrals.")
        
    return is_eligible, reasons

def get_donor_badge(donation_count):
    """Returns badge tier details based on donor donation count."""
    if donation_count <= 0:
        return {
            "title": "Rakt Rookie",
            "emoji": "🌱",
            "color": "#7F8C8D",
            "desc": "Registered as a potential donor. Ready to make the first impact!"
        }
    elif donation_count == 1:
        return {
            "title": "Rakt Sevak",
            "emoji": "🩸",
            "color": "#E74C3C",
            "desc": "Completed 1 lifesaving blood donation."
        }
    elif donation_count <= 3:
        return {
            "title": "Sanjeevani Warrior",
            "emoji": "🛡️",
            "color": "#3498DB",
            "desc": f"Completed {donation_count} donations. Supporting the Indian emergency medical network."
        }
    elif donation_count <= 5:
        return {
            "title": "Veer Raktdaata",
            "emoji": "🏆",
            "color": "#F1C40F",
            "desc": f"Outstanding effort! Completed {donation_count} donations."
        }
    else:
        return {
            "title": "Maha Donor",
            "emoji": "🌟",
            "color": "#9B59B6",
            "desc": f"A true legend! Saved up to {donation_count * 3} lives with {donation_count} donations."
        }

def simulate_proximity_and_eta(donor_name, donor_city, hospital_name, hospital_city):
    """
    Generates a deterministic distance and ETA based on strings.
    This guarantees that the exact same donor and hospital request will show the same distance/ETA.
    """
    # Create unique string combination
    combined = f"{donor_name}-{donor_city}-{hospital_name}-{hospital_city}"
    hash_val = int(hashlib.md5(combined.encode('utf-8')).hexdigest(), 16)
    
    # Check if they are in the same city. If not, distance is much larger
    same_city = donor_city.strip().lower() == hospital_city.strip().lower()
    
    if same_city:
        # Distance between 1.2 km and 9.8 km
        distance = round(1.2 + (hash_val % 86) / 10.0, 1)
        # ETA between 8 mins and 45 mins
        eta = int(8 + (hash_val % 37))
    else:
        # Out of city simulation: distance between 45 km and 250 km
        distance = round(45.0 + (hash_val % 205), 1)
        # ETA between 60 mins and 240 mins
        eta = int(60 + (hash_val % 180))
        
    return distance, eta

def get_safety_tips():
    return {
        "pre": [
            "Have a healthy, low-fat meal before donating. Avoid fatty foods which can affect blood tests.",
            "Drink plenty of water (about 500ml) during the 2 hours preceding your appointment.",
            "Get a good night's sleep of at least 7-8 hours prior to your donation day.",
            "Avoid alcohol consumption for 24 hours prior to donation."
        ],
        "during": [
            "Wear clothing with sleeves that can easily be rolled up past your elbows.",
            "Stay relaxed: breathe deeply, listen to music, or chat with the medical staff.",
            "Notify the nurse immediately if you feel dizzy, cold, or experience any discomfort."
        ],
        "post": [
            "Keep the strip bandage on for at least 4-6 hours, keeping it dry.",
            "Drink extra fluids over the next 24-48 hours to replenish volume.",
            "Avoid heavy lifting or strenuous physical exercise for the rest of the day.",
            "If the needle site starts to bleed, apply pressure and raise your arm until it stops."
        ]
    }

def get_emergency_guidance():
    return [
        "**Stay Calm:** Panic delays coordination. Work step-by-step using our contact listings.",
        "**Double Check Details:** Make sure you have the exact patient name, blood group, hospital name, and contact person details ready before calling donors.",
        "**Prepare Transportation:** If a donor is willing but lacks transport, arrange a cab or pick-up to speed up their arrival.",
        "**Notify the Hospital:** Inform the hospital's blood bank coordinator that you have contacted independent donors who are on their way.",
        "**Encourage Replacements:** If you receive blood from a blood bank, commit to finding replacement donors to keep the reserve levels balanced."
    ]
