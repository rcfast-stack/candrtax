#!/usr/bin/env python3
"""Execute PHP / WP-CLI on WordPress via Novamira MCP."""
import sys, json, requests

MCP_URL = "https://wordpress-1254753-6532124.cloudwaysapps.com/wp-json/mcp/novamira"
AUTH = ("jtoews@consult-smart.com", "YJjCpzthlwizjnPCMMGF9aNO")

def get_session():
    try:
        with open("/tmp/mcp_session.txt") as f:
            return f.read().strip()
    except:
        return None

def init_session():
    r = requests.post(MCP_URL, auth=AUTH, json={
        "jsonrpc": "2.0", "id": 0, "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                   "clientInfo": {"name": "claude", "version": "1.0"}}
    })
    session = r.headers.get("mcp-session-id") or r.headers.get("Mcp-Session-Id")
    with open("/tmp/mcp_session.txt", "w") as f:
        f.write(session)
    return session

def call_ability(ability_name, params, session=None):
    if not session:
        session = get_session() or init_session()
    r = requests.post(MCP_URL, auth=AUTH, headers={"Mcp-Session-Id": session}, json={
        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {"name": "mcp-adapter-execute-ability",
                   "arguments": {"ability_name": ability_name, "parameters": params}}
    })
    d = r.json()
    if "error" in d:
        return {"error": d["error"]}
    content = d["result"]["content"][0]["text"]
    parsed = json.loads(content)
    if isinstance(parsed, dict) and "data" in parsed:
        return parsed["data"]
    return parsed

def execute_php(code, session=None):
    return call_ability("novamira/execute-php", {"code": code}, session)

def run_wpcli(args_list, session=None):
    return call_ability("novamira/run-wp-cli", {"args": args_list}, session)

if __name__ == "__main__":
    code = sys.stdin.read().strip()
    if code.startswith("<?php"):
        code = code[5:].lstrip()
    result = execute_php(code)
    output = result.get("output", "")
    if output:
        print(output, end="")
    rv = result.get("return_value")
    if rv is not None:
        print("\nRETURN:", json.dumps(rv, indent=2))
    if result.get("errors"):
        print("ERRORS:", result["errors"], file=sys.stderr)
