# Flask + Docker Template for Cloud Run

This repository is a **minimal starter template** for building JSON-only Flask services that run in Docker and deploy cleanly to **Google Cloud Run**.

It gives you:

- A ready-to-use `Dockerfile` for containerizing a Flask app.
- A small `helpers.py` module with convenience functions for JSON responses.
- A `requirements.txt` for the runtime dependencies.
- Sensible `.gitignore` and `.dockerignore` defaults.

You **must add your own `app.py`** (the actual Flask application) when you create a child project from this template.

> ✅ After you spin up a new project from this template, you should **replace this README** with documentation for your actual service. This file is intentionally generic.

---

## 1. Using this repo as a template

1. On GitHub, click **Use this template → Create a new repository**.
2. Choose:
   - Your account/organization.
   - A new repo name (e.g. `restcalc-service`).
   - Visibility (public/private).
3. Click **Create repository from template**.

Then clone your new repo locally:

```bash
git clone https://github.com/<your-username>/<your-new-repo>.git
cd <your-new-repo>
```

Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
# or on Windows:
# venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Now you’re ready to create `app.py`.

---

## 2. Adding `app.py` (your Flask application)

This template expects an **`app.py`** at the repo root that exposes a Flask application named `app`. A simple starting point:

```python
from flask import Flask, request
from helpers import rest_response, rest_error

app = Flask(__name__)

# Optional: keep JSON keys in insertion order instead of alphabetical
app.config["JSON_SORT_KEYS"] = False


@app.route("/health", methods=["GET"])
def health():
    """Basic health check endpoint for Cloud Run / monitoring."""
    return rest_response("OK")


@app.route("/echo", methods=["POST"])
def echo():
    """Example JSON endpoint that echoes back a message field."""
    data = request.get_json(silent=True) or {}

    if "message" not in data:
        return rest_error("Field 'message' is required")

    return rest_response({"message": data["message"]})


if __name__ == "__main__":
    # For local development only. In Cloud Run, the Dockerfile will
    # run the app via a production server (e.g. gunicorn).
    app.run(host="0.0.0.0", port=8080)
```

Key points:

- The variable **`app`** is the Flask application object.  
- Local dev: `python app.py` will start the server on `http://localhost:8080`.  
- For production, Cloud Run will run your app using whatever command is specified in the `Dockerfile` (for example, a `gunicorn app:app` entry point).

You can change routes, add blueprints, etc., but **keep the `app` variable** exported from `app.py` so the container entry point can find it.

---

## 3. What `helpers.py` does

`helpers.py` centralizes JSON response formatting so that every endpoint returns a consistent envelope.

It defines two helpers:

```python
from flask import jsonify

def rest_response(obj):
    """Wraps a successful result in a standard JSON envelope."""
    return jsonify({
        "status": "OK",
        "result": obj,
    })


def rest_error(message: str):
    """Returns an error response with HTTP 400 and a message."""
    return jsonify({
        "status": "ERROR",
        "result": message,
    }), 400
```

Usage in your routes:

```python
from helpers import rest_response, rest_error

@app.route("/example")
def example():
    try:
        data = {"foo": "bar"}
        return rest_response(data)
    except Exception as exc:
        return rest_error(str(exc))
```

This gives you consistent payloads like:

```json
{
  "status": "OK",
  "result": {"foo": "bar"}
}
```

and on error:

```json
{
  "status": "ERROR",
  "result": "Something bad happened"
}
```

---

## 4. Files in this template

- **`app.py`** – **You add this.** Your Flask app entry point. Must define `app`.
- **`helpers.py`** – Shared helpers for JSON responses (`rest_response`, `rest_error`).
- **`requirements.txt`** – Python dependencies for the container image.
- **`Dockerfile`** – Builds a container image that runs your Flask app.
- **`.gitignore`** – Standard Python ignores (venv, `__pycache__`, etc.).
- **`.dockerignore`** – Excludes unwanted files from the Docker build context.

You are free to add more modules, packages, and tests as your service grows.

---

## 5. Running locally

After you’ve created `app.py` and installed dependencies:

```bash
# In your project directory:
python app.py
```

By default the example above listens on:

- `http://localhost:8080/health`
- `http://localhost:8080/echo`

You can hit those with curl:

```bash
curl http://localhost:8080/health
curl -X POST http://localhost:8080/echo \
     -H "Content-Type: application/json" \
     -d '{"message": "hello"}'
```

---

## 6. Building and running the Docker image locally

Build the image (replace `my-flask-service` with whatever name you want):

```bash
docker build -t my-flask-service .
```

Run it:

```bash
docker run -p 8080:8080 my-flask-service
```

Then open:

- `http://localhost:8080/health`

The container should expose port **8080**, which is what Cloud Run expects by default. The Dockerfile included in this template is configured to start your Flask app when the container starts.

---

## 7. Deploying to Cloud Run _from this repo_

There are two common ways to deploy this template to **Cloud Run**.

### Option A: Deploy from source (GitHub → Cloud Run)

1. Push your child repo (with `app.py` added) to GitHub.
2. In the **Google Cloud Console**, go to **Cloud Run**.
3. Click **Create Service** (or **Deploy**).
4. Choose **Deploy one revision from source**.
5. Select:
   - **Source**: GitHub.
   - Connect your GitHub account and choose your repo and branch.
   - Use the included `Dockerfile` for the build.
6. Configure:
   - **Region**: pick the region you want (e.g. `us-west1`).
   - **Service name**: something like `my-flask-service`.
   - **Container port**: `8080` (default for this template).
   - **Authentication**: allow unauthenticated if this is a public HTTP API.
7. Click **Create**.

Cloud Run will:

- Build a container image using your `Dockerfile`.
- Deploy it.
- Give you a public HTTPS URL like:

```
https://my-flask-service-xxxxx-uc.a.run.app
```

Hit `/health` on that URL to verify the deployment.

---

### Option B: Deploy via `gcloud` CLI + Dockerfile

If you prefer to deploy from your local machine (with the Google Cloud SDK installed):

```bash
# From your project root, where Dockerfile lives
gcloud builds submit --tag gcr.io/PROJECT_ID/my-flask-service

gcloud run deploy my-flask-service \
  --image gcr.io/PROJECT_ID/my-flask-service \
  --platform managed \
  --region us-west1 \
  --allow-unauthenticated
```

Replace `PROJECT_ID` and region as needed. Once the deploy finishes, you’ll get a Cloud Run URL. Again, check `/health`.

---

## 8. Customizing for your own project

When you create a new project from this template, you will likely want to:

- Rename routes and add new ones.
- Introduce additional modules or packages (e.g. `services/`, `models/`, etc.).
- Swap out or extend `helpers.py` if your response envelope changes.
- Add tests (`pytest`, `unittest`) and a basic CI workflow.
- Add configuration management (e.g. environment variables for DB URLs, API keys, etc.).

This template is intentionally minimal so you can bend it toward **REST APIs**, **JSON-only microservices**, or small web apps.

---

## 9. Replace this README in child projects

This README is written for the **template itself**.

Once you have an actual service (e.g. “Showa year converter”, “Dijkstra path API”, etc.):

1. Copy any sections you like (local dev, Cloud Run deploy).
2. Replace this file with a README that describes:
   - What your service does.
   - API endpoints and example requests/responses.
   - Any environment variables or configuration.
   - Versioning, changelog, etc.

Think of this README as the scaffolding that you **tear down** once the real building is up.

---

Happy shipping! 🚀
