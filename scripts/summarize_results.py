#!/usr/bin/env python3
"""
GTBench results summarizer.

Features:
- Aggregate across one or many .jsonl files.
- Report total histories, matches normales/abnormales, draws, winners.
- Per agent_model (e.g., PromptAgent_gpt-5): wins, losses, draws.
- Optional per-match listing with sequence of moves.
"""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def load_jsonl(path: Path):
    """Load all JSON objects from a JSONL file."""
    items = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                # skip bad lines
                continue
    return items


def summarize(items, per_match=False):
    """Summarize a list of history_tracker dicts.

    If per_match=True, include a compact listing of matches with move sequences.
    """
    total_runs = len(items)
    games = Counter()
    normal_matches = 0
    abnormal_matches = 0
    draw_matches = 0
    tokens_total = 0
    winners = Counter()
    agents_fault = Counter()
    
    # Time tracking
    total_duration = 0
    match_durations = []

    # win rates aggregated across histories
    win_rates_acc = defaultdict(list)

    # per agent_model W/L/D
    wld = defaultdict(lambda: {"wins": 0, "losses": 0, "draws": 0})

    # optional detailed matches
    match_details = []

    for hist in items:
        game = hist.get("game_config", {}).get("game_name", "unknown")
        games[game] += 1
        tokens_total += hist.get("token_size", 0)

        # accumulate win rates
        for agent, rate in hist.get("win_rate", {}).items():
            win_rates_acc[agent].append(rate)

        for match_index, m in enumerate(hist.get("matches", [])):
            # Track duration if available
            duration = m.get("duration_seconds", 0)
            if duration > 0:
                total_duration += duration
                match_durations.append(duration)
            
            # participants as agent_model from steps
            participants = []
            for s in m.get("steps", []):
                agent = s.get("agent", "")
                model = s.get("model_name", "")
                if agent and model:
                    key = f"{agent}_{model}"
                    if key not in participants:
                        participants.append(key)

            if m.get("status") == "Normal":
                normal_matches += 1
                winner = m.get("winner", "")
                if winner:
                    winners[winner] += 1
                    # mark W/L
                    wld[winner]["wins"] += 1
                    for p in participants:
                        if p != winner:
                            wld[p]["losses"] += 1
                else:
                    draw_matches += 1
                    for p in participants:
                        wld[p]["draws"] += 1
            else:
                abnormal_matches += 1
                for a in m.get("agents_at_fault", []):
                    agents_fault[a] += 1

            if per_match:
                seq = []
                for s in m.get("steps", []):
                    move = s.get("move", "")
                    move = move.strip("<>") if isinstance(move, str) else move
                    seq.append(f"{s.get('agent','')}:{move}")
                match_detail = {
                    "game": game,
                    "status": m.get("status"),
                    "participants": participants,
                    "winner": m.get("winner", ""),
                    "sequence": seq,
                }
                # Add duration if available
                if duration > 0:
                    match_detail["duration_seconds"] = duration
                match_details.append(match_detail)

    # average win rates
    avg_win_rates = {k: (sum(v)/len(v) if v else 0.0) for k, v in win_rates_acc.items()}
    avg_tokens = tokens_total / total_runs if total_runs else 0
    
    # Calculate time statistics
    avg_duration = total_duration / len(match_durations) if match_durations else 0
    min_duration = min(match_durations) if match_durations else 0
    max_duration = max(match_durations) if match_durations else 0

    result = {
        "total_histories": total_runs,
        "games": dict(games),
        "normal_matches": normal_matches,
        "abnormal_matches": abnormal_matches,
        "draw_matches": draw_matches,
        "winners": dict(winners),
        "agents_at_fault": dict(agents_fault),
        "avg_win_rates": avg_win_rates,
        "agent_model_wld": wld,
        "tokens_total": tokens_total,
        "avg_tokens_per_history": avg_tokens,
        "time_statistics": {
            "total_duration_seconds": round(total_duration, 2),
            "avg_duration_per_match_seconds": round(avg_duration, 2),
            "min_duration_seconds": round(min_duration, 2),
            "max_duration_seconds": round(max_duration, 2),
            "total_matches_with_timing": len(match_durations)
        }
    }

    if per_match:
        result["matches"] = match_details
    return result


def main():
    parser = argparse.ArgumentParser(description="Summarize GTBench JSONL results")
    parser.add_argument("paths", nargs="+", help="Ruta(s) a archivos .jsonl o directorios con .jsonl")
    parser.add_argument("--per-match", action="store_true", help="Incluye listado de partidas con secuencia de jugadas")
    parser.add_argument("--save", type=str, help="Ruta para guardar el resumen en JSON")
    args = parser.parse_args()

    files = []
    for p in args.paths:
        path = Path(p)
        if path.is_dir():
            files.extend(sorted(path.rglob("*.jsonl")))
        elif path.suffix == ".jsonl" and path.exists():
            files.append(path)

    items = []
    for fp in files:
        items.extend(load_jsonl(fp))

    summary = summarize(items, per_match=args.per_match)

    if args.save:
        Path(args.save).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
