#!/usr/bin/env python3
"""Minimal MCP JSON-RPC bridge for the NOESIS control plane."""

from __future__ import annotations

import json
import sys

from noesis_control_plane import build_checkpoint

TOOLS = {
    "get_noesis_checkpoint": {
        "description": "Build a deterministic NOESIS-QCAL control-plane checkpoint.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    "validate_noesis_control_plane": {
        "description": "Validate QCAL node contracts, registry integrity and epistemic state.",
        "inputSchema": {"type": "object", "properties": {}},
    },
}


def result(payload: dict) -> dict:
    return {"content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}]}


def handle(request: dict):
    request_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    def ok(value):
        return {"jsonrpc": "2.0", "id": request_id, "result": value}

    def error(code, message):
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}

    if method == "initialize":
        return ok({
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "noesis-control-plane", "version": "1.0.0"},
        })
    if method == "tools/list":
        return ok({"tools": [{"name": name, **spec} for name, spec in TOOLS.items()]})
    if method == "tools/call":
        name = params.get("name")
        if name in TOOLS:
            return ok(result(build_checkpoint()))
        return ok({"isError": True, "content": [{"type": "text", "text": f"Unknown tool: {name}"}]})
    if request_id is None:
        return None
    return error(-32601, f"Method not found: {method!r}")


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = handle(request)
        except Exception as exc:
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(exc)}}
        if response is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
