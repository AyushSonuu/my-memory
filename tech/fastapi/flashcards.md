# 🃏 FastAPI Flashcards

> Pull from: L01 Python Types Intro

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
