#!/usr/bin/env python3
"""
Script para comparar visualmente el rendimiento de GPT-OSS-20B
en diferentes configuraciones de razonamiento y estrategias de prompt.

Genera un reporte HTML interactivo con gráficos y tablas comparativas.
"""

import argparse
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any


def load_jsonl(path: Path) -> List[Dict]:
    """Carga todos los objetos JSON de un archivo JSONL."""
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


def extract_config_from_path(path: Path) -> Dict[str, str]:
    """Extrae configuración desde la ruta del experimento."""
    parts = path.parts
    
    # Buscar el nombre del experimento (e.g., test-no-reasoning-simple)
    exp_name = None
    for part in parts:
        if part.startswith("test-"):
            exp_name = part
            break
    
    if not exp_name:
        return {"reasoning": "unknown", "prompt": "unknown"}
    
    # Extraer tipo de razonamiento
    if "no-reasoning" in exp_name:
        reasoning = "Sin Razonamiento"
    elif "reasoning-low" in exp_name:
        reasoning = "Razonamiento Bajo"
    elif "reasoning-medium" in exp_name:
        reasoning = "Razonamiento Medio"
    elif "reasoning-high" in exp_name:
        reasoning = "Razonamiento Alto"
    else:
        reasoning = "Unknown"
    
    # Extraer estrategia de prompt
    if exp_name.endswith("-simple"):
        prompt = "Simple"
    elif exp_name.endswith("-cot"):
        prompt = "CoT"
    elif exp_name.endswith("-sccot"):
        prompt = "SCCoT"
    elif exp_name.endswith("-tot"):
        prompt = "ToT"
    else:
        prompt = "Unknown"
    
    return {"reasoning": reasoning, "prompt": prompt}


def analyze_experiments(folders: List[Path]) -> Dict[str, Any]:
    """Analiza múltiples carpetas de experimentos."""
    results = {}
    
    for folder in folders:
        if not folder.exists():
            print(f"⚠️  Carpeta no encontrada: {folder}")
            continue
        
        config = extract_config_from_path(folder)
        config_key = f"{config['reasoning']} + {config['prompt']}"
        
        # Buscar todos los archivos JSONL recursivamente
        jsonl_files = list(folder.rglob("*.jsonl"))
        
        if not jsonl_files:
            print(f"⚠️  No se encontraron archivos JSONL en: {folder}")
            continue
        
        # Analizar por juego
        game_stats = defaultdict(lambda: {
            "total_matches": 0,
            "normal_matches": 0,
            "abnormal_matches": 0,
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "total_duration": 0,
            "total_tokens": 0,
            "durations": [],
            "tokens": [],
        })
        
        for jsonl_file in jsonl_files:
            # Determinar el juego desde el path
            game_name = jsonl_file.parent.name
            
            items = load_jsonl(jsonl_file)
            
            for hist in items:
                # Obtener configuración de agentes
                agents_config = hist.get("agents_config", [])
                
                # Identificar el agente que NO es MCTS (el agente bajo prueba)
                # Asumimos que el primer agente que no sea MCTSAgent es el que queremos evaluar
                test_agent = None
                for agent_conf in agents_config:
                    agent_name = agent_conf.get("agent_name", "")
                    if agent_name != "MCTSAgent":
                        test_agent = agent_name
                        break
                
                # Si no encontramos un agente de prueba, usar el primero
                if not test_agent and agents_config:
                    test_agent = agents_config[0].get("agent_name", "")
                
                for match in hist.get("matches", []):
                    game_stats[game_name]["total_matches"] += 1
                    
                    if match.get("status") == "Normal":
                        game_stats[game_name]["normal_matches"] += 1
                    else:
                        game_stats[game_name]["abnormal_matches"] += 1
                    
                    # Obtener el ganador
                    winner = match.get("winner", "")
                    
                    # Determinar si el ganador es el agente bajo prueba
                    is_test_agent_win = False
                    if winner and test_agent:
                        # El winner puede ser "CoTAgent_gpt-oss-20b-reasoning-low" o similar
                        is_test_agent_win = winner.startswith(test_agent)
                    
                    # Contar victorias/derrotas/empates
                    if winner == "":
                        game_stats[game_name]["draws"] += 1
                    elif is_test_agent_win:
                        game_stats[game_name]["wins"] += 1
                    else:
                        game_stats[game_name]["losses"] += 1
                    
                    # Duración
                    duration = match.get("duration_seconds", 0)
                    if duration > 0:
                        game_stats[game_name]["total_duration"] += duration
                        game_stats[game_name]["durations"].append(duration)
                    
                    # Tokens
                    tokens = match.get("token_size", 0)
                    game_stats[game_name]["total_tokens"] += tokens
                    game_stats[game_name]["tokens"].append(tokens)
        
        results[config_key] = dict(game_stats)
    
    return results


def generate_html_report(results: Dict[str, Any], output_file: Path):
    """Genera un reporte HTML interactivo."""
    
    # Extraer todos los juegos únicos
    all_games = set()
    for config_stats in results.values():
        all_games.update(config_stats.keys())
    all_games = sorted(all_games)
    
    # Extraer todas las configuraciones
    configs = sorted(results.keys())
    
    html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparación de Rendimiento GPT-OSS-20B</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .section {
            margin-bottom: 50px;
        }
        
        .section h2 {
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
        }
        
        .metric-card h3 {
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .metric-card .value {
            font-size: 2.5em;
            font-weight: bold;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-radius: 10px;
            overflow: hidden;
        }
        
        th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 1px;
        }
        
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #f0f0f0;
        }
        
        tr:hover {
            background: #f8f9ff;
        }
        
        .chart-container {
            position: relative;
            height: 400px;
            margin: 30px 0;
            padding: 20px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .win-rate {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
        }
        
        .win-rate.high { background: #4ade80; color: white; }
        .win-rate.medium { background: #fbbf24; color: white; }
        .win-rate.low { background: #f87171; color: white; }
        
        .badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin-right: 5px;
        }
        
        .badge.reasoning-none { background: #e0e7ff; color: #4338ca; }
        .badge.reasoning-low { background: #fef3c7; color: #92400e; }
        .badge.reasoning-medium { background: #fecaca; color: #991b1b; }
        .badge.reasoning-high { background: #ddd6fe; color: #5b21b6; }
        
        .badge.prompt-simple { background: #dbeafe; color: #1e40af; }
        .badge.prompt-cot { background: #d1fae5; color: #065f46; }
        .badge.prompt-sccot { background: #fed7aa; color: #9a3412; }
        .badge.prompt-tot { background: #fce7f3; color: #9f1239; }
        
        footer {
            background: #f8f9ff;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎮 Comparación de Rendimiento GPT-OSS-20B</h1>
            <p>Análisis comparativo de diferentes configuraciones de razonamiento y estrategias de prompt</p>
        </header>
        
        <div class="content">
"""
    
    # Sección de resumen general
    html += """
            <div class="section">
                <h2>📊 Resumen General</h2>
                <div class="metrics-grid">
"""
    
    total_configs = len(configs)
    total_games = len(all_games)
    total_matches = sum(
        sum(game_stats["total_matches"] for game_stats in config_stats.values())
        for config_stats in results.values()
    )
    
    html += f"""
                    <div class="metric-card">
                        <h3>Configuraciones</h3>
                        <div class="value">{total_configs}</div>
                    </div>
                    <div class="metric-card">
                        <h3>Juegos Evaluados</h3>
                        <div class="value">{total_games}</div>
                    </div>
                    <div class="metric-card">
                        <h3>Total de Partidas</h3>
                        <div class="value">{total_matches}</div>
                    </div>
"""
    
    html += """
                </div>
            </div>
"""
    
    # Tabla comparativa agrupada por juego
    html += """
            <div class="section">
                <h2>🎯 Resultados por Juego</h2>
"""
    
    # Iterar por cada juego
    for game in all_games:
        html += f"""
                <h3 style="margin-top: 30px; margin-bottom: 15px; color: #3b82f6; border-left: 4px solid #3b82f6; padding-left: 12px;">
                    🎮 {game}
                </h3>
                <table>
                    <thead>
                        <tr>
                            <th>Configuración</th>
                            <th>Partidas</th>
                            <th>Victorias</th>
                            <th>Derrotas</th>
                            <th>Empates</th>
                            <th>% Victoria</th>
                            <th>Normal/Anormal</th>
                            <th>Tiempo Promedio (s)</th>
                            <th>Tokens Promedio</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        
        # Ordenar configuraciones: primero por tipo de prompt (Simple, CoT, SCCoT, ToT), luego por nivel de razonamiento
        def sort_key(config):
            # Determinar tipo de prompt
            if "Simple" in config:
                prompt_order = 0
            elif "CoT" in config and "SCCoT" not in config:
                prompt_order = 1
            elif "SCCoT" in config:
                prompt_order = 2
            elif "ToT" in config:
                prompt_order = 3
            else:
                prompt_order = 4
            
            # Determinar nivel de razonamiento
            if "Sin Razonamiento" in config:
                reasoning_order = 0
            elif "Razonamiento Bajo" in config:
                reasoning_order = 1
            elif "Razonamiento Medio" in config:
                reasoning_order = 2
            elif "Razonamiento Alto" in config:
                reasoning_order = 3
            else:
                reasoning_order = 4
            
            return (prompt_order, reasoning_order)
        
        # Filtrar y ordenar configuraciones que tienen este juego
        configs_for_game = [c for c in configs if game in results[c]]
        configs_for_game.sort(key=sort_key)
        
        # Iterar por cada configuración ordenada para este juego
        for config in configs_for_game:
            config_stats = results[config]
            stats = config_stats[game]
            
            # Badges para la configuración
            reasoning_class = "reasoning-none"
            if "Bajo" in config:
                reasoning_class = "reasoning-low"
            elif "Medio" in config:
                reasoning_class = "reasoning-medium"
            elif "Alto" in config:
                reasoning_class = "reasoning-high"
            
            prompt_class = "prompt-simple"
            if "CoT" in config and "SCCoT" not in config:
                prompt_class = "prompt-cot"
            elif "SCCoT" in config:
                prompt_class = "prompt-sccot"
            elif "ToT" in config:
                prompt_class = "prompt-tot"
            
            stats = config_stats[game]
            total = stats["total_matches"]
            normal = stats["normal_matches"]
            wins = stats["wins"]
            losses = stats["losses"]
            draws = stats["draws"]
            
            # Calcular % victoria solo sobre partidas normales
            win_rate = (wins / normal * 100) if normal > 0 else 0
            win_rate_class = "high" if win_rate >= 60 else "medium" if win_rate >= 40 else "low"
            
            avg_duration = (stats["total_duration"] / len(stats["durations"])) if stats["durations"] else 0
            avg_tokens = (stats["total_tokens"] / len(stats["tokens"])) if stats["tokens"] else 0
            
            html += f"""
                        <tr>
                            <td>
                                <span class="badge {reasoning_class}">{config.split('+')[0].strip()}</span>
                                <span class="badge {prompt_class}">{config.split('+')[1].strip()}</span>
                            </td>
                            <td>{total}</td>
                            <td style="color: #22c55e; font-weight: bold;">{wins}</td>
                            <td style="color: #ef4444; font-weight: bold;">{losses}</td>
                            <td style="color: #6b7280;">{draws}</td>
                            <td><span class="win-rate {win_rate_class}">{win_rate:.1f}%</span></td>
                            <td>{stats["normal_matches"]} / {stats["abnormal_matches"]}</td>
                            <td>{avg_duration:.2f}</td>
                            <td>{avg_tokens:.0f}</td>
                        </tr>
"""
        
        html += """
                    </tbody>
                </table>
"""
    
    html += """
            </div>
"""
    
    # Gráficos de comparación
    html += """
            <div class="section">
                <h2>📈 Visualizaciones Comparativas</h2>
                
                <h3>Tasa de Victoria por Configuración</h3>
                <div class="chart-container">
                    <canvas id="winRateChart"></canvas>
                </div>
                
                <h3>Tiempo Promedio por Configuración</h3>
                <div class="chart-container">
                    <canvas id="timeChart"></canvas>
                </div>
                
                <h3>Tokens Promedio por Configuración</h3>
                <div class="chart-container">
                    <canvas id="tokensChart"></canvas>
                </div>
            </div>
"""
    
    # Preparar datos para gráficos
    chart_data = {
        "configs": configs,
        "win_rates": [],
        "avg_times": [],
        "avg_tokens": []
    }
    
    for config in configs:
        config_stats = results[config]
        total_wins = sum(stats["wins"] for stats in config_stats.values())
        total_normal = sum(stats["normal_matches"] for stats in config_stats.values())
        # Calcular win_rate solo sobre partidas normales
        win_rate = (total_wins / total_normal * 100) if total_normal > 0 else 0
        
        all_durations = []
        all_tokens = []
        for stats in config_stats.values():
            all_durations.extend(stats["durations"])
            all_tokens.extend(stats["tokens"])
        
        avg_time = (sum(all_durations) / len(all_durations)) if all_durations else 0
        avg_token = (sum(all_tokens) / len(all_tokens)) if all_tokens else 0
        
        chart_data["win_rates"].append(win_rate)
        chart_data["avg_times"].append(avg_time)
        chart_data["avg_tokens"].append(avg_token)
    
    # Scripts para gráficos
    html += f"""
        </div>
        
        <footer>
            <p>Generado automáticamente por GTBench Analysis Tool</p>
            <p>© 2025 - Análisis de Rendimiento GPT-OSS-20B</p>
        </footer>
    </div>
    
    <script>
        const configs = {json.dumps(chart_data["configs"])};
        const winRates = {json.dumps(chart_data["win_rates"])};
        const avgTimes = {json.dumps(chart_data["avg_times"])};
        const avgTokens = {json.dumps(chart_data["avg_tokens"])};
        
        const colors = [
            'rgba(102, 126, 234, 0.8)',  // Sin Razonamiento + Simple
            'rgba(34, 197, 94, 0.8)',     // Sin Razonamiento + CoT
            'rgba(251, 146, 60, 0.8)',    // Sin Razonamiento + SCCoT
            'rgba(237, 100, 166, 0.8)',   // Sin Razonamiento + ToT
            'rgba(118, 75, 162, 0.8)',    // Razonamiento Bajo + Simple
            'rgba(16, 185, 129, 0.8)',    // Razonamiento Bajo + CoT
            'rgba(249, 115, 22, 0.8)',    // Razonamiento Bajo + SCCoT
            'rgba(219, 39, 119, 0.8)',    // Razonamiento Bajo + ToT
            'rgba(79, 70, 229, 0.8)',     // Razonamiento Medio + Simple
            'rgba(5, 150, 105, 0.8)',     // Razonamiento Medio + CoT
            'rgba(234, 88, 12, 0.8)',     // Razonamiento Medio + SCCoT
            'rgba(190, 24, 93, 0.8)',     // Razonamiento Medio + ToT
            'rgba(99, 102, 241, 0.8)',    // Razonamiento Alto + Simple
            'rgba(16, 185, 129, 0.8)',    // Razonamiento Alto + CoT
            'rgba(249, 115, 22, 0.8)',    // Razonamiento Alto + SCCoT
            'rgba(219, 39, 119, 0.8)'     // Razonamiento Alto + ToT
        ];
        
        // Gráfico de tasa de victoria
        new Chart(document.getElementById('winRateChart'), {{
            type: 'bar',
            data: {{
                labels: configs,
                datasets: [{{
                    label: 'Tasa de Victoria (%)',
                    data: winRates,
                    backgroundColor: colors,
                    borderColor: colors.map(c => c.replace('0.8', '1')),
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return 'Victoria: ' + context.parsed.y.toFixed(1) + '%';
                            }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        ticks: {{
                            callback: function(value) {{
                                return value + '%';
                            }}
                        }}
                    }}
                }}
            }}
        }});
        
        // Gráfico de tiempo promedio
        new Chart(document.getElementById('timeChart'), {{
            type: 'line',
            data: {{
                labels: configs,
                datasets: [{{
                    label: 'Tiempo Promedio (segundos)',
                    data: avgTimes,
                    borderColor: 'rgba(102, 126, 234, 1)',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: true
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return value.toFixed(1) + 's';
                            }}
                        }}
                    }}
                }}
            }}
        }});
        
        // Gráfico de tokens promedio
        new Chart(document.getElementById('tokensChart'), {{
            type: 'line',
            data: {{
                labels: configs,
                datasets: [{{
                    label: 'Tokens Promedio',
                    data: avgTokens,
                    borderColor: 'rgba(118, 75, 162, 1)',
                    backgroundColor: 'rgba(118, 75, 162, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: true
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return value.toFixed(0);
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    
    # Guardar HTML
    output_file.write_text(html, encoding="utf-8")
    print(f"✅ Reporte HTML generado: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Compara visualmente el rendimiento de GPT-OSS-20B"
    )
    parser.add_argument(
        "folders",
        nargs="+",
        type=Path,
        help="Carpetas de experimentos a comparar"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("comparison_report.html"),
        help="Archivo HTML de salida (default: comparison_report.html)"
    )
    
    args = parser.parse_args()
    
    print("🔍 Analizando experimentos...")
    results = analyze_experiments(args.folders)
    
    if not results:
        print("❌ No se encontraron resultados para analizar")
        return
    
    print(f"📊 Generando reporte HTML...")
    generate_html_report(results, args.output)
    
    print(f"\n✨ ¡Listo! Abre el archivo para ver el reporte:")
    print(f"   file://{args.output.absolute()}")


if __name__ == "__main__":
    main()
