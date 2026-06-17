# 🃏 FastAPI Flashcards

> Pull from: L01 Python Types Intro · L02 Concurrency &amp; Async/Await · L03 Environment Variables · L04 First Steps

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
