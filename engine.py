import json
import os
import datetime
from datetime import datetime as dt

RECEIPTS_FILE = 'receipts.json'

def load_receipts():
    if not os.path.exists(RECEIPTS_FILE):
        return {"receipts": [], "streak": 0, "last_receipt_date": None}
    with open(RECEIPTS_FILE, 'r') as f:
        return json.load(f)

def save_receipts(data):
    with open(RECEIPTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def add_receipt(title, category, impact, confidence):
    data = load_receipts()
    now = dt.now()
    date_str = now.isoformat()
    
    new_receipt = {
        "id": len(data['receipts']) + 1,
        "date": date_str,
        "title": title,
        "category": category, # Win, Completion, Fast Decision, Smart Move
        "impact": impact, # 1-10
        "confidence_score": confidence, # 1-10 (how Kian felt at the time)
    }
    
    # Update streak
    last_date = data.get('last_receipt_date')
    if last_date:
        last_dt = dt.fromisoformat(last_date)
        delta = (now.date() - last_dt.date()).days
        if delta == 1:
            data['streak'] += 1
        elif delta > 1:
            data['streak'] = 1
    else:
        data['streak'] = 1
        
    data['last_receipt_date'] = date_str
    data['receipts'].append(new_receipt)
    save_receipts(data)
    print(f"✅ Receipt logged: {title}. Impact: {impact}/10. Current Streak: {data['streak']} days.")

def get_summary():
    data = load_receipts()
    receipts = data['receipts']
    if not receipts:
        return "No receipts found. Time to build some evidence, sir."
    
    total_impact = sum(r['impact'] for r in receipts)
    categories = {}
    for r in receipts:
        cat = r['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    summary = f"--- CONFIDENCE SUMMARY ---\n"
    summary += f"Total Receipts: {len(receipts)}\n"
    summary += f"Current Streak: {data['streak']} days of building competence.\n"
    summary += f"Cumulative Impact Score: {total_impact}\n"
    summary += f"Category Breakdown:\n"
    for cat, count in categories.items():
        summary += f"- {cat}: {count}\n"
    return summary

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python engine.py [add/summary]")
    elif sys.argv[1] == "add":
        title = input("What did you achieve/decide? ")
        print("Categories: [Win, Completion, Fast Decision, Smart Move]")
        category = input("Category: ")
        impact = int(input("Impact (1-10): "))
        confidence = int(input("Confidence level (1-10): "))
        add_receipt(title, category, impact, confidence)
    elif sys.argv[1] == "summary":
        print(get_summary())
