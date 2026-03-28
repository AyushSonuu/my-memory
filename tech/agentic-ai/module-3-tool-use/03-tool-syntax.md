# 03 · Tool Syntax (JSON Schema) 🔤

---

## 🎯 One Line
> Behind the scenes, tools are described to LLMs via **JSON Schema** — aisuite generates this automatically from your function's name, docstring, and parameters. Understanding the schema helps you write better tool descriptions.

---

> ℹ️ **This lesson's content was covered alongside Lesson 02.** See [Creating a Tool](02-creating-a-tool.md) for the full walkthrough including the JSON schema deep-dive, aisuite auto-generation, docstring best practices, and the `max_turns` parameter.

## Quick Reference: The Two Schemas

### Simple (no params)

```
  def get_current_time():                    {
      """Returns the current                   "type": "function",
      time as a string"""           ──▶        "function": {
      return datetime.now()                      "name": "get_current_time",
          .strftime("%H:%M:%S")                  "description": "Returns the
                                                   current time as a string",
                                                 "parameters": {}
                                               }
                                             }
```

### With parameters

```
  def get_current_time(timezone):            {
      """Returns current time                  "type": "function",
      for the given time zone"""    ──▶        "function": {
      tz = ZoneInfo(timezone)                    "name": "get_current_time",
      return datetime.now(tz)                    "description": "Returns current
          .strftime("%H:%M:%S")                    time for the given time zone",
                                                 "parameters": {
                                                   "timezone": {
                                                     "type": "string",
                                                     "description": "IANA time zone
                                                       e.g. 'America/New_York'"
                                                   }
                                                 }
                                               }
                                             }
```

### Key Mapping

| Your Code | JSON Schema Field | What LLM Sees |
|-----------|------------------|---------------|
| `def function_name` | `"name"` | What to call this tool |
| `"""docstring"""` | `"description"` | When/why to use it |
| Function params | `"parameters"` | What arguments to pass |
| Type hints + docstring | `"type"` + `"description"` per param | Format of each argument |

---

> **← Prev** [Creating a Tool](02-creating-a-tool.md) · **Next →** [Code Execution](04-code-execution.md)
