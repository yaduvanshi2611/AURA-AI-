# AURA AI — cloud platform starter

A modular FastAPI starter with user registration, bearer-token sign-in, hashed API keys, SQLAlchemy storage, replaceable inference, a training-job placeholder, and a simple web page.

## Run locally

1. Install Python 3.11 or newer.
2. Create and activate an environment: `python -m venv .venv` then `.venv\\Scripts\\Activate.ps1` on Windows.
3. Install packages: `pip install -r requirements.txt`.
4. Copy `.env.example` to `.env` and change `SECRET_KEY` to a long random value before deploying.
5. Run `uvicorn app.main:app --reload`; open `http://127.0.0.1:8000` or `/docs`.

The default `demo` inference provider echoes a short prompt locally. It does not call an external AI service or download a model. The app creates a random temporary signing key for local development when `SECRET_KEY` is unset. Before deployment, set a stable, long random `SECRET_KEY` in `.env` so sessions remain valid after restarts.

For an optional open-weight development model, install compatible `transformers` and `torch`, set `INFERENCE_BACKEND=huggingface-dev`, and restart. `DEV_MODEL_ID` selects that temporary provider. This is separate from the future AURA model; implement that behind `InferenceProvider` when ready. The base app can start without the optional ML packages when using `demo`.

Register via `/api/auth/register`. Sign in at `/api/auth/token` using form fields `username` (email) and `password`. Send the returned token as `Authorization: Bearer ...`. Create keys at `/api/keys`; a key is shown once and stored only as a hash. Revoke with `DELETE /api/keys/{id}`.

`/api/training/jobs` is a placeholder and does not train a model. Add a queue, private dataset storage, and workers before use. This starter needs HTTPS, a production secret, database migrations, rate limits, backups, and monitoring before deployment.

## Docker

`docker build -t aura-ai .` then `docker run --env-file .env -p 8000:8000 aura-ai`.
