#!/usr/bin/env python3
"""
Analiza el rendimiento de los modelos en términos de tiempo y tokens.
"""

import argparse
import json
from pathlib import Path
from collections import defaultdict


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
                continue
    return items


def analyze_performance(items):
    """Analiza rendimiento de tiempo y tokens por juego y agente."""
    
    # Métricas generales
    total_matches = 0
    total_duration = 0
    total_tokens = 0
    
    # Por juego
    game_stats = defaultdict(lambda: {
        "matches": 0,
        "total_duration": 0,
        "total_tokens": 0,
        "durations": [],
        "tokens": []
    })
    
    # Por agente
    agent_stats = defaultdict(lambda: {
        "total_queries": 0,
        "total_tokens": 0,
        "query_tokens": []
    })
    
    for hist in items:
        game_name = hist.get("game_config", {}).get("game_name", "unknown")
        
        for match in hist.get("matches", []):
            if match.get("status") != "Normal":
                continue
                
            total_matches += 1
            duration = match.get("duration_seconds", 0)
            match_tokens = match.get("token_size", 0)
            
            total_duration += duration
            total_tokens += match_tokens
            
            game_stats[game_name]["matches"] += 1
            game_stats[game_name]["total_duration"] += duration
            game_stats[game_name]["total_tokens"] += match_tokens
            game_stats[game_name]["durations"].append(duration)
            game_stats[game_name]["tokens"].append(match_tokens)
            
            # Analizar por agente
            for step in match.get("steps", []):
                agent_name = f"{step.get('agent', '')}_{step.get('model_name', '')}"
                step_tokens = step.get("token_size", 0)
                num_queries = len(step.get("queries", []))
                
                if step_tokens > 0:
                    agent_stats[agent_name]["total_queries"] += num_queries
                    agent_stats[agent_name]["total_tokens"] += step_tokens
                    if num_queries > 0:
                        agent_stats[agent_name]["query_tokens"].extend([
                            q.get("token_size", 0) for q in step.get("queries", [])
                        ])
    
    # Calcular promedios
    avg_duration = total_duration / total_matches if total_matches > 0 else 0
    avg_tokens = total_tokens / total_matches if total_matches > 0 else 0
    
    # Resultados
    results = {
        "summary": {
            "total_matches": total_matches,
            "total_duration_seconds": round(total_duration, 2),
            "total_duration_minutes": round(total_duration / 60, 2),
            "avg_duration_per_match_seconds": round(avg_duration, 2),
            "total_tokens": total_tokens,
            "avg_tokens_per_match": round(avg_tokens, 2),
            "tokens_per_second": round(total_tokens / total_duration, 2) if total_duration > 0 else 0
        },
        "by_game": {},
        "by_agent": {}
    }
    
    # Por juego
    for game, stats in game_stats.items():
        matches = stats["matches"]
        results["by_game"][game] = {
            "matches": matches,
            "avg_duration_seconds": round(stats["total_duration"] / matches, 2) if matches > 0 else 0,
            "min_duration_seconds": round(min(stats["durations"]), 2) if stats["durations"] else 0,
            "max_duration_seconds": round(max(stats["durations"]), 2) if stats["durations"] else 0,
            "avg_tokens": round(stats["total_tokens"] / matches, 2) if matches > 0 else 0,
            "min_tokens": min(stats["tokens"]) if stats["tokens"] else 0,
            "max_tokens": max(stats["tokens"]) if stats["tokens"] else 0,
        }
    
    # Por agente
    for agent, stats in agent_stats.items():
        queries = stats["total_queries"]
        results["by_agent"][agent] = {
            "total_queries": queries,
            "total_tokens": stats["total_tokens"],
            "avg_tokens_per_query": round(stats["total_tokens"] / queries, 2) if queries > 0 else 0,
            "min_tokens_per_query": min(stats["query_tokens"]) if stats["query_tokens"] else 0,
            "max_tokens_per_query": max(stats["query_tokens"]) if stats["query_tokens"] else 0,
        }
    
    return results


def format_output(results):
    """Formatea la salida de forma legible."""
    output = []
    
    output.append("=" * 80)
    output.append("RESUMEN DE RENDIMIENTO")
    output.append("=" * 80)
    
    summary = results["summary"]
    output.append(f"\n📊 Estadísticas Generales:")
    output.append(f"  • Total de partidas: {summary['total_matches']}")
    output.append(f"  • Tiempo total: {summary['total_duration_seconds']} segundos ({summary['total_duration_minutes']} minutos)")
    output.append(f"  • Tiempo promedio por partida: {summary['avg_duration_per_match_seconds']} segundos")
    output.append(f"  • Tokens totales: {summary['total_tokens']:,}")
    output.append(f"  • Tokens promedio por partida: {summary['avg_tokens_per_match']:.2f}")
    output.append(f"  • Velocidad: {summary['tokens_per_second']:.2f} tokens/segundo")
    
    if results["by_game"]:
        output.append(f"\n🎮 Por Juego:")
        for game, stats in results["by_game"].items():
            output.append(f"\n  {game}:")
            output.append(f"    • Partidas: {stats['matches']}")
            output.append(f"    • Tiempo promedio: {stats['avg_duration_seconds']} seg (min: {stats['min_duration_seconds']}, max: {stats['max_duration_seconds']})")
            output.append(f"    • Tokens promedio: {stats['avg_tokens']:.0f} (min: {stats['min_tokens']}, max: {stats['max_tokens']})")
    
    if results["by_agent"]:
        output.append(f"\n🤖 Por Agente:")
        for agent, stats in results["by_agent"].items():
            output.append(f"\n  {agent}:")
            output.append(f"    • Total de consultas LLM: {stats['total_queries']}")
            output.append(f"    • Tokens totales: {stats['total_tokens']:,}")
            output.append(f"    • Tokens por consulta: {stats['avg_tokens_per_query']:.2f} (min: {stats['min_tokens_per_query']}, max: {stats['max_tokens_per_query']})")
    
    output.append("\n" + "=" * 80)
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="Analizar rendimiento de tiempo y tokens")
    parser.add_argument("paths", nargs="+", help="Ruta(s) a archivos .jsonl o directorios")
    parser.add_argument("--json", action="store_true", help="Salida en formato JSON")
    parser.add_argument("--save", type=str, help="Guardar resultados en archivo")
    args = parser.parse_args()
    
    files = []
    for p in args.paths:
        path = Path(p)
        if path.is_dir():
            files.extend(sorted(path.rglob("*.jsonl")))
        elif path.suffix == ".jsonl" and path.exists():
            files.append(path)
    
    if not files:
        print("No se encontraron archivos .jsonl")
        return
    
    items = []
    for fp in files:
        items.extend(load_jsonl(fp))
    
    if not items:
        print("No se encontraron datos en los archivos")
        return
    
    results = analyze_performance(items)
    
    if args.json:
        output = json.dumps(results, indent=2)
    else:
        output = format_output(results)
    
    print(output)
    
    if args.save:
        Path(args.save).write_text(output, encoding="utf-8")
        print(f"\n✅ Resultados guardados en: {args.save}")


if __name__ == "__main__":
    main()
