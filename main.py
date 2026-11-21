import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


def _fallback_route(text: str):
    cleaned = (text or "").strip()
    if not cleaned:
        return ["status"]
    return ["note", cleaned]


def _fallback_dispatch(cmd):
    if not cmd:
        return "STATUS:OK|MODE:FALLBACK|ENC:UTF-8"
    if cmd[0] == "status":
        return "STATUS:OK|APP:JANNAT_LIGHT|ENC:UTF-8"
    return f"OK:{' '.join(str(x) for x in cmd)}"


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
        print("HEALTH_OK|MODE:FALLBACK")


def main():
    args = sys.argv[1:]
    if not args:
        print(dispatch(["status"]))
        return
    if args[0] == "health":
        health_main()
        return
    routed = route_bangla(" ".join(args))
    print(dispatch(routed))


if __name__ == "__main__":
    main()
    
