# FastAPI for Data Scientists: Hands-On Exercise

A small, runnable companion to **Part 2** of the
[MLOps for Data Scientists](https://futureproofds.com/blog/mlops-for-data-scientists)
series. You'll take a tiny churn model, wrap it in a FastAPI service, call it for
a real prediction, and add one endpoint yourself. Budget about **10-20 minutes**.

---

## 1. About this repo

This is a hands-on exercise to make the article's concepts click. You'll clone
it, run a working FastAPI service in a couple of commands, make a real
prediction, and then fill in a small TODO so the ideas stick. No prior FastAPI
experience needed. If you can train a model and write a function, you're ready.

## 2. Quick start

This project uses [uv](https://docs.astral.sh/uv/), the same tool as
[Part 1](https://futureproofds.com/blog/mlops-for-data-scientists/1-notebooks-dont-ship)
of this series. The nice thing: with `uv run`, you **don't
create or activate a virtual environment yourself**. The first time you run
something, uv reads `pyproject.toml`, builds an isolated environment, and
installs the dependencies for you, then caches it. That's the modern Python
workflow, and it's what you'd use for a real service.

> **Don't have uv?** Install it in one line:
> `curl -LsSf https://astral.sh/uv/install.sh | sh` (see
> [the docs](https://docs.astral.sh/uv/getting-started/installation/) for other
> platforms). Prefer plain pip? See [Using pip instead](#using-pip-instead).

### Step 1: Train the model

```bash
uv run scripts/train_model.py
```

*You should see:* on this **first** `uv run`, uv resolves and installs the
dependencies (fast), then `Model trained and saved to .../churn_model.pkl`.
That `.pkl` is the trained model your API will serve. Later `uv run` commands
reuse the same environment, so they start instantly.

### Step 2: Start the server (leave this running)

```bash
uv run uvicorn my_ml_project.api:app --reload
```

*You should see:* `Uvicorn running on http://127.0.0.1:8000`. Notice the terminal
**doesn't come back to a prompt**. The server is running and holding it. That's
expected. Leave it be; you'll watch log lines appear here as requests come in.
(To stop it later, press `Ctrl+C`.)

### Step 3: Call the service (in a SECOND terminal)

Open a new terminal and run the client:

```bash
uv run client/call_predict.py
```

*You should see:* a churn probability and a risk band come back, plus a new
log line appear in your **first** terminal. That log line is your service
telling you it handled a request.

### Using pip instead

Prefer the classic `venv` + `pip` workflow? Here you *do* manage the environment
yourself. Because this uses the src layout, install the project itself so the
`my_ml_project` package is importable:

```bash
python3 -m venv venv           # create an isolated environment
source venv/bin/activate       # activate it; your prompt now shows (venv)
pip install -e .               # installs the project and its dependencies

python scripts/train_model.py
uvicorn my_ml_project.api:app --reload
# in a second terminal (activate the venv there too): python client/call_predict.py
```

## 3. Your exercise

Your job is to get hands-on with the running service:

1. **Get the service running** by following steps 1 and 2 in
   [Quick start](#2-quick-start) to train the model and start the server.
2. **Make a prediction** by running `uv run client/call_predict.py` in a second
   terminal and reading the response. Try changing the numbers in that script
   and re-running.
3. **Explore the auto-generated docs** by opening
   [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.
   FastAPI builds this interactive page for free from your Pydantic models.
   Expand the `/predict` endpoint, click **Try it out**, and send a request
   right from the browser.
4. **Implement the `/health` endpoint.** Open `src/my_ml_project/api.py` and find
   the `TODO` near the bottom. Add a simple health check endpoint.
5. **Verify it works.** With the server running, visit
   [http://localhost:8000/health](http://localhost:8000/health) in your browser.
   You should see `{"status": "ok"}`.

## 4. Hints

<details>
<summary>Stuck on the <code>/health</code> endpoint? Click here.</summary>

- Use `@app.get("/health")`, since it's a **GET** request, not a `@app.post`.
- The function can just return a plain dictionary; FastAPI converts it to JSON
  for you.
- It's three lines of code total. Something like:

  ```python
  @app.get("/health")
  def health():
      return {"status": "ok"}
  ```

</details>

## 5. Going further (optional)

Want to push a little past the article? Try these:

- **Add input validation.** Reject obviously invalid input, for example a
  negative `tenure_months`. (Hint: Pydantic's `Field` lets you set constraints
  like `Field(ge=0)`.)
- **Add structured logging.** The `/predict` endpoint already logs each request.
  Extend it to record the prediction in a more structured format (e.g. JSON) so
  it'd be easy to ship to a logging system later.

---

That's it. You've served a model over HTTP, called it, read auto-generated
docs, and added your own endpoint. That's the core of putting a model behind an
API.
