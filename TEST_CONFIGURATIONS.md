# 🧪 Guía de Pruebas: GPT-OSS-20B con Diferentes Configuraciones

Este documento contiene los comandos para ejecutar las 9 configuraciones de pruebas diferentes con GPT-OSS-20B.

## 📋 Configuraciones de Modelo Disponibles

| Archivo | Descripción | Razonamiento |
|---------|-------------|--------------|
| `gpt-oss-20b-no-reasoning.yaml` | Sin razonamiento | `reasoning: false` |
| `gpt-oss-20b-reasoning-low.yaml` | Razonamiento bajo | `reasoning_effort: "low"` |
| `gpt-oss-20b-reasoning-medium.yaml` | Razonamiento medio | `reasoning_effort: "medium"` |

## 📋 Configuraciones de Agente Disponibles

| Archivo | Descripción | Tipo de Prompt |
|---------|-------------|----------------|
| `prompt_agent.yaml` | Prompt Simple | Sin cadena de pensamiento |
| `cot_agent.yaml` | Chain of Thought (CoT) | Con razonamiento paso a paso |
| `tot_agent.yaml` | Tree of Thoughts (ToT) | Con múltiples ramas de pensamiento |

---

## 🔬 Comandos para las 9 Pruebas

### Grupo 1: Sin Razonamiento

#### 1️⃣ GPT-OSS-20B sin razonamiento + Prompt Simple vs MCTS
```bash
NVIDIA_API_KEY=tu_api_key PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names tictactoe \
  --agent-configs gamingbench/configs/agent_configs/prompt_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-no-reasoning-simple \
  --exchange-first-player
```

PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names first_sealed_auction kuhn_poker liars_dice negotiation pig \
  --agent-configs gamingbench/configs/agent_configs/sccot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-no-reasoning-sccot \
  --exchange-first-player

PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names prisoners_dilemma \
  --agent-configs gamingbench/configs/agent_configs/prompt_agent.yaml \
                 gamingbench/configs/agent_configs/titfortat_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-no-reasoning-simple \
  --exchange-first-player

#### 2️⃣ GPT-OSS-20B sin razonamiento + CoT vs MCTS
```bash
NVIDIA_API_KEY=tu_api_key PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names tictactoe \
  --agent-configs gamingbench/configs/agent_configs/cot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-no-reasoning-cot \
  --exchange-first-player
```

PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names prisoners_dilemma \
  --agent-configs gamingbench/configs/agent_configs/cot_agent.yaml \
                 gamingbench/configs/agent_configs/titfortat_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-no-reasoning-cot \
  --exchange-first-player

#### 3️⃣ GPT-OSS-20B sin razonamiento + ToT vs MCTS
```bash
NVIDIA_API_KEY=tu_api_key PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names tictactoe \
  --agent-configs gamingbench/configs/agent_configs/tot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-no-reasoning-tot \
  --exchange-first-player
```

PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names prisoners_dilemma \
  --agent-configs gamingbench/configs/agent_configs/titfortat_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-no-reasoning-tot \
  --exchange-first-player

---

### Grupo 2: Razonamiento Bajo

#### 4️⃣ GPT-OSS-20B razonamiento bajo + Prompt Simple vs MCTS
```bash
NVIDIA_API_KEY=tu_api_key PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names tictactoe \
  --agent-configs gamingbench/configs/agent_configs/prompt_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-reasoning-low.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-reasoning-low.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-reasoning-low-simple \
  --exchange-first-player
```
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names first_sealed_auction kuhn_poker liars_dice negotiation pig \
  --agent-configs gamingbench/configs/agent_configs/sccot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-reasoning-low.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-reasoning-low.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-reasoning-low-sccot \
  --exchange-first-player

#### 5️⃣ GPT-OSS-20B razonamiento bajo + CoT vs MCTS
```bash
NVIDIA_API_KEY=tu_api_key PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names tictactoe \
  --agent-configs gamingbench/configs/agent_configs/cot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-reasoning-low.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-reasoning-low.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-reasoning-low-cot \
  --exchange-first-player
```

#### 6️⃣ GPT-OSS-20B razonamiento bajo + ToT vs MCTS
```bash
NVIDIA_API_KEY=tu_api_key PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names tictactoe \
  --agent-configs gamingbench/configs/agent_configs/tot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-reasoning-low.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-reasoning-low.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-reasoning-low-tot \
  --exchange-first-player
```

---

### Grupo 3: Razonamiento Medio

#### 7️⃣ GPT-OSS-20B razonamiento medio + Prompt Simple vs MCTS
```bash
NVIDIA_API_KEY=tu_api_key PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names tictactoe \
  --agent-configs gamingbench/configs/agent_configs/prompt_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-reasoning-medium-simple \
  --exchange-first-player
```

PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names first_sealed_auction kuhn_poker liars_dice negotiation pig \
  --agent-configs gamingbench/configs/agent_configs/sccot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-reasoning-medium-sccot \
  --exchange-first-player

#### 8️⃣ GPT-OSS-20B razonamiento medio + CoT vs MCTS
```bash
NVIDIA_API_KEY=tu_api_key PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names tictactoe \
  --agent-configs gamingbench/configs/agent_configs/cot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-reasoning-medium-cot \
  --exchange-first-player
```

#### 9️⃣ GPT-OSS-20B razonamiento medio + ToT vs MCTS
```bash
NVIDIA_API_KEY=tu_api_key PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names tictactoe \
  --agent-configs gamingbench/configs/agent_configs/tot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-reasoning-medium-tot \
  --exchange-first-player
```

---

## 📊 Analizar Resultados

### Analizar una prueba específica:
```bash
./.venv/bin/python scripts/analyze_performance.py experiments/test-no-reasoning-simple/
```

### Comparar todas las pruebas:
```bash
./.venv/bin/python scripts/analyze_performance.py \
  experiments/test-no-reasoning-simple/ \
  experiments/test-no-reasoning-cot/ \
  experiments/test-no-reasoning-tot/ \
  experiments/test-reasoning-low-simple/ \
  experiments/test-reasoning-low-cot/ \
  experiments/test-reasoning-low-tot/ \
  experiments/test-reasoning-medium-simple/ \
  experiments/test-reasoning-medium-cot/ \
  experiments/test-reasoning-medium-tot/
```

### Ver detalles por match:
```bash
./.venv/bin/python scripts/summarize_results.py --per-match \
  experiments/test-no-reasoning-simple/**/*.jsonl
```

---

## 🎯 Script para Ejecutar Todas las Pruebas

Puedes crear un script bash para ejecutar todas las pruebas secuencialmente:

```bash
#!/bin/bash
# run_all_tests.sh

export NVIDIA_API_KEY=tu_api_key
export PYTHONPATH=.

GAMES="tictactoe"  # Cambiar según necesites
NUM_MATCHES=10

echo "🚀 Iniciando pruebas completas de GPT-OSS-20B..."

# Grupo 1: Sin razonamiento
echo "📋 Grupo 1: Sin razonamiento"
echo "  1/9: Simple..."
./.venv/bin/python gamingbench/main.py --game-names $GAMES \
  --agent-configs gamingbench/configs/agent_configs/prompt_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
  --num-matches $NUM_MATCHES --exp-root ./experiments/test-no-reasoning-simple --exchange-first-player

echo "  2/9: CoT..."
./.venv/bin/python gamingbench/main.py --game-names $GAMES \
  --agent-configs gamingbench/configs/agent_configs/cot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
  --num-matches $NUM_MATCHES --exp-root ./experiments/test-no-reasoning-cot --exchange-first-player

echo "  3/9: ToT..."
./.venv/bin/python gamingbench/main.py --game-names $GAMES \
  --agent-configs gamingbench/configs/agent_configs/tot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
  --num-matches $NUM_MATCHES --exp-root ./experiments/test-no-reasoning-tot --exchange-first-player

# Grupo 2: Razonamiento bajo
echo "📋 Grupo 2: Razonamiento bajo"
echo "  4/9: Simple..."
./.venv/bin/python gamingbench/main.py --game-names $GAMES \
  --agent-configs gamingbench/configs/agent_configs/prompt_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-reasoning-low.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-reasoning-low.yaml \
  --num-matches $NUM_MATCHES --exp-root ./experiments/test-reasoning-low-simple --exchange-first-player

echo "  5/9: CoT..."
./.venv/bin/python gamingbench/main.py --game-names $GAMES \
  --agent-configs gamingbench/configs/agent_configs/cot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-reasoning-low.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-reasoning-low.yaml \
  --num-matches $NUM_MATCHES --exp-root ./experiments/test-reasoning-low-cot --exchange-first-player

echo "  6/9: ToT..."
./.venv/bin/python gamingbench/main.py --game-names $GAMES \
  --agent-configs gamingbench/configs/agent_configs/tot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-reasoning-low.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-reasoning-low.yaml \
  --num-matches $NUM_MATCHES --exp-root ./experiments/test-reasoning-low-tot --exchange-first-player

# Grupo 3: Razonamiento medio
echo "📋 Grupo 3: Razonamiento medio"
echo "  7/9: Simple..."
./.venv/bin/python gamingbench/main.py --game-names $GAMES \
  --agent-configs gamingbench/configs/agent_configs/prompt_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
  --num-matches $NUM_MATCHES --exp-root ./experiments/test-reasoning-medium-simple --exchange-first-player

echo "  8/9: CoT..."
./.venv/bin/python gamingbench/main.py --game-names $GAMES \
  --agent-configs gamingbench/configs/agent_configs/cot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
  --num-matches $NUM_MATCHES --exp-root ./experiments/test-reasoning-medium-cot --exchange-first-player

echo "  9/9: ToT..."
./.venv/bin/python gamingbench/main.py --game-names $GAMES \
  --agent-configs gamingbench/configs/agent_configs/tot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
  --num-matches $NUM_MATCHES --exp-root ./experiments/test-reasoning-medium-tot --exchange-first-player

echo "✅ Todas las pruebas completadas!"
echo "📊 Generando análisis comparativo..."

./.venv/bin/python scripts/analyze_performance.py \
  experiments/test-no-reasoning-simple/ \
  experiments/test-no-reasoning-cot/ \
  experiments/test-no-reasoning-tot/ \
  experiments/test-reasoning-low-simple/ \
  experiments/test-reasoning-low-cot/ \
  experiments/test-reasoning-low-tot/ \
  experiments/test-reasoning-medium-simple/ \
  experiments/test-reasoning-medium-cot/ \
  experiments/test-reasoning-medium-tot/ \
  > experiments/comparative_analysis.txt

echo "📄 Resultados guardados en experiments/comparative_analysis.txt"
```

Para usarlo:
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```

---

## 📝 Notas

- Cambia `tu_api_key` por tu API key real de NVIDIA
- Ajusta `--num-matches` según cuántas partidas quieras por prueba
- Puedes cambiar `tictactoe` por otros juegos: `kuhn_poker`, `negotiation`, `pig`, etc.
- Cada prueba guarda resultados en un directorio separado para facilitar el análisis







python3 scripts/compare_configurations.py \
  experiments/test-no-reasoning-simple \
  experiments/test-no-reasoning-cot \
  experiments/test-no-reasoning-sccot \
  experiments/test-no-reasoning-tot \
  experiments/test-reasoning-low-simple \
  experiments/test-reasoning-low-cot \
  experiments/test-reasoning-low-sccot \
  experiments/test-reasoning-low-tot \
  experiments/test-reasoning-medium-simple \
  experiments/test-reasoning-medium-cot \
  experiments/test-reasoning-medium-sccot \
  experiments/test-reasoning-medium-tot \
  experiments/test-reasoning-high-simple \
  experiments/test-reasoning-high-cot \
  experiments/test-reasoning-high-sccot \
  experiments/test-reasoning-high-tot \
  --output experiments/comparison_report.html


  PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names prisoners_dilemma \
  --agent-configs gamingbench/configs/agent_configs/sccot_agent.yaml \
                 gamingbench/configs/agent_configs/titfortat_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-reasoning-medium-sccot \
  --exchange-first-player