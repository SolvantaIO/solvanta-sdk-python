"""Synchronous and asynchronous Solvanta API clients."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import httpx

from .constants import DEFAULT_BASE_URL
from .errors import SolvantaError
from .types import Dashboard, Service, ServiceCatalog, SolveResponse


def _headers(api_key: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def _raise_for_error(response: httpx.Response) -> None:
    if response.status_code in (200, 201, 202):
        return
    try:
        body = response.json()
        err = body.get("error", {})
        code = err.get("code", "unknown_error")
        message = err.get("message", response.text)
    except Exception:
        code = "unknown_error"
        message = response.text
    raise SolvantaError(code, message, response.status_code)


class Solvanta:
    """Synchronous Solvanta API client.

    Usage::

        client = Solvanta("sk_...")
        result = client.solve("ReCaptchaV3Task", {
            "url": "https://example.com",
            "sitekey": "6Le...",
            "action": "login",
        })
        print(result.result)
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 120.0,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            base_url=self._base_url,
            headers=_headers(api_key),
            timeout=timeout,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Solvanta:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    # ── Solve ─────────────────────────────────────────────────────────

    def solve(
        self,
        task: str,
        payload: Dict[str, Any],
        *,
        idempotency_key: Optional[str] = None,
    ) -> SolveResponse:
        """Create a metered solve and return the result."""
        headers: Dict[str, str] = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        resp = self._client.post(
            "/v1/solve",
            json={"task": task, "payload": payload},
            headers=headers,
        )
        _raise_for_error(resp)
        return SolveResponse.from_dict(resp.json())

    def get_solve(self, solve_id: str) -> SolveResponse:
        """Retrieve an individual solve result by ID."""
        resp = self._client.get(f"/v1/solves/{solve_id}")
        _raise_for_error(resp)
        return SolveResponse.from_dict(resp.json())

    def list_solves(self, *, limit: int = 20) -> List[SolveResponse]:
        """List recent solve history."""
        resp = self._client.get("/v1/solves", params={"limit": limit})
        _raise_for_error(resp)
        return [SolveResponse.from_dict(s) for s in resp.json()]

    # ── Discovery ─────────────────────────────────────────────────────

    def services(self) -> ServiceCatalog:
        """Discover registered solver tasks and readiness."""
        resp = self._client.get("/v1/solver/services")
        _raise_for_error(resp)
        return ServiceCatalog.from_dict(resp.json())

    def dashboard(self) -> Dashboard:
        """Read workspace overview and balance."""
        resp = self._client.get("/v1/dashboard")
        _raise_for_error(resp)
        return Dashboard.from_dict(resp.json())


class AsyncSolvanta:
    """Asynchronous Solvanta API client.

    Usage::

        async with AsyncSolvanta("sk_...") as client:
            result = await client.solve("CloudflareTask", {
                "url": "https://example.com",
            })
            print(result.result)
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 120.0,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            headers=_headers(api_key),
            timeout=timeout,
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncSolvanta:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    # ── Solve ─────────────────────────────────────────────────────────

    async def solve(
        self,
        task: str,
        payload: Dict[str, Any],
        *,
        idempotency_key: Optional[str] = None,
    ) -> SolveResponse:
        """Create a metered solve and return the result."""
        headers: Dict[str, str] = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        resp = await self._client.post(
            "/v1/solve",
            json={"task": task, "payload": payload},
            headers=headers,
        )
        _raise_for_error(resp)
        return SolveResponse.from_dict(resp.json())

    async def get_solve(self, solve_id: str) -> SolveResponse:
        """Retrieve an individual solve result by ID."""
        resp = await self._client.get(f"/v1/solves/{solve_id}")
        _raise_for_error(resp)
        return SolveResponse.from_dict(resp.json())

    async def list_solves(self, *, limit: int = 20) -> List[SolveResponse]:
        """List recent solve history."""
        resp = await self._client.get("/v1/solves", params={"limit": limit})
        _raise_for_error(resp)
        return [SolveResponse.from_dict(s) for s in resp.json()]

    # ── Discovery ─────────────────────────────────────────────────────

    async def services(self) -> ServiceCatalog:
        """Discover registered solver tasks and readiness."""
        resp = await self._client.get("/v1/solver/services")
        _raise_for_error(resp)
        return ServiceCatalog.from_dict(resp.json())

    async def dashboard(self) -> Dashboard:
        """Read workspace overview and balance."""
        resp = await self._client.get("/v1/dashboard")
        _raise_for_error(resp)
        return Dashboard.from_dict(resp.json())
