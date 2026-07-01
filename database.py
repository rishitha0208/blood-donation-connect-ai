import sqlite3
import os
from datetime import datetime, timedelta
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blood_donation.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database and seeds it with rich mock data if empty."""
    # Delete old database to force recreate with ABHA column and Indian schema
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(donors)")
            columns = [info[1] for info in cursor.fetchall()]
            conn.close()
            if "abha_id" not in columns:
                os.remove(DB_PATH)
        except Exception:
            pass

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Donors table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS donors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        blood_group TEXT NOT NULL,
        phone TEXT NOT NULL,
        city TEXT NOT NULL,
        last_donation_date TEXT,
        donation_count INTEGER DEFAULT 1,
        availability INTEGER DEFAULT 1, -- 1 for Yes, 0 for No
        registered_at TEXT DEFAULT CURRENT_TIMESTAMP,
        abha_id TEXT
    )
    """)
    
    # Emergency requests table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emergencies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        blood_group TEXT NOT NULL,
        hospital TEXT NOT NULL,
        city TEXT NOT NULL,
        urgency TEXT NOT NULL, -- Low, Medium, High
        status TEXT DEFAULT 'Pending', -- Pending, Resolved
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Check if empty to seed mock data
    cursor.execute("SELECT COUNT(*) FROM donors")
    if cursor.fetchone()[0] == 0:
        # Seed mock donors across different Indian cities and blood groups with mock ABHA IDs
        mock_donors = [
            ("Rahul Sharma", 28, "O+", "+91 98765 43210", "Mumbai", (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d"), 3, 1, "91-4829-1029-4820"),
            ("Priya Patel", 24, "O-", "+91 91234 56789", "Mumbai", (datetime.now() - timedelta(days=45)).strftime("%Y-%m-%d"), 1, 1, "91-1029-3849-5012"),
            ("Amit Verma", 35, "A+", "+91 98123 45678", "Delhi", (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d"), 5, 1, "91-5829-1024-9582"),
            ("Sneha Reddy", 31, "A-", "+91 88990 12345", "Bangalore", (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d"), 2, 0, "91-3829-1029-4821"),
            ("Vikram Singh", 42, "B+", "+91 77665 44321", "Delhi", (datetime.now() - timedelta(days=95)).strftime("%Y-%m-%d"), 6, 1, "91-2849-1029-3829"),
            ("Ananya Das", 29, "B-", "+91 95555 12340", "Kolkata", None, 0, 1, "91-4829-1029-4833"),
            ("Rohan Mehta", 27, "AB+", "+91 94444 88888", "Mumbai", (datetime.now() - timedelta(days=200)).strftime("%Y-%m-%d"), 4, 1, "91-8822-1029-4820"),
            ("Neha Nair", 33, "AB-", "+91 93333 77777", "Bangalore", (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d"), 2, 1, "91-4829-2244-4820"),
            ("Suresh Kumar", 50, "O+", "+91 92222 66666", "Chennai", (datetime.now() - timedelta(days=150)).strftime("%Y-%m-%d"), 8, 1, "91-4829-1029-9999"),
            ("Kiran Rao", 22, "A+", "+91 90000 11111", "Bangalore", (datetime.now() - timedelta(days=100)).strftime("%Y-%m-%d"), 1, 1, "91-1122-3344-5566"),
            ("Aditya Joshi", 29, "O-", "+91 91111 22222", "Pune", None, 0, 1, "91-7788-9900-1122"),
            ("Meera Sen", 26, "B+", "+91 92222 33333", "Kolkata", (datetime.now() - timedelta(days=70)).strftime("%Y-%m-%d"), 3, 1, "91-5566-7788-9900"),
            ("Rajesh Iyer", 38, "O-", "+91 93333 44444", "Chennai", (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"), 2, 0, "91-1234-5678-9012"),
            ("Pooja Hegde", 30, "A-", "+91 94444 55555", "Hyderabad", (datetime.now() - timedelta(days=110)).strftime("%Y-%m-%d"), 4, 1, "91-2345-6789-0123"),
            ("Vijay Devera", 34, "AB+", "+91 95555 66666", "Hyderabad", None, 0, 1, "91-3456-7890-1234")
        ]
        cursor.executemany("""
        INSERT INTO donors (name, age, blood_group, phone, city, last_donation_date, donation_count, availability, abha_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, mock_donors)
        
    cursor.execute("SELECT COUNT(*) FROM emergencies")
    if cursor.fetchone()[0] == 0:
        # Seed mock emergency requests at Indian hospitals
        mock_emergencies = [
            ("Aarav Gupta", "O-", "KEM Hospital", "Mumbai", "High", "Pending", (datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")),
            ("Sunita Rao", "A+", "AIIMS Delhi", "Delhi", "Medium", "Resolved", (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")),
            ("Ramesh Krishnan", "B+", "St. John's Medical College", "Bangalore", "High", "Pending", (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")),
            ("Tanvi Sen", "AB-", "AMRI Hospital", "Kolkata", "Low", "Pending", (datetime.now() - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")),
        ]
        cursor.executemany("""
        INSERT INTO emergencies (patient_name, blood_group, hospital, city, urgency, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, mock_emergencies)
        
    conn.commit()
    conn.close()
 
def register_donor(name, age, blood_group, phone, city, last_donation_date, availability, donation_count=1, abha_id=None):
    """Registers a new donor or updates donation count for an existing one."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if a donor with same phone number already exists
    cursor.execute("SELECT id, donation_count FROM donors WHERE phone = ?", (phone,))
    existing = cursor.fetchone()
    
    if existing:
        # Update details and increment donation count
        new_count = existing['donation_count'] + 1 if donation_count == 1 else donation_count
        cursor.execute("""
        UPDATE donors 
        SET name = ?, age = ?, blood_group = ?, city = ?, last_donation_date = ?, availability = ?, donation_count = ?, abha_id = ?
        WHERE id = ?
        """, (name, age, blood_group, city, last_donation_date, availability, new_count, abha_id, existing['id']))
        donor_id = existing['id']
    else:
        cursor.execute("""
        INSERT INTO donors (name, age, blood_group, phone, city, last_donation_date, donation_count, availability, abha_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, age, blood_group, phone, city, last_donation_date, donation_count, availability, abha_id))
        donor_id = cursor.lastrowid
        
    conn.commit()
    conn.close()
    return donor_id

def search_donors(blood_group, city):
    """Returns exact matching donors who are active."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT name, age, blood_group, phone, city, last_donation_date, donation_count, availability, abha_id
    FROM donors
    WHERE blood_group = ? AND LOWER(city) = LOWER(?) AND availability = 1
    ORDER BY last_donation_date DESC
    """, (blood_group, city))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_donor_by_id(donor_id):
    """Fetches a donor profile by their database ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors WHERE id = ?", (donor_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def create_emergency_request(patient_name, blood_group, hospital, city, urgency):
    """Creates a new emergency request."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO emergencies (patient_name, blood_group, hospital, city, urgency, status, created_at)
    VALUES (?, ?, ?, ?, ?, 'Pending', ?)
    """, (patient_name, blood_group, hospital, city, urgency, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def resolve_emergency(emergency_id):
    """Marks an emergency request as resolved."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE emergencies SET status = 'Resolved' WHERE id = ?", (emergency_id,))
    conn.commit()
    conn.close()

def get_all_donors_df():
    """Returns all donors as a Pandas DataFrame for dashboard and CSV exporting."""
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM donors", conn)
    conn.close()
    return df

def get_emergencies_df():
    """Returns all emergencies as a Pandas DataFrame."""
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM emergencies ORDER BY id DESC", conn)
    conn.close()
    return df

def get_dashboard_stats():
    """Aggregates system statistics."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    stats = {}
    cursor.execute("SELECT COUNT(*) FROM donors")
    stats['total_donors'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM donors WHERE availability = 1")
    stats['available_donors'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM emergencies WHERE status = 'Pending'")
    stats['active_emergencies'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM emergencies WHERE status = 'Resolved'")
    stats['resolved_emergencies'] = cursor.fetchone()[0]
    
    conn.close()
    return stats

