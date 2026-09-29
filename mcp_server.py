import sys
import json
from client import CalendarDeconflictionScheduler

scheduler = CalendarDeconflictionScheduler()

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-autonomous-calendar-deconfliction-scheduler-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "book_slot",
                        "description": "Book a scheduled meeting slot on the personal calendar",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "start_hour": {"type": "number"},
                                "start_min": {"type": "number"},
                                "duration_min": {"type": "number"},
                                "title": {"type": "string"}
                            },
                            "required": ["start_hour", "start_min", "duration_min", "title"]
                        }
                    },
                    {
                        "name": "find_available_slots",
                        "description": "Find non-conflicting meeting windows with buffer time guarantees",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "duration_min": {"type": "number"}
                            },
                            "required": ["duration_min"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "book_slot":
            scheduler.book_slot(args["start_hour"], args["start_min"], args["duration_min"], args["title"])
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": "Slot booked successfully"}]}}
        elif tool_name == "find_available_slots":
            slots = scheduler.find_available_slots(args["duration_min"])
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(slots, indent=2)}]}}

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_res = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
