#!/usr/bin/env python3
"""
Compara MCTS vs GPT-5 a través de múltiples juegos usando los archivos .jsonl generados por GTBench.

Definición de lados:
- Lado MCTS: participante cuyo nombre de agente empieza con 'MCTSAgent_'.
- Lado GPT-5: cualquier participante cuyo nombre termine en '_gpt-5' y NO sea MCTS.

Para cada partida Normal se cuentan victorias/derrotas/empates por juego y totales.
Las partidas Abnormal se reportan como métricas informativas (no cuentan en W/L/D).
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List


def load_jsonl(path: Path) -> List[dict]:
    items = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                continue
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


def analyze(items: List[dict], llm_tag: str = "gpt-5") -> Dict:
    per_game = defaultdict(lambda: {
        "normal": 0,
        "abnormal": 0,
        "mcts_wins": 0,
        "gpt5_wins": 0,
        "draws": 0,
        "files": set(),
    })

    totals = {
        "normal": 0,
        "abnormal": 0,
        "mcts_wins": 0,
        "gpt5_wins": 0,
        "draws": 0,
    }

    for hist in items:
        game = hist.get("game_config", {}).get("game_name", "unknown")
        matches = hist.get("matches", [])

        for m in matches:
            status = m.get("status")
            # obtener participantes como agent_model
            participants = []
            for s in m.get("steps", []):
                agent = s.get("agent", "")
                model = s.get("model_name", "")
                if agent and model:
                    key = f"{agent}_{model}"
                    if key not in participants:
                        participants.append(key)

            # identificar lados
            mcts_side = [p for p in participants if p.startswith("MCTSAgent_")]
            gpt_side = [
                p for p in participants
                if p.endswith(f"_{llm_tag}") and not p.startswith("MCTSAgent_")
            ]

            if status != "Normal":
                per_game[game]["abnormal"] += 1
                totals["abnormal"] += 1
                continue

            # solo contamos partidas normales donde hay MCTS y algún GPT-5
            if not mcts_side or not gpt_side:
                continue

            per_game[game]["normal"] += 1
            totals["normal"] += 1

            winner = m.get("winner", "")
            if winner in mcts_side:
                per_game[game]["mcts_wins"] += 1
                totals["mcts_wins"] += 1
            elif winner in gpt_side:
                per_game[game]["gpt5_wins"] += 1
                totals["gpt5_wins"] += 1
            else:
                per_game[game]["draws"] += 1
                totals["draws"] += 1

    # calcular winrates por juego
    result_per_game = {}
    for game, stats in per_game.items():
        n = max(1, stats["normal"])  # evitar div cero; si 0 normales, winrates serán 0.0
        result_per_game[game] = {
            **{
                k: v for k, v in stats.items()
                if k in ["normal", "abnormal", "mcts_wins", "gpt5_wins", "draws"]
            },
            "mcts_winrate": stats["mcts_wins"] / n,
            "gpt5_winrate": stats["gpt5_wins"] / n,
            "draw_rate": stats["draws"] / n,
            "better": (
                "MCTS" if stats["mcts_wins"] > stats["gpt5_wins"]
                else ("GPT-5" if stats["gpt5_wins"] > stats["mcts_wins"] else "Tie")
            ),
        }

    n_all = max(1, totals["normal"])  # evitar div cero
    overall = {
        **totals,
        "mcts_winrate": totals["mcts_wins"] / n_all,
        "gpt5_winrate": totals["gpt5_wins"] / n_all,
        "draw_rate": totals["draws"] / n_all,
        "better": (
            "MCTS" if totals["mcts_wins"] > totals["gpt5_wins"]
            else ("GPT-5" if totals["gpt5_wins"] > totals["mcts_wins"] else "Tie")
        ),
    }

    return {"per_game": result_per_game, "overall": overall}


def main():
    parser = argparse.ArgumentParser(
        description="Comparar MCTS vs GPT-5 en resultados GTBench (.jsonl)"
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="Rutas a .jsonl o carpetas con .jsonl (ej. experiments/test-gpt5)",
    )
    parser.add_argument(
        "--llm-tag",
        default="gpt-5",
        help="Sufijo de modelo para identificar el lado LLM (por defecto: gpt-5)",
    )
    parser.add_argument("--save", type=str, help="Ruta para guardar el resumen en JSON")
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


if __name__ == "__main__":
    main()
