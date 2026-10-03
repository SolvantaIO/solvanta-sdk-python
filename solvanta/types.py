"""Request and response types for the Solvanta API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SolveResponse:
    """Result of a POST /v1/solve request."""

    id: str
    status: str
    result: Optional[Dict[str, Any]]
    credits_used: int
    balance: Optional[int]
    elapsed_ms: int

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> SolveResponse:
        return SolveResponse(
            id=data.get("id", ""),
            status=data.get("status", ""),
            result=data.get("result"),
            credits_used=data.get("credits_used", 0),
            balance=data.get("balance"),
            elapsed_ms=data.get("elapsed_ms", 0),
        )


@dataclass
class Service:
    """A registered solver from GET /v1/solver/services."""

    task: str
    name: str
    family: str
    platform: str
    description: str
    capabilities: List[str]
    credits: int
    native: bool
    configured: bool

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Service:
        return Service(
            task=data.get("task", ""),
            name=data.get("name", ""),
            family=data.get("family", ""),
            platform=data.get("platform", ""),
            description=data.get("description", ""),
            capabilities=data.get("capabilities", []),
            credits=data.get("credits", 0),
            native=data.get("native", False),
            configured=data.get("configured", False),
        )


@dataclass
class ServiceCatalog:
    """Full solver catalog from GET /v1/solver/services."""

    services: List[Service]
    worker_reachable: bool

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> ServiceCatalog:
        return ServiceCatalog(
            services=[Service.from_dict(s) for s in data.get("services", [])],
            worker_reachable=data.get("worker_reachable", False),
        )


@dataclass
class Dashboard:
    """Workspace overview from GET /v1/dashboard."""

    data: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Dashboard:
        return Dashboard(data=data)
