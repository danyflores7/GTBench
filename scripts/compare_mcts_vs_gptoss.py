#!/usr/bin/env python3
"""
Compara MCTS vs GPT-OSS-120B (NVIDIA) en múltiples juegos usando archivos .jsonl de GTBench.

Notas de parsing:
- Algunos archivos llamados ".jsonl" contienen JSON multi-línea y/o basura suelta (p. ej.,
    líneas "Normal"). El loader es tolerante: extrae cada objeto JSON balanceando llaves y
    omite texto ajeno.

Definición de conteo:
- Se cuentan todas las partidas con status == "Normal".
- Ganador por bando:
    * MCTS si winner empieza con "MCTSAgent".
    * LLM si winner termina con f"_{llm_tag}" y no empieza con "MCTSAgent".
    * Empate si winner está vacío/Draw/Tie o winner_score == 0.
    * Si no se puede clasificar, se incrementa "unclassified".
"""

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

def _iter_json_objects(text: str):
    """Yield JSON object strings by scanning braces; ignore text outside objects."""
    in_str = False
    escape = False
    depth = 0
    start = None
    for i, ch in enumerate(text):
        if in_str:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
            continue
        if ch == '{':
            if depth == 0:
                start = i
            depth += 1
            continue
        if ch == '}':
            depth -= 1
            if depth == 0 and start is not None:
                yield text[start:i + 1]
                start = None


def load_jsonl(path: Path) -> List[dict]:
    """Tolerant loader: soporta JSONL, JSON multi-línea concatenado y basura suelta."""
    raw = path.read_text(encoding="utf-8", errors="ignore")
    # filtrar líneas claramente no JSON (vacías, "Normal", comentarios)
    filtered = "\n".join(
        ln for ln in raw.splitlines()
        if (s := ln.strip()) and s != "Normal" and not s.startswith("//")
    )
    items: List[dict] = []
    # camino rápido: parse línea a línea si parecen objetos cerrados
    any_parsed = False
    for ln in filtered.splitlines():
        s = ln.strip()
        if s.startswith("{") and s.endswith("}"):
            try:
                items.append(json.loads(s))
                any_parsed = True
            except Exception:
                pass
    # si no se logró parsear nada, usar escaneo por llaves
    if not any_parsed:
        for obj_s in _iter_json_objects(filtered):
            try:
                items.append(json.loads(obj_s))
            except Exception:
                pass
    return items


def collect_files(paths: List[str]) -> List[Path]:
    files: List[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            files.extend(sorted(path.rglob("*.jsonl")))
        elif path.suffix == ".jsonl" and path.exists():
            files.append(path)
    # de-dup
    files = sorted(list(dict.fromkeys(files)))
    return files


def analyze(items: List[dict], llm_tag: str = "gpt-oss-120b") -> Dict:
    per_game = defaultdict(
        lambda: {
            "normal": 0,
            "abnormal": 0,
            "mcts_wins": 0,
            "gpt_wins": 0,
            "draws": 0,
            "unclassified": 0,
        }
    )

    totals = {
        "normal": 0,
        "abnormal": 0,
        "mcts_wins": 0,
        "gpt_wins": 0,
        "draws": 0,
        "unclassified": 0,
    }

    for hist in items:
        game = hist.get("game_config", {}).get("game_name", "unknown")
        matches = hist.get("matches", [])

        for m in matches:
            status = m.get("status")
            if status != "Normal":
                per_game[game]["abnormal"] += 1
                totals["abnormal"] += 1
                continue

            # Contar siempre los Normal
            per_game[game]["normal"] += 1
            totals["normal"] += 1

            winner = (m.get("winner") or "").strip()
            winner_score = m.get("winner_score", None)

            # Empate
            if not winner or winner.lower() in {"draw", "tie"} or winner_score == 0:
                per_game[game]["draws"] += 1
                totals["draws"] += 1
                continue

            # Clasificación por string del ganador
            if winner.startswith("MCTSAgent"):
                per_game[game]["mcts_wins"] += 1
                totals["mcts_wins"] += 1
            elif winner.endswith(f"_{llm_tag}") and not winner.startswith("MCTSAgent"):
                per_game[game]["gpt_wins"] += 1
                totals["gpt_wins"] += 1
            else:
                per_game[game]["unclassified"] += 1
                totals["unclassified"] += 1

    # calcular winrates por juego
    result_per_game = {}
    for game, stats in per_game.items():
        n = max(1, stats["normal"])  # evitar div cero; si 0 normales, winrates serán 0.0
        result_per_game[game] = {
            **{k: v for k, v in stats.items() if k in [
                "normal", "abnormal", "mcts_wins", "gpt_wins", "draws", "unclassified"
            ]},
            "mcts_winrate": stats["mcts_wins"] / n,
            "gpt_winrate": stats["gpt_wins"] / n,
            "draw_rate": stats["draws"] / n,
            "better": (
                "MCTS"
                if stats["mcts_wins"] > stats["gpt_wins"]
                else ("GPT-OSS-120B" if stats["gpt_wins"] > stats["mcts_wins"] else "Tie")
            ),
        }

    n_all = max(1, totals["normal"])  # evitar div cero
    overall = {
        **totals,
        "mcts_winrate": totals["mcts_wins"] / n_all,
        "gpt_winrate": totals["gpt_wins"] / n_all,
        "draw_rate": totals["draws"] / n_all,
        "better": (
            "MCTS"
            if totals["mcts_wins"] > totals["gpt_wins"]
            else ("GPT-OSS-120B" if totals["gpt_wins"] > totals["mcts_wins"] else "Tie")
        ),
    }

    return {"per_game": result_per_game, "overall": overall}


def save_csv(per_game: Dict, csv_path: Path) -> None:
    fieldnames = [
        "game", "normal", "abnormal", "mcts_wins", "gpt_wins", "draws",
        "unclassified", "mcts_winrate", "gpt_winrate", "draw_rate", "better",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for game, row in sorted(per_game.items()):
            writer.writerow({"game": game, **row})


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Comparar MCTS vs GPT-OSS-120B en resultados GTBench (.jsonl)"
        )
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help=(
            "Rutas a .jsonl o carpetas con .jsonl "
            "(ej. experiments/test-gptoss)"
        ),
    )
    parser.add_argument(
        "--llm-tag",
        default="gpt-oss-120b",
        help=(
            "Sufijo de modelo para identificar el lado LLM "
            "(por defecto: gpt-oss-120b)"
        ),
    )
    parser.add_argument(
        "--save",
        type=str,
        help="Ruta para guardar el resumen en JSON",
    )
    parser.add_argument(
        "--save-csv",
        type=str,
        help="Ruta para guardar per_game en CSV",
    )
    args = parser.parse_args()

    files = collect_files(args.paths)
    items: List[dict] = []
    for fp in files:
        items.extend(load_jsonl(fp))

    summary = analyze(items, llm_tag=args.llm_tag)
    out = json.dumps(summary, indent=2)
    print(out)

    if args.save:
        Path(args.save).write_text(out, encoding="utf-8")
    if args.save_csv:
        save_csv(summary["per_game"], Path(args.save_csv))


if __name__ == "__main__":
    main()
