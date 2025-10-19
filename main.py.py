from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import re
import json

app = FastAPI(title="TechNova Router API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def parse_query(q: str):
    text = q.strip()

    # Ticket status
    if match := re.search(r"status of ticket (\d+)", text, re.I):
        return "get_ticket_status", {"ticket_id": int(match.group(1))}

    # Schedule meeting
    if match := re.search(r"schedule a meeting on (\d{4}-\d{2}-\d{2}) at (\d{1,2}:\d{2}) in room (\w+)", text, re.I):
        return "schedule_meeting", {
            "date": match.group(1),
            "time": match.group(2),
            "meeting_room": match.group(3),
        }

    # Expense balance
    if match := re.search(r"expense balance .* employee (\d+)", text, re.I):
        return "get_expense_balance", {"employee_id": int(match.group(1))}

    # Performance bonus
    if match := re.search(r"performance bonus .* employee (\d+) .* (\d{4})", text, re.I):
        return "calculate_performance_bonus", {
            "employee_id": int(match.group(1)),
            "current_year": int(match.group(2)),
        }

    # Office issue
    if match := re.search(r"office issue (\d+) .* department (\w+)", text, re.I):
        return "report_office_issue", {
            "issue_code": int(match.group(1)),
            "department": match.group(2),
        }

    return None, None

@app.get("/execute")
def execute(q: str = Query(...)):
    name, args = parse_query(q)
    if not name:
        raise HTTPException(status_code=400, detail="Query format not recognized")
    return {"name": name, "arguments": json.dumps(args)}

@app.get("/")
def home():
    return {"message": "Use /execute?q=your query"}
