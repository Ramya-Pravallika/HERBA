"""
Script to seed the SQLite database with initial remedy data
"""

from database import init_db, get_db_connection
import json

def seed_data():
    init_db()
    conn = get_db_connection()
    c = conn.cursor()
    
    # Clear existing data to avoid duplicates on re-run
    c.execute('DELETE FROM remedies')
    c.execute('DELETE FROM seek_help_criteria')
    
    # --- DATA ---
    
    # COLD & CONGESTION
    c.execute('''
        INSERT INTO remedies (symptom_type, name, rationale, steps_json, precautions_json, avoid_if_json, safe_for_pregnancy, safe_for_children, min_age)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'cold',
        'Warm Salt Water Gargle',
        'Helps soothe a sore throat and reduce swelling by drawing out fluids from inflamed tissues.',
        json.dumps([
            "Mix 1/4 to 1/2 teaspoon of salt into an 8-ounce glass of warm water.",
            "Gargle the solution in your throat for 10-15 seconds.",
            "Spit it out (do not swallow).",
            "Repeat 2-4 times a day as needed."
        ]),
        json.dumps(["Do not make the water too hot.", "Ensure children do not swallow the mixture."]),
        json.dumps([]),
        True, True, 6
    ))
    
    c.execute('''
        INSERT INTO remedies (symptom_type, name, rationale, steps_json, precautions_json, avoid_if_json, safe_for_pregnancy, safe_for_children, min_age)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'cold',
        'Steam Inhalation',
        'Warm, moist air helps loosen mucus in nasal passages and throat.',
        json.dumps([
            "Boil water and pour it into a heat-safe bowl.",
            "Lean over the bowl (keeping face 8-12 inches away) with a towel over your head to trap steam.",
            "Breathe deeply through your nose for 5-10 minutes."
        ]),
        json.dumps(["Risk of scald/burns - be very careful with hot water.", "Keep eyes closed."]),
        json.dumps([]),
        True, False, 12
    ))

    # HEADACHE
    c.execute('''
        INSERT INTO remedies (symptom_type, name, rationale, steps_json, precautions_json, avoid_if_json, safe_for_pregnancy, safe_for_children, min_age)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'headache',
        'Cold Compress',
        'Numbing effect helps dull pain and constrict blood vessels.',
        json.dumps([
            "Wrap ice or a cold pack in a clean towel.",
            "Apply to forehead or neck for 15 minutes.",
            "Take a break for 15 minutes before re-applying."
        ]),
        json.dumps(["Do not apply ice directly to skin."]),
        json.dumps([]),
        True, True, 2
    ))
    
    # STOMACH
    c.execute('''
        INSERT INTO remedies (symptom_type, name, rationale, steps_json, precautions_json, avoid_if_json, safe_for_pregnancy, safe_for_children, min_age)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'stomach',
        'Ginger Tea',
        'Ginger helps speed up stomach emptying and reduces nausea.',
        json.dumps([
            "Peel and slice a 1-inch piece of fresh ginger.",
            "Boil in water for 5-7 minutes.",
            "Strain and sip slowly."
        ]),
        json.dumps(["Can cause heartburn in some people."]),
        json.dumps([]),
        True, True, 2
    ))

    # --- SEEK HELP CRITERIA ---
    
    # Cold Info
    criteria_list = [
        "Difficulty breathing or shortness of breath",
        "High fever (above 103°F/39.4°C) or fever lasting >3 days",
        "Chest pain or pressure",
        "Blue color in lips or face"
    ]
    for criteria in criteria_list:
        c.execute('INSERT INTO seek_help_criteria (symptom_type, criteria) VALUES (?, ?)', ('cold', criteria))

    # Headache Info
    criteria_list = [
        "Sudden, severe headache ('thunderclap')",
        "Headache with stiff neck, fever, or confusion",
        "Headache following a head injury",
        "Vision loss or weakness"
    ]
    for criteria in criteria_list:
        c.execute('INSERT INTO seek_help_criteria (symptom_type, criteria) VALUES (?, ?)', ('headache', criteria))
        
    conn.commit()
    conn.close()
    print("Database seeded successfully with remedies and safety criteria!")

if __name__ == "__main__":
    seed_data()
