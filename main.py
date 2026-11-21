import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def _fallback_route(text):
    cleaned = (text or "").strip()
    return {"action": "status"} if not cleaned else {"action": "note_add", "text": cleaned}

def _fallback_dispatch(command):
    if isinstance(command, dict) and command.get("action") == "status":
        return '{"status":"ok","action":"status","message":"Jannat is ready.","encoding":"UTF-8"}'
    return '{"status":"error","action":"fallback","message":"Core modules are unavailable."}'

try:
    from bangla_router import route_bangla
except Exception:
    route_bangla = _fallback_route

try:
    from silent_controller import dispatch
except Exception:
    dispatch = _fallback_dispatch

try:
    from health_check import main as health_main
except Exception:
    def health_main():
        print("HEALTH_FAIL|MODE:FALLBACK")
        return 1

def main():
    args = sys.argv[1:]
    if args and args[0].lower() == "health":
        return health_main()
    text = " ".join(args)
    routed = route_bangla(text) if text else {"action": "status"}
    print(dispatch(routed))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
