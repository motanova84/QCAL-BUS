#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from urllib import request as urlrequest

ROOT_DIR = Path(__file__).resolve().parents[1]


def build_payloads(tail: int) -> list[dict]:
    return [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "get_mesh_state", "arguments": {}},
        },
        {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {"name": "get_node_catalog", "arguments": {}},
        },
        {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {"name": "get_emissions_log", "arguments": {"tail": tail}},
        },
    ]


def validate_payload(response: dict, request_id: int) -> None:
    if response.get("id") != request_id:
        raise RuntimeError(f"Respuesta MCP fuera de secuencia: {response}")
    if "error" in response:
        raise RuntimeError(f"Error MCP: {response['error']}")


def run_stdio_validation(tail: int) -> list[dict]:
    payload = "\n".join(json.dumps(item) for item in build_payloads(tail)) + "\n"
    result = subprocess.run(
        [sys.executable, str(ROOT_DIR / "qcal_mesh_sync.py"), "--mcp-server"],
        input=payload,
        text=True,
        capture_output=True,
        check=True,
    )
    responses = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    for index, response in enumerate(responses, start=1):
        validate_payload(response, index)
    return responses


def run_http_validation(url: str, tail: int) -> list[dict]:
    responses = []
    for payload in build_payloads(tail):
        req = urlrequest.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlrequest.urlopen(req) as resp:
            responses.append(json.loads(resp.read().decode("utf-8")))
    for index, response in enumerate(responses, start=1):
        validate_payload(response, index)
    return responses


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="mcp_client_test",
        description="Valida el bridge MCP de QCAL-BUS por stdio u HTTP JSON-RPC.",
    )
    parser.add_argument(
        "--transport",
        choices=("stdio", "http"),
        default="stdio",
        help="Transporte MCP a validar.",
    )
    parser.add_argument(
        "--url",
        default="http://localhost:5000/api/mcp",
        help="URL del bridge HTTP MCP.",
    )
    parser.add_argument(
        "--tail",
        type=int,
        default=3,
        help="Entradas del ledger a solicitar en get_emissions_log.",
    )
    args = parser.parse_args()

    if args.transport == "stdio":
        responses = run_stdio_validation(args.tail)
    else:
        responses = run_http_validation(args.url, args.tail)

    mesh_state = json.loads(responses[2]["result"]["content"][0]["text"])
    catalog = json.loads(responses[3]["result"]["content"][0]["text"])
    emissions = json.loads(responses[4]["result"]["content"][0]["text"])

    print("MCP validation OK")
    print(f"  Ψ_GLOBAL: {mesh_state.get('global_psi', 0.0):.8f}")
    print(f"  Nodos: {len(catalog.get('nodes', {}))}")
    print(f"  Emisiones consultadas: {len(emissions)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
