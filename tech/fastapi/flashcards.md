# 🃏 FastAPI Flashcards

> Pull from: L01 Python Types Intro · L02 Concurrency &amp; Async/Await · L03 Environment Variables · L04 First Steps · L05 ASGI Protocol · L06 MiniAPI

---

## L01 — Python Types Intro

**Q: What is a type hint in Python?**
<details><summary>Answer</summary>

A **type hint** (also called type annotation) is a special syntax using `:` to declare what type a variable or parameter should be. Example: `name: str`. Python itself does NOT enforce them at runtime — they're metadata for editors and tools like FastAPI/Pydantic.
</details>

---

**Q: Does adding type hints change what Python does at runtime?**
<details><summary>Answer</summary>

No. Python ignores type hints completely at runtime. `def f(x: int): pass` called with `f("hello")` will NOT crash. Only tools like **FastAPI** and **Pydantic** read and enforce type hints.
</details>

---

**Q: What is the difference between `name: str` and `name = "john"`?**
<details><summary>Answer</summary>

- `name: str` → **type hint** — what type the variable should be (editor/FastAPI sees this)
- `name = "john"` → **default value** — what value it gets if nothing is passed
- `name: str = "john"` → **both** — type hint AND default value combined
- Key tell: `:` = type hint, `=` = default value
</details>

---

**Q: Name the 5 simple built-in types you can use as hints.**
<details><summary>Answer</summary>

`str`, `int`, `float`, `bool`, `bytes`

No imports needed — they're built into Python.
</details>

---

**Q: What is a "type parameter" and give an example?**
<details><summary>Answer</summary>

A **type parameter** is the inner type you specify inside `[ ]` for generic types (collections).

Example: `list[str]` — here `str` is the type parameter. It means "a list where every element is a string."

More examples: `dict[str, float]`, `tuple[int, int, str]`, `set[bytes]`
</details>

---

**Q: How do you declare a variable that can be an `int` OR a `str`?**
<details><summary>Answer</summary>

Use the `|` (vertical bar / pipe):
```python
def process(item: int | str):
    ...
```
This is called a **Union type**. Available natively in Python 3.10+.
</details>

---

**Q: What does `str | None = None` mean? Break down each part.**
<details><summary>Answer</summary>

- `str | None` → **Union type hint** — can be a string OR None
- `= None` → **default value** — defaults to None if not provided
- Together: "This param is optional — if given, must be str; if not given, it's None"
- `str | None` without `= None` means the param IS required but accepts None as a valid value
</details>

---

**Q: What does Pydantic's `BaseModel` give you that plain type hints don't?**
<details><summary>Answer</summary>

Plain type hints are passive. `BaseModel` **actively**:
1. Validates types at runtime (wrong type = error)
2. Auto-converts compatible types (string `"123"` → int `123`)
3. Gives rich editor autocomplete on the model instance
4. Generates clear validation error messages automatically

FastAPI is entirely built on Pydantic.
</details>

---

**Q: What is `Annotated[str, "metadata"]`? What does each part mean?**
<details><summary>Answer</summary>

`Annotated` lets you attach extra metadata to a type hint.

- **First arg (`str`)** = the actual type — Python and editors see this
- **Rest (`"metadata"`)** = extra info for tools — Python ignores it, FastAPI reads it

Example in FastAPI: `Annotated[str, Query(max_length=50)]` → FastAPI adds a max-length validation rule from the metadata.
</details>

---

**Q: List 5 things FastAPI does automatically from a single type annotation.**
<details><summary>Answer</summary>

1. **Editor support** — autocomplete, type checks
2. **Parameter reading** — from path, query, body, headers
3. **Type conversion** — string "42" → int 42
4. **Validation** — rejects wrong types with auto error response
5. **OpenAPI docs** — generates /docs UI automatically
</details>

---

**Q: `one_person: Person` — does this mean `one_person` IS the class Person, or an instance?**
<details><summary>Answer</summary>

An **instance** of the class Person. 

`one_person: Person` means "one_person is an object created from the Person class, like `Person(name='Alice')`." It does NOT mean one_person is the class itself.
</details>

---

**Q: What module do you import `Any` and `Annotated` from?**
<details><summary>Answer</summary>

Both come from Python's standard library `typing` module:

```python
from typing import Any, Annotated
```
</details>

---

## Cross-Topic Pulls

**Q: (AsyncIO link) FastAPI supports async — what does `async def` give you over regular `def`?**
<details><summary>Answer</summary>

`async def` creates a coroutine that can `await` I/O operations without blocking the event loop. In FastAPI, use `async def` for route handlers that do async I/O (DB calls, HTTP requests). FastAPI runs on an async server (uvicorn/ASGI) and handles both sync and async handlers.
</details>

---

**Q: (Pydantic link) What is the difference between a Python dataclass and a Pydantic BaseModel?**
<details><summary>Answer</summary>

- **Dataclass**: stores data with type hints but NO runtime validation — Python doesn't check types
- **Pydantic BaseModel**: validates + coerces data at runtime, raises clear errors on bad input, integrates with FastAPI's request parsing

FastAPI uses `BaseModel`, not dataclasses, for request/response bodies.
</details>

---

## L02 — Concurrency &amp; Async / Await

**Q: What is the difference between concurrency and parallelism?**
<details><summary>Answer</summary>

- **Concurrency** = multiple tasks making progress by interleaving on ONE thread — one pauses while waiting, another runs. Smart switching. (One waiter serving multiple tables.)
- **Parallelism** = multiple tasks truly running simultaneously on multiple CPU cores. (Multiple waiters, one table each.)

Web APIs need concurrency (lots of I/O waiting). Heavy CPU computation needs parallelism.
</details>

---

**Q: What is I/O-bound vs CPU-bound work?**
<details><summary>Answer</summary>

- **I/O-bound**: the bottleneck is waiting for input/output — network calls, DB queries, file reads. CPU is idle while waiting. → Use concurrency (async/await).
- **CPU-bound**: the bottleneck is actual computation — the CPU is maxed out doing math. → Use parallelism (multiprocessing).
</details>

---

**Q: What are the two rules of async/await in Python?**
<details><summary>Answer</summary>

1. `await` can ONLY be used inside an `async def` function
2. To call an `async def` function and get its result, you MUST `await` it

Calling `async_fn()` without `await` gives you a coroutine object, NOT the result.
</details>

---

**Q: What is a coroutine?**
<details><summary>Answer</summary>

A **coroutine** is what an `async def` function returns when called (without await). It's a pauseable function — a state machine that can be started, paused at `await` expressions, and resumed. FastAPI (via Starlette) knows how to run coroutines on the event loop.
</details>

---

**Q: You write `def my_route()` (not async) in FastAPI. What does FastAPI do with it?**
<details><summary>Answer</summary>

FastAPI automatically runs it in an **external threadpool** — this prevents it from blocking the async event loop. There's ~100ns of overhead, which is imperceptible. It's safe and correct. This is the recommended approach when your code uses sync libraries with no `await` support.
</details>

---

**Q: When should you use `async def` vs `def` in a FastAPI route?**
<details><summary>Answer</summary>

- **`async def`**: when your route calls something with `await` (async DB library, async HTTP client, etc.)
- **`def`**: when using sync libraries (no `await`), or when you're not sure — safe default
- **Never**: use blocking sync I/O (like `requests.get()`) inside `async def` — it freezes the event loop
</details>

---

**Q: Name the three layers under FastAPI and what each does.**
<details><summary>Answer</summary>

| Layer | Role |
|-------|------|
| **FastAPI** | Routes, validation, serialization (your app logic) |
| **Starlette** | Async ASGI framework foundation |
| **AnyIO** | Concurrency layer — supports asyncio AND Trio |

uvicorn (or another ASGI server) runs the whole stack.
</details>

---

**Q: What goes wrong if you call a blocking sync function (e.g. `time.sleep(5)`) inside `async def`?**
<details><summary>Answer</summary>

It **freezes the entire event loop** for 5 seconds. While that one coroutine is sleeping synchronously, NO other requests can be processed. The server appears hung. Always use async equivalents (`await asyncio.sleep(5)`) inside `async def`.
</details>

---

## L03 — Environment Variables

**Q: What is an environment variable?**
<details><summary>Answer</summary>

A **key=value pair** that lives in the operating system — outside your code. Any program, including Python, can read it at runtime. Used for config, secrets, and settings without hardcoding them.

Key facts: lives in OS, not in git, always a string (`str`).
</details>

---

**Q: What is the difference between `os.environ["KEY"]` and `os.getenv("KEY")`?**
<details><summary>Answer</summary>

- `os.getenv("KEY")` — safe, returns `None` if not set (or a custom default as 2nd arg): `os.getenv("KEY", "default")`
- `os.environ["KEY"]` — raises `KeyError` if the var is not set; use only when the var is truly mandatory

General rule: prefer `os.getenv` unless you want a loud crash on a missing var.
</details>

---

**Q: Env vars are always what type in Python? What's the implication?**
<details><summary>Answer</summary>

Always `str`. The OS stores everything as plain text.

Implication: you must cast manually in Python:
```python
port = int(os.getenv("PORT", "8000"))        # str → int
debug = os.getenv("DEBUG", "false") == "true" # str → bool (safe!)
```

`bool("False")` is `True` — never pass an env var directly to `bool()`.
</details>

---

**Q: What is a `.env` file and how does python-dotenv use it?**
<details><summary>Answer</summary>

A `.env` file is a plain-text file containing env var definitions (one `KEY=value` per line). It is NOT committed to git (add to `.gitignore`).

`python-dotenv` loads it into `os.environ` at runtime:
```python
from dotenv import load_dotenv
load_dotenv()  # reads .env and populates os.environ
name = os.getenv("MY_NAME")
```

Use case: local development — keeps secrets out of code while making them easy to set.
</details>

---

**Q: What is `pydantic-settings` `BaseSettings` and when should you use it?**
<details><summary>Answer</summary>

`BaseSettings` is a Pydantic class that reads env vars (and optionally `.env` files) with full type validation and coercion:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My App"
    port: int = 8000       # auto-cast from str env var
    debug: bool = False    # handles "true"/"false" safely

settings = Settings()
```

Use it when: you have multiple config values, want type safety, or need to validate config in production FastAPI apps.
</details>

---

**Q: What is a per-invocation environment variable? Give the syntax.**
<details><summary>Answer</summary>

A var set on the same command line as the program — exists ONLY for that one process run and is gone after it exits.

```bash
# Linux/macOS only
MY_NAME="Wade Wilson" python main.py
# → "Wade Wilson" is visible inside main.py
# → After the process exits, MY_NAME is NOT set in the shell
```

Use case: quick one-off overrides without polluting your shell session or committing anything.
</details>

---

**Q: What is the PATH environment variable and how does the OS use it?**
<details><summary>Answer</summary>

`PATH` is a special OS env var that holds an ordered list of directories. When you type a command (like `python`), the OS searches these dirs **left to right** and runs the **first match** found.

- Linux/macOS separator: `:` (colon)
- Windows separator: `;` (semicolon)

The Python installer's "Add Python to PATH?" checkbox appends Python's `bin/` directory to PATH — so `python` can be called from any terminal without typing the full path.
</details>

---

**Q: What are the security best practices for environment variables?**
<details><summary>Answer</summary>

1. **Never commit secrets** — API keys, DB passwords, tokens go in env vars or `.env`, never in code files
2. **Add `.env` to `.gitignore`** — prevents accidental commits
3. **Use `.env.example`** — commit a template with dummy values so teammates know what vars are needed
4. **Prod: use secret managers** — AWS Secrets Manager, GCP Secret Manager, Vault — not `.env` files on servers
5. **Follow 12-Factor App** — [12factor.net/config](https://12factor.net/config): strict separation of config from code

One-liner: "If it changes between environments (dev/staging/prod), it's config — put it in env vars."
</details>

---

**Q: List 3 critical gotchas with environment variables in Python.**
<details><summary>Answer</summary>

1. **`bool("False")` is `True`** — "False" is a non-empty string, always truthy. Use `os.getenv("DEBUG", "false").lower() == "true"` instead.

2. **`export` is required in Bash** — `MY_NAME="Wade"` (no `export`) creates a shell variable, NOT an env var. Child processes like Python won't see it.

3. **Per-invocation syntax is Linux/macOS only** — `KEY=val python script.py` doesn't work on Windows. PowerShell needs `$Env:KEY = "val"` before the command.
</details>

---

## L04 — First Steps

**Q: What is a "path operation" in FastAPI?**
<details><summary>Answer</summary>

A **path operation** = **path** + **operation** combined.

- **Path** = the URL segment after the domain — e.g. `/`, `/items`, `/users/42`
- **Operation** = the HTTP method — GET, POST, PUT, DELETE, etc.

Together they form one handler: `@app.get("/")` means "handle GET requests to /". FastAPI calls the decorated function a **path operation function**.
</details>

---

**Q: What does the `@app.get("/")` decorator do — break it down?**
<details><summary>Answer</summary>

It is a **path operation decorator** that does three things in one line:

1. **Registers** the function as a handler with FastAPI's router
2. **Specifies the path**: `"/"` — the root URL
3. **Specifies the HTTP method**: `get` — only GET requests trigger this function

`app` is the `FastAPI()` instance. `.get` is one of the operation methods. FastAPI reads this decorator and builds its internal routing table automatically.
</details>

---

**Q: What are the 3 parts of a path operation function — name them and explain each.**
<details><summary>Answer</summary>

```python
@app.get("/")           # 1. Path operation decorator
async def root():       # 2. Path operation function (the handler)
    return {...}        # 3. Return value → auto-serialized to JSON
```

1. **Decorator** — tells FastAPI which path + method to bind to
2. **Function** — your actual Python code that runs when the route is hit (`async def` OR `def`)
3. **Return value** — a dict, Pydantic model, list, etc. FastAPI auto-converts it to a JSON response
</details>

---

**Q: What is the `fastapi dev` command and what does it do?**
<details><summary>Answer</summary>

`fastapi dev main.py` starts a **development server** with:
- **Live reload** — code changes auto-restart the server (no manual restart needed)
- **Debug mode** — better error messages
- Runs on `http://127.0.0.1:8000` by default

Alternative: `fastapi dev --entrypoint main:app` (or configure in `pyproject.toml` under `[tool.fastapi]`).

For production: `fastapi deploy` (or run via `uvicorn main:app`).
</details>

---

**Q: What is `/docs` and what UI does it use?**
<details><summary>Answer</summary>

`/docs` is the **interactive API documentation** that FastAPI auto-generates. It uses **Swagger UI** — a browser-based interface where you can:
- Browse all your API endpoints
- See expected inputs/outputs for each route
- **Execute requests live** directly from the browser (no Postman needed)

It is powered by the OpenAPI schema that FastAPI generates automatically from your code.
</details>

---

**Q: What is OpenAPI and why does FastAPI use it?**
<details><summary>Answer</summary>

**OpenAPI** (formerly Swagger) is an **API schema standard** — a specification for describing REST APIs in a machine-readable format (JSON/YAML). It defines paths, HTTP methods, parameters, request bodies, and responses.

FastAPI generates an OpenAPI schema automatically from your code (available at `/openapi.json`). This schema then **powers**:
- `/docs` — Swagger UI interactive docs
- `/redoc` — ReDoc UI docs
- Client SDK generation, testing tools, API gateways

FastAPI uses OpenAPI because: write code once → get docs, validation, and tooling for free.
</details>

---

**Q: Why does FastAPI generate docs automatically — what is it reading?**
<details><summary>Answer</summary>

FastAPI reads your **Python type hints and decorators** to build the OpenAPI schema. Specifically:
- `@app.get("/")` → path + operation
- Function parameter types → parameter definitions
- Return type annotations / Pydantic models → response schema

It uses two schema standards under the hood:
- **OpenAPI** — describes the API (paths, methods, params, responses)
- **JSON Schema** — describes the data shapes (types, required fields, formats)

No separate config file or annotation needed. The type hints ARE the spec.
</details>

---

**Q: What HTTP operations does FastAPI support — list all 8 with their decorators.**
<details><summary>Answer</summary>

| Operation | Decorator | Conventional Use |
|-----------|-----------|-----------------|
| GET | `@app.get()` | Read data |
| POST | `@app.post()` | Create data |
| PUT | `@app.put()` | Update (full replace) |
| DELETE | `@app.delete()` | Delete data |
| PATCH | `@app.patch()` | Update (partial) |
| OPTIONS | `@app.options()` | CORS preflight / metadata |
| HEAD | `@app.head()` | Like GET but no body |
| TRACE | `@app.trace()` | Diagnostic loop-back |

Important: FastAPI does NOT enforce REST semantics — these are conventions only. GraphQL APIs, for example, use POST for everything and that is perfectly valid.
</details>

---

## L05 — ASGI Protocol

**Q: What does ASGI stand for and what is it?**
<details><summary>Answer</summary>

**Async Server Gateway Interface** — a **protocol/contract** (not a library) between an ASGI server and an ASGI application.

It defines one rule: your application must expose `async def app(scope, receive, send)`. That's it. The server calls it; you implement it.
</details>

---

**Q: What are the 3 parameters of the ASGI interface and what does each do?**
<details><summary>Answer</summary>

1. **`scope`** — a dict of request metadata: `type`, `method`, `path`, `headers`, `query_string`. Read-only. Think of it as the envelope.
2. **`receive`** — async callable the app pulls to READ incoming events (request body, WebSocket messages). Pull-based — app calls when ready.
3. **`send`** — async callable the app pushes outgoing events (response headers, response body, WebSocket sends). Must send `http.response.start` BEFORE `http.response.body`.
</details>

---

**Q: What is the correct order of `send()` calls for an HTTP response?**
<details><summary>Answer</summary>

1. First: `await send({"type": "http.response.start", "status": 200, "headers": [...]})`
2. Second: `await send({"type": "http.response.body", "body": b"..."})`

`http.response.start` MUST come before `http.response.body` — same as real HTTP (headers before content). Wrong order = broken response.
</details>

---

**Q: What is Uvicorn and what is the ONE thing it needs from your app?**
<details><summary>Answer</summary>

**Uvicorn** is an ASGI **server** — it handles raw TCP connections, parses HTTP bytes, builds `scope`, creates `receive`/`send` callables, then calls:

```python
await app(scope, receive, send)
```

That's the only thing it needs. It doesn't care if `app` is FastAPI, Django, Starlette, or a hand-rolled function — just needs that callable with those 3 args.
</details>

---

**Q: Why can FastAPI handle WebSockets but WSGI Flask cannot?**
<details><summary>Answer</summary>

**WSGI** (Flask's protocol) is synchronous and one-shot: `def app(environ, start_response)`. Once the response is started, the connection closes. No mechanism to keep reading or writing.

**ASGI** has `receive()` (keep reading events in a loop) and `send()` (keep writing events). WebSockets need both — ASGI's design makes this natural. Flask's WSGI foundation physically cannot support it without bolt-on hacks.
</details>

---

**Q: What are the 3 connection types ASGI supports?**
<details><summary>Answer</summary>

Determined by `scope["type"]`:

1. **`"http"`** — regular HTTP request/response
2. **`"websocket"`** — bidirectional, persistent connection
3. **`"lifespan"`** — app startup/shutdown events

FastAPI handles all three. Always check `scope["type"]` before processing.
</details>

---

**Q: What is Gunicorn's role alongside Uvicorn in production?**
<details><summary>Answer</summary>

**Uvicorn** = the ASGI server (actual request serving, async event loop).
**Gunicorn** = process manager (starts/stops/restarts/health-checks worker processes).

Production command:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```
Gunicorn manages 4 Uvicorn worker processes. Gunicorn = HR manager, Uvicorn = engineer who does the actual work.
</details>

---

**Q: Write a minimal ASGI app that returns "Hello ASGI" to any HTTP request.**
<details><summary>Answer</summary>

```python
async def app(scope, receive, send):
    if scope["type"] != "http":
        return
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [(b"content-type", b"text/plain")]
    })
    await send({
        "type": "http.response.body",
        "body": b"Hello ASGI"
    })
```

Run with: `uvicorn main:app`
</details>

---

## L06 — MiniAPI — Build Your Own Framework

**Q: What makes a Python class an ASGI application?**
<details><summary>Answer</summary>

Adding this method:
```python
async def __call__(self, scope, receive, send):
    ...
```

When Uvicorn does `await app(scope, receive, send)`, Python calls `app.__call__(scope, receive, send)`. Any class with this signature is a valid ASGI app — that's how `FastAPI()`, `Starlette()`, and `MiniAPI()` all work.
</details>

---

**Q: What does `@app.get("/users")` actually do at the Python level?**
<details><summary>Answer</summary>

Two-step decorator call:
1. `app.get("/users")` → called, returns a `decorator` function
2. `decorator(users_handler)` → called, inserts `("GET", "/users") → users_handler` into the routes dict, returns the original function unchanged

Equivalent without `@`:
```python
async def users(): ...
users = app.get("/users")(users)  # register + return
```

`@` is syntactic sugar for "call this function with the decorated function as argument."
</details>

---

**Q: In MiniAPI, what is `Router.resolve()` and how does it work?**
<details><summary>Answer</summary>

`resolve(path, method)` loops through the registered `Route` objects and returns the first one where `route.path == path and route.method == method`. Returns `None` if no match.

```python
def resolve(self, path, method):
    for route in self.routes:
        if route.path == path and route.method == method:
            return route
    return None
```

FastAPI's router does the same — but with regex matching for path params like `/users/{id}`.
</details>

---

**Q: Why does MiniAPI never call `receive()` and when would you need it?**
<details><summary>Answer</summary>

Our MiniAPI only handles GET requests with no body — so we never need to read incoming data. `receive()` is needed for:
- POST/PUT routes that accept a JSON body
- WebSocket connections (loop-read incoming messages)

A real app would do:
```python
message = await receive()  # {"type": "http.request", "body": b"..."}
data = json.loads(message["body"])
```

FastAPI calls `receive()` internally when a route expects a Pydantic body parameter.
</details>

---

**Q: Name 5 things FastAPI adds that MiniAPI doesn't have.**
<details><summary>Answer</summary>

1. **Path parameters** — regex matching for `/users/{id}`
2. **Query parameters** — auto-parse `?page=1&limit=10` from `scope["query_string"]`
3. **Request body + Pydantic validation** — calls `receive()`, deserializes JSON, validates with BaseModel
4. **Dependency Injection** — `Depends()` resolves a dependency graph before calling handler
5. **OpenAPI docs** — auto-generates `/docs` Swagger UI + `/redoc` from type hints
</details>

---

**Q: What is the full layer stack from browser request to FastAPI handler?**
<details><summary>Answer</summary>

```
Browser → HTTP bytes
  ↓
Uvicorn (ASGI server)
  → parses bytes → builds scope → creates receive/send
  → await app(scope, receive, send)
  ↓
Starlette (ASGI framework)
  → middleware chain → routing
  ↓
FastAPI (on top of Starlette)
  → type hint validation (Pydantic) → dependency injection
  ↓
Your handler function
  → returns dict/model
  ↓
FastAPI serializes → JSONResponse.send() → await send(...)
  ↓
Uvicorn writes bytes to socket → Browser receives response
```
</details>


---

## L07 — Query Parameters

**Q: How does FastAPI know if a function param is a path param or a query param?**
<details><summary>Answer</summary>

It checks the parameter name against the path string. If it appears inside `{braces}` → path param. If it's NOT in the path → automatically a query param. Order in the function signature doesn't matter.
</details>

---

**Q: What is the difference between `q: str | None = None` and `q: str`?**
<details><summary>Answer</summary>

- `q: str` → **required** — absent from URL = 422 error
- `q: str | None = None` → **optional** — absent from URL = `q` is `None` inside the function

Both are string type when present. The `| None = None` is the FastAPI signal for "this is optional."
</details>

---

**Q: How do you make a query param required with no default?**
<details><summary>Answer</summary>

Declare it with a type and NO default value:
```python
async def fn(needy: str):  # required
```
If absent from URL → FastAPI auto-returns `422 Unprocessable Entity` with a clear message.
</details>

---

**Q: What string values does FastAPI accept as `True` for a `bool` query param?**
<details><summary>Answer</summary>

Case-insensitive: `1`, `true`, `on`, `yes` — any capitalisation (True, TRUE, On, YES...).

Everything else → `False`. This is smarter than `bool("false")` which Python would evaluate as `True` (non-empty string).
</details>

---

**Q: `q: str | None` without `= None` — is q required or optional?**
<details><summary>Answer</summary>

**Required** — but accepts `None` as a valid value. Without `= None` there's no default, so FastAPI demands it be present in the URL. You need BOTH `| None` (type) AND `= None` (default) to make a param truly optional.
</details>

---

**Q: Write a route with one path param, one required query param, one optional query param with default, and one nullable optional query param.**
<details><summary>Answer</summary>

```python
@app.get("/items/{item_id}")
async def read_item(
    item_id: str,             # path param
    needy: str,               # required query param
    skip: int = 0,            # optional query param, default 0
    limit: int | None = None  # optional, default None
):
    ...
```

Valid URL: `/items/widget?needy=hello&skip=5`
</details>

---

## L08 — Request Body

**Q: How does FastAPI know a function param should come from the request body?**
<details><summary>Answer</summary>

If the param's type is a **Pydantic `BaseModel` subclass**, FastAPI reads it from the JSON request body. The rule:
- Name in `{path}` → path param
- Pydantic model type → body param
- Singular type (`str`, `int`, etc.) not in path → query param
</details>

---

**Q: How do you declare a required vs optional field in a Pydantic model?**
<details><summary>Answer</summary>

- **Required**: no default value — `name: str`
- **Optional**: has a default — `tax: float | None = None` or `skip: int = 0`

Same rule as Python function params. No default = required. Has default = optional.
</details>

---

**Q: What does FastAPI return if a required body field is missing?**
<details><summary>Answer</summary>

`422 Unprocessable Entity` with a detailed JSON error body — automatically, no code needed:
```json
{"detail": [{"type": "missing", "loc": ["body", "name"], "msg": "Field required"}]}
```
Lists every missing/invalid field with location and message.
</details>

---

**Q: What is `model_dump()` and when do you use it?**
<details><summary>Answer</summary>

`model_dump()` converts a Pydantic model instance → plain Python `dict`.

```python
item.model_dump()
# → {"name": "Foo", "price": 45.2, "description": None, "tax": None}
```

Use it for: DB inserts, merging with `**item.model_dump()`, returning modified versions.
</details>

---

**Q: Write the signature for a route that takes a path param, body param, and query param together.**
<details><summary>Answer</summary>

```python
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,           # path — name in {item_id}
    item: Item,             # body — Pydantic BaseModel
    q: str | None = None    # query — singular type, not in path
):
    ...
```

FastAPI detects all three sources from types alone — zero extra config.
</details>

---

**Q: `description: str | None` without `= None` in a Pydantic model — is it required?**
<details><summary>Answer</summary>

**Yes, required** — it accepts `None` as a valid value but the client MUST send the field. To make it truly optional (can be omitted entirely), you need BOTH the union AND the default:

```python
description: str | None = None   # truly optional — can be absent
```
</details>
