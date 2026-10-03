# Solvanta Python SDK

Official Python SDK for the [Solvanta](https://solvanta.dev) solver API. Supports both synchronous and asynchronous usage.

## Install

```bash
pip install solvanta
```

## Quick Start

```python
from solvanta import Solvanta, RECAPTCHA_V3

client = Solvanta("sk_...")

result = client.solve(RECAPTCHA_V3, {
    "url": "https://example.com",
    "sitekey": "6Le...",
    "action": "login",
})

print(result.id)           # solve UUID
print(result.result)       # {"token": "03A..."}
print(result.credits_used) # credits charged
```

## Usage

### Create a Client

```python
from solvanta import Solvanta

# Default settings
client = Solvanta("sk_...")

# Custom options
client = Solvanta("sk_...", base_url="https://custom.endpoint.com", timeout=60.0)

# Context manager (auto-closes connection)
with Solvanta("sk_...") as client:
    result = client.solve(...)
```

### Solve

```python
from solvanta import RECAPTCHA_V2, CLOUDFLARE, ARKOSE

# ReCaptcha V2
result = client.solve(RECAPTCHA_V2, {
    "url": "https://example.com",
    "sitekey": "6Le...",
    "invisible": False,
})

# Cloudflare
result = client.solve(CLOUDFLARE, {
    "url": "https://example.com",
    "proxy": "http://user:pass@host:port",
})

# Arkose / FunCaptcha
result = client.solve(ARKOSE, {
    "url": "https://example.com",
    "sitekey": "pk_...",
})

# With idempotency key
result = client.solve(RECAPTCHA_V3, {
    "url": "https://example.com",
    "sitekey": "6Le...",
}, idempotency_key="req_abc123")
```

### Retrieve a Solve

```python
solve = client.get_solve("uuid-here")
print(solve.status)  # "solved" | "processing" | "failed"
```

### List Solve History

```python
solves = client.list_solves(limit=50)
for s in solves:
    print(s.id, s.status, s.credits_used)
```

### Discover Services

```python
catalog = client.services()
for svc in catalog.services:
    print(f"{svc.task} — {svc.credits} credits — {'ready' if svc.configured else 'offline'}")
```

### Dashboard

```python
dash = client.dashboard()
print(dash.data)
```

## Async Client

```python
import asyncio
from solvanta import AsyncSolvanta, CLOUDFLARE

async def main():
    async with AsyncSolvanta("sk_...") as client:
        result = await client.solve(CLOUDFLARE, {
            "url": "https://example.com",
            "proxy": "http://user:pass@host:port",
        })
        print(result.result)

asyncio.run(main())
```

All methods on `AsyncSolvanta` mirror `Solvanta` but return coroutines.

## Task Constants

| Constant | Task Name |
|----------|-----------|
| `RECAPTCHA_V2` | ReCaptchaV2Task |
| `RECAPTCHA_V2_ENTERPRISE` | ReCaptchaV2EnterpriseTask |
| `RECAPTCHA_V3` | ReCaptchaV3Task |
| `RECAPTCHA_V3_ENTERPRISE` | ReCaptchaV3EnterpriseTask |
| `CLOUDFLARE` | CloudflareTask |
| `ARKOSE` | ArkoseTask |
| `FORTER` | ForterTask |
| `NUDATA` | NuDataTask |
| `THREATMETRIX` | ThreatMetrixTask |
| `UE_MSM` | UeMsmTask |
| `METADATA1` | Metadata1Task |

## Error Handling

```python
from solvanta import Solvanta, SolvantaError

client = Solvanta("sk_...")

try:
    client.solve("ReCaptchaV3Task", {"url": "...", "sitekey": "..."})
except SolvantaError as e:
    print(e.code)        # "insufficient_credits"
    print(e.message)     # human-readable message
    print(e.status_code) # 402
```

## Requirements

- Python 3.9+
- httpx (installed automatically)
