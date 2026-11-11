#!/usr/bin/env python3
"""
Web Server & REST API for IBD Prerequisite Studio (DCC222 / DCC011 - UFMG).
Zero external dependencies — runs with standard Python 3.
Supports:
- Mode 'structured': Conceptual, ER/EER, (min,max), RIR (b,p,n) and RA Structural Constraint validation
- Mode 'sql_query': Live SQL / RA query execution & expected output comparison
- Mode 'sql_ddl': Live DDL execution + Fault-Injection Test Suite (PK, UNIQUE, CHECK, ON DELETE CASCADE/RESTRICT)
- Mode 'sql_assertion': SQL-92 CREATE ASSERTION transpilation & Fault-Injection Validation
"""

import os
import sys
import json
import time
import sqlite3
import http.server
import socketserver
from typing import Any, Dict
from db_engine import (
    EXERCISES_DATA,
    get_connection,
    validate_structured,
    validate_ddl,
    validate_assertion,
    extract_assertion_subqueries,
)

PORT = int(os.environ.get("PORT", 8080))
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class PrerequisiteStudioHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format: str, *args: Any) -> None:
        # Clean console logs
        pass

    def do_GET(self):
        if self.path == "/api/exercises":
            self.send_json_response(self.get_exercises_summary())
        elif self.path.startswith("/api/exercise/"):
            try:
                ex_id = self.path.split("/")[-1]
                self.send_json_response(self.get_exercise_details(ex_id))
            except Exception as e:
                self.send_json_response({"error": str(e)}, status=400)
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            data = json.loads(body)
        except Exception as e:
            self.send_json_response({"error": f"JSON inválido: {e}"}, status=400)
            return

        if self.path == "/api/execute":
            ex_id = str(data.get("exerciseId", "T5.1"))
            query = data.get("query", "")
            self.send_json_response(self.execute_workspace(ex_id, query))
        elif self.path == "/api/validate":
            ex_id = str(data.get("exerciseId", "T1.1"))
            self.send_json_response(self.validate_workspace(ex_id, data))
        else:
            self.send_json_response({"error": "Endpoint não encontrado"}, status=404)

    def send_json_response(self, data: Any, status: int = 200):
        response_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def get_exercises_summary(self):
        summary = []
        for ex_id, info in EXERCISES_DATA.items():
            summary.append({
                "id": ex_id,
                "title": info["title"],
                "type": info.get("type", "oficial"),
                "mode": info.get("mode", "structured"),
            })
        return summary

    def get_exercise_details(self, ex_id: str) -> Dict[str, Any]:
        if ex_id not in EXERCISES_DATA:
            return {"error": f"Exercício '{ex_id}' não encontrado."}

        info = EXERCISES_DATA[ex_id]
        mode = info.get("mode", "structured")
        schema_tables = {}

        if info.get("setup"):
            conn = get_connection(ex_id)
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [r[0] for r in cur.fetchall()]
            for t in tables:
                cur.execute(f"PRAGMA table_info({t});")
                cols = [
                    {"cid": c[0], "name": c[1], "type": c[2], "notnull": c[3], "pk": c[5]}
                    for c in cur.fetchall()
                ]
                cur.execute(f"SELECT * FROM {t};")
                sample_rows = [list(r) for r in cur.fetchall()]
                schema_tables[t] = {"columns": cols, "rows": sample_rows}

        return {
            "id": ex_id,
            "title": info["title"],
            "type": info.get("type", "oficial"),
            "mode": mode,
            "fields": info.get("fields", []),
            "expectedColumns": info.get("expected_columns", []),
            "expectedRows": info.get("expected_rows", []),
            "ddlTests": [t["name"] for t in info.get("ddl_tests", [])],
            "assertionTests": [t["name"] for t in info.get("assertion_tests", [])],
            "tables": schema_tables,
        }

    def execute_workspace(self, ex_id: str, query: str) -> Dict[str, Any]:
        if ex_id not in EXERCISES_DATA:
            return {"success": False, "error": "Exercício inválido."}

        info = EXERCISES_DATA[ex_id]
        mode = info.get("mode", "sql_query")
        if not query.strip():
            return {"success": False, "error": "O editor está vazio."}

        start = time.time()
        try:
            conn = get_connection(ex_id)
            cur = conn.cursor()

            if mode == "sql_ddl":
                conn.executescript(query)
                cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
                created = cur.fetchall()
                elapsed_ms = round((time.time() - start) * 1000, 2)
                return {
                    "success": True,
                    "columns": ["Tabela Criada", "Definição DDL no Catálogo SQLite"],
                    "rows": [[r[0], r[1]] for r in created],
                    "rowCount": len(created),
                    "elapsedMs": elapsed_ms,
                }

            elif mode == "sql_assertion":
                assertions = extract_assertion_subqueries(query)
                rows_out = []
                for name, subq in assertions:
                    cur.execute(subq)
                    v_rows = cur.fetchall()
                    status_str = "OK (0 violações no estado base)" if len(v_rows) == 0 else f"VIOLADA ({len(v_rows)} tuplas)"
                    rows_out.append([name, status_str, subq])
                elapsed_ms = round((time.time() - start) * 1000, 2)
                return {
                    "success": True,
                    "columns": ["Asserção", "Estado Atual do BD", "Subconsulta de Violação (NOT EXISTS)"],
                    "rows": rows_out,
                    "rowCount": len(rows_out),
                    "elapsedMs": elapsed_ms,
                }

            else:
                cur.execute(query)
                rows = [list(r) for r in cur.fetchall()]
                cols = [desc[0] for desc in cur.description] if cur.description else []
                elapsed_ms = round((time.time() - start) * 1000, 2)
                return {
                    "success": True,
                    "columns": cols,
                    "rows": rows,
                    "rowCount": len(rows),
                    "elapsedMs": elapsed_ms,
                }
        except Exception as e:
            elapsed_ms = round((time.time() - start) * 1000, 2)
            return {"success": False, "error": str(e), "elapsedMs": elapsed_ms}

    def validate_workspace(self, ex_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if ex_id not in EXERCISES_DATA:
            return {"matched": False, "error": f"Exercício '{ex_id}' não encontrado."}

        info = EXERCISES_DATA[ex_id]
        mode = info.get("mode", "structured")

        if mode == "structured":
            answers = data.get("answers", {})
            return validate_structured(ex_id, answers)

        elif mode == "sql_ddl":
            query = data.get("query", "")
            return validate_ddl(ex_id, query)

        elif mode == "sql_assertion":
            query = data.get("query", "")
            return validate_assertion(ex_id, query)

        else:
            # sql_query mode
            query = data.get("query", "")
            exec_res = self.execute_workspace(ex_id, query)
            if not exec_res["success"]:
                return {
                    "matched": False,
                    "mode": "sql_query",
                    "error": exec_res["error"],
                    "execResult": exec_res,
                }

            expected_cols = info["expected_columns"]
            expected_rows = info["expected_rows"]
            actual_cols = exec_res["columns"]
            actual_rows = exec_res["rows"]

            matched = True
            diff_reason = ""

            norm_actual_cols = [c.strip().lower() for c in actual_cols]
            norm_expected_cols = [c.strip().lower() for c in expected_cols]

            if norm_actual_cols != norm_expected_cols:
                matched = False
                diff_reason = f"Colunas divergentes. Esperado: {expected_cols}, Obtido: {actual_cols}."
            elif len(actual_rows) != len(expected_rows):
                matched = False
                diff_reason = f"Quantidade de tuplas diferente. Esperado: {len(expected_rows)}, Obtido: {len(actual_rows)}."
            else:
                # Order-insensitive comparison unless ORDER BY is explicitly required
                def norm_row(r):
                    out = []
                    for val in r:
                        try:
                            out.append(str(round(float(val), 2)))
                        except (ValueError, TypeError):
                            out.append(str(val).strip().lower())
                    return tuple(out)

                if sorted(norm_row(r) for r in actual_rows) != sorted(norm_row(r) for r in expected_rows):
                    matched = False
                    diff_reason = "Os valores das tuplas retornadas diferem do gabarito esperado."

            return {
                "matched": matched,
                "mode": "sql_query",
                "diffReason": "Sucesso! Resultado 100% equivalente ao esperado." if matched else diff_reason,
                "execResult": exec_res,
                "expectedColumns": expected_cols,
                "expectedRows": expected_rows,
            }


def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), PrerequisiteStudioHandler) as httpd:
        print(f"🚀 IBD Prerequisite Studio rodando em http://localhost:{PORT}")
        sys.stdout.flush()
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()

