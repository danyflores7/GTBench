# 🧪 Guía de Pruebas: GPT-OSS-120B con Diferentes Configuraciones

Este documento contiene los comandos para ejecutar las pruebas con GPT-OSS-120B en diferentes configuraciones de razonamiento y tipos de prompts.

## 📋 Configuraciones de Modelo Disponibles (120B)

| Archivo | Descripción | Razonamiento |
|---------|-------------|--------------|
| `gpt-oss-120b-no-reasoning.yaml` | Sin razonamiento | `reasoning: false` |
| `gpt-oss-120b-reasoning-low.yaml` | Razonamiento bajo | `reasoning_effort: "low"` |
| `gpt-oss-120b-reasoning-medium.yaml` | Razonamiento medio | `reasoning_effort: "medium"` |
| `gpt-oss-120b-reasoning-high.yaml` | Razonamiento alto | `reasoning_effort: "high"` |

## 📋 Configuraciones de Agente Disponibles

| Archivo | Descripción | Tipo de Prompt |
|---------|-------------|----------------|
| `prompt_agent.yaml` | Prompt Simple | Sin cadena de pensamiento |
| `cot_agent.yaml` | Chain of Thought (CoT) | Con razonamiento paso a paso |
| `sccot_agent.yaml` | Self-Consistency CoT | CoT con múltiples muestras |
| `tot_agent.yaml` | Tree of Thoughts (ToT) | Con múltiples ramas de pensamiento |

## 🎮 Juegos a Evaluar

- **Juegos principales**: `first_sealed_auction`, `kuhn_poker`, `liars_dice`, `negotiation`, `pig`
- **Juego especial**: `prisoners_dilemma` (vs `titfortat_agent`)

---

## 🔬 Comandos para las Pruebas - GPT-OSS-120B

### Grupo 1: Sin Razonamiento (no-reasoning)

#### 1️⃣ GPT-OSS-120B sin razonamiento + Prompt Simple vs MCTS
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names first_sealed_auction kuhn_poker liars_dice negotiation pig \
  --agent-configs gamingbench/configs/agent_configs/prompt_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-no-reasoning.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-no-reasoning.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-no-reasoning-simple \
  --exchange-first-player
```

**Prisoners Dilemma:**
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names prisoners_dilemma \
  --agent-configs gamingbench/configs/agent_configs/prompt_agent.yaml \
                 gamingbench/configs/agent_configs/titfortat_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-no-reasoning.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-no-reasoning.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-no-reasoning-simple \
  --exchange-first-player
```

#### 2️⃣ GPT-OSS-120B sin razonamiento + CoT vs MCTS
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names first_sealed_auction kuhn_poker liars_dice negotiation pig \
  --agent-configs gamingbench/configs/agent_configs/cot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-no-reasoning.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-no-reasoning.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-no-reasoning-cot \
  --exchange-first-player
```

**Prisoners Dilemma:**
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names prisoners_dilemma \
  --agent-configs gamingbench/configs/agent_configs/cot_agent.yaml \
                 gamingbench/configs/agent_configs/titfortat_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-no-reasoning.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-no-reasoning.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-no-reasoning-cot \
  --exchange-first-player
```

#### 3️⃣ GPT-OSS-120B sin razonamiento + SCCoT vs MCTS
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names first_sealed_auction kuhn_poker liars_dice negotiation pig \
  --agent-configs gamingbench/configs/agent_configs/sccot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-no-reasoning.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-no-reasoning.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-no-reasoning-sccot \
  --exchange-first-player
```

**Prisoners Dilemma:**
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names prisoners_dilemma \
  --agent-configs gamingbench/configs/agent_configs/sccot_agent.yaml \
                 gamingbench/configs/agent_configs/titfortat_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-no-reasoning.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-no-reasoning.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-no-reasoning-sccot \
  --exchange-first-player
```

#### 4️⃣ GPT-OSS-120B sin razonamiento + ToT vs MCTS
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names first_sealed_auction kuhn_poker liars_dice negotiation pig \
  --agent-configs gamingbench/configs/agent_configs/tot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-no-reasoning.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-no-reasoning.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-no-reasoning-tot \
  --exchange-first-player
```

**Prisoners Dilemma:**
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names prisoners_dilemma \
  --agent-configs gamingbench/configs/agent_configs/tot_agent.yaml \
                 gamingbench/configs/agent_configs/titfortat_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-no-reasoning.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-no-reasoning.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-no-reasoning-tot \
  --exchange-first-player
```

---

### Grupo 2: Razonamiento Bajo (reasoning-low)

#### 5️⃣ GPT-OSS-120B razonamiento bajo + Prompt Simple vs MCTS
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names first_sealed_auction kuhn_poker liars_dice negotiation pig \
  --agent-configs gamingbench/configs/agent_configs/prompt_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-low.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-low.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-low-simple \
  --exchange-first-player
```

**Prisoners Dilemma:**
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names prisoners_dilemma \
  --agent-configs gamingbench/configs/agent_configs/prompt_agent.yaml \
                 gamingbench/configs/agent_configs/titfortat_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-low.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-low.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-low-simple \
  --exchange-first-player
```

#### 6️⃣ GPT-OSS-120B razonamiento bajo + CoT vs MCTS
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names first_sealed_auction kuhn_poker liars_dice negotiation pig \
  --agent-configs gamingbench/configs/agent_configs/cot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-low.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-low.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-low-cot \
  --exchange-first-player
```

**Prisoners Dilemma:**
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names prisoners_dilemma \
  --agent-configs gamingbench/configs/agent_configs/cot_agent.yaml \
                 gamingbench/configs/agent_configs/titfortat_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-low.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-low.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-low-cot \
  --exchange-first-player
```

#### 7️⃣ GPT-OSS-120B razonamiento bajo + SCCoT vs MCTS
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names first_sealed_auction kuhn_poker liars_dice negotiation pig \
  --agent-configs gamingbench/configs/agent_configs/sccot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-low.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-low.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-low-sccot \
  --exchange-first-player
```

**Prisoners Dilemma:**
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names prisoners_dilemma \
  --agent-configs gamingbench/configs/agent_configs/sccot_agent.yaml \
                 gamingbench/configs/agent_configs/titfortat_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-low.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-low.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-low-sccot \
  --exchange-first-player
```

#### 8️⃣ GPT-OSS-120B razonamiento bajo + ToT vs MCTS
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names first_sealed_auction kuhn_poker liars_dice negotiation pig \
  --agent-configs gamingbench/configs/agent_configs/tot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-low.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-low.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-low-tot \
  --exchange-first-player
```

**Prisoners Dilemma:**
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names prisoners_dilemma \
  --agent-configs gamingbench/configs/agent_configs/tot_agent.yaml \
                 gamingbench/configs/agent_configs/titfortat_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-low.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-low.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-low-tot \
  --exchange-first-player
```

---

### Grupo 3: Razonamiento Medio (reasoning-medium)

#### 9️⃣ GPT-OSS-120B razonamiento medio + Prompt Simple vs MCTS
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names first_sealed_auction kuhn_poker liars_dice negotiation pig \
  --agent-configs gamingbench/configs/agent_configs/prompt_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-medium.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-medium.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-medium-simple \
  --exchange-first-player
```

**Prisoners Dilemma:**
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names prisoners_dilemma \
  --agent-configs gamingbench/configs/agent_configs/prompt_agent.yaml \
                 gamingbench/configs/agent_configs/titfortat_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-medium.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-medium.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-medium-simple \
  --exchange-first-player
```

#### 🔟 GPT-OSS-120B razonamiento medio + CoT vs MCTS
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names first_sealed_auction kuhn_poker liars_dice negotiation pig \
  --agent-configs gamingbench/configs/agent_configs/cot_agent.yaml \
  --agent-configs gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-medium.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-medium.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-medium-cot \
  --exchange-first-player
```

**Prisoners Dilemma:**
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names prisoners_dilemma \
  --agent-configs gamingbench/configs/agent_configs/cot_agent.yaml \
                 gamingbench/configs/agent_configs/titfortat_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-medium.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-medium.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-medium-cot \
  --exchange-first-player
```

#### 1️⃣1️⃣ GPT-OSS-120B razonamiento medio + SCCoT vs MCTS
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names first_sealed_auction kuhn_poker liars_dice negotiation pig \
  --agent-configs gamingbench/configs/agent_configs/sccot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-medium.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-medium.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-medium-sccot \
  --exchange-first-player
```

**Prisoners Dilemma:**
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names prisoners_dilemma \
  --agent-configs gamingbench/configs/agent_configs/sccot_agent.yaml \
                 gamingbench/configs/agent_configs/titfortat_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-medium.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-medium.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-medium-sccot \
  --exchange-first-player
```

#### 1️⃣2️⃣ GPT-OSS-120B razonamiento medio + ToT vs MCTS
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names first_sealed_auction kuhn_poker liars_dice negotiation pig \
  --agent-configs gamingbench/configs/agent_configs/tot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-medium.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-medium.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-medium-tot \
  --exchange-first-player
```

**Prisoners Dilemma:**
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names prisoners_dilemma \
  --agent-configs gamingbench/configs/agent_configs/tot_agent.yaml \
                 gamingbench/configs/agent_configs/titfortat_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-medium.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-medium.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-medium-tot \
  --exchange-first-player
```

---

### Grupo 4: Razonamiento Alto (reasoning-high)

#### 1️⃣3️⃣ GPT-OSS-120B razonamiento alto + Prompt Simple vs MCTS
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names first_sealed_auction kuhn_poker liars_dice negotiation pig \
  --agent-configs gamingbench/configs/agent_configs/prompt_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-high.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-high.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-high-simple \
  --exchange-first-player
```

**Prisoners Dilemma:**
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names prisoners_dilemma \
  --agent-configs gamingbench/configs/agent_configs/prompt_agent.yaml \
                 gamingbench/configs/agent_configs/titfortat_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-high.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-high.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-high-simple \
  --exchange-first-player
```

#### 1️⃣4️⃣ GPT-OSS-120B razonamiento alto + CoT vs MCTS
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names first_sealed_auction kuhn_poker liars_dice negotiation pig \
  --agent-configs gamingbench/configs/agent_configs/cot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-high.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-high.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-high-cot \
  --exchange-first-player
```

**Prisoners Dilemma:**
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names prisoners_dilemma \
  --agent-configs gamingbench/configs/agent_configs/cot_agent.yaml \
                 gamingbench/configs/agent_configs/titfortat_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-high.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-high.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-high-cot \
  --exchange-first-player
```

#### 1️⃣5️⃣ GPT-OSS-120B razonamiento alto + SCCoT vs MCTS
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names first_sealed_auction kuhn_poker liars_dice negotiation pig \
  --agent-configs gamingbench/configs/agent_configs/sccot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-high.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-high.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-high-sccot \
  --exchange-first-player
```

**Prisoners Dilemma:**
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names prisoners_dilemma \
  --agent-configs gamingbench/configs/agent_configs/sccot_agent.yaml \
                 gamingbench/configs/agent_configs/titfortat_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-high.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-high.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-high-sccot \
  --exchange-first-player
```

#### 1️⃣6️⃣ GPT-OSS-120B razonamiento alto + ToT vs MCTS
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names first_sealed_auction kuhn_poker liars_dice negotiation pig \
  --agent-configs gamingbench/configs/agent_configs/tot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-high.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-high.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-high-tot \
  --exchange-first-player
```

**Prisoners Dilemma:**
```bash
PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
  --game-names prisoners_dilemma \
  --agent-configs gamingbench/configs/agent_configs/tot_agent.yaml \
                 gamingbench/configs/agent_configs/titfortat_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-120b-reasoning-high.yaml \
                  gamingbench/configs/model_configs/gpt-oss-120b-reasoning-high.yaml \
  --num-matches 10 \
  --exp-root ./experiments/test-120b-reasoning-high-tot \
  --exchange-first-player
```

---

## 📊 Analizar Resultados

### Analizar una configuración específica:
```bash
./.venv/bin/python scripts/analyze_performance.py experiments/test-120b-no-reasoning-simple/
```

### Comparar todas las configuraciones de 120B:
```bash
python3 scripts/compare_configurations.py \
  experiments/test-120b-no-reasoning-simple \
  experiments/test-120b-no-reasoning-cot \
  experiments/test-120b-no-reasoning-sccot \
  experiments/test-120b-no-reasoning-tot \
  experiments/test-120b-reasoning-low-simple \
  experiments/test-120b-reasoning-low-cot \
  experiments/test-120b-reasoning-low-sccot \
  experiments/test-120b-reasoning-low-tot \
  experiments/test-120b-reasoning-medium-simple \
  experiments/test-120b-reasoning-medium-cot \
  experiments/test-120b-reasoning-medium-sccot \
  experiments/test-120b-reasoning-medium-tot \
  experiments/test-120b-reasoning-high-simple \
  experiments/test-120b-reasoning-high-cot \
  experiments/test-120b-reasoning-high-sccot \
  experiments/test-120b-reasoning-high-tot \
  --output experiments/comparison_report_120b.html
```

### Ver detalles por match:
```bash
./.venv/bin/python scripts/summarize_results.py --per-match \
  experiments/test-120b-no-reasoning-simple/**/*.jsonl
```

---

## 🚀 Script para Ejecutar Todas las Pruebas de 120B

Puedes crear un script bash para ejecutar todas las pruebas secuencialmente:

```bash
#!/bin/bash
# run_all_tests_120b.sh

export PYTHONPATH=.

GAMES="first_sealed_auction kuhn_poker liars_dice negotiation pig"
NUM_MATCHES=10

echo "🚀 Iniciando pruebas completas de GPT-OSS-120B..."
echo "🎮 Juegos: $GAMES"
echo "🔢 Matches por configuración: $NUM_MATCHES"
echo ""

# Función para ejecutar prueba
run_test() {
    local reasoning=$1
    local agent=$2
    local agent_file=$3
    local exp_name=$4
    local num=$5
    
    echo "  $num: $reasoning + $agent..."
    
    # Juegos principales vs MCTS
    PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
      --game-names $GAMES \
      --agent-configs gamingbench/configs/agent_configs/${agent_file}.yaml \
                     gamingbench/configs/agent_configs/mcts_agent.yaml \
      --model-configs gamingbench/configs/model_configs/gpt-oss-120b-${reasoning}.yaml \
                      gamingbench/configs/model_configs/gpt-oss-120b-${reasoning}.yaml \
      --num-matches $NUM_MATCHES \
      --exp-root ./experiments/test-120b-${reasoning}-${exp_name} \
      --exchange-first-player
    
    # Prisoners Dilemma vs TitForTat
    PYTHONPATH=. ./.venv/bin/python gamingbench/main.py \
      --game-names prisoners_dilemma \
      --agent-configs gamingbench/configs/agent_configs/${agent_file}.yaml \
                     gamingbench/configs/agent_configs/titfortat_agent.yaml \
      --model-configs gamingbench/configs/model_configs/gpt-oss-120b-${reasoning}.yaml \
                      gamingbench/configs/model_configs/gpt-oss-120b-${reasoning}.yaml \
      --num-matches $NUM_MATCHES \
      --exp-root ./experiments/test-120b-${reasoning}-${exp_name} \
      --exchange-first-player
}

# Grupo 1: Sin razonamiento
echo "📋 Grupo 1: Sin razonamiento (no-reasoning)"
run_test "no-reasoning" "Simple" "prompt_agent" "simple" "1/16"
run_test "no-reasoning" "CoT" "cot_agent" "cot" "2/16"
run_test "no-reasoning" "SCCoT" "sccot_agent" "sccot" "3/16"
run_test "no-reasoning" "ToT" "tot_agent" "tot" "4/16"

# Grupo 2: Razonamiento bajo
echo ""
echo "📋 Grupo 2: Razonamiento bajo (reasoning-low)"
run_test "reasoning-low" "Simple" "prompt_agent" "simple" "5/16"
run_test "reasoning-low" "CoT" "cot_agent" "cot" "6/16"
run_test "reasoning-low" "SCCoT" "sccot_agent" "sccot" "7/16"
run_test "reasoning-low" "ToT" "tot_agent" "tot" "8/16"

# Grupo 3: Razonamiento medio
echo ""
echo "📋 Grupo 3: Razonamiento medio (reasoning-medium)"
run_test "reasoning-medium" "Simple" "prompt_agent" "simple" "9/16"
run_test "reasoning-medium" "CoT" "cot_agent" "cot" "10/16"
run_test "reasoning-medium" "SCCoT" "sccot_agent" "sccot" "11/16"
run_test "reasoning-medium" "ToT" "tot_agent" "tot" "12/16"

# Grupo 4: Razonamiento alto
echo ""
echo "📋 Grupo 4: Razonamiento alto (reasoning-high)"
run_test "reasoning-high" "Simple" "prompt_agent" "simple" "13/16"
run_test "reasoning-high" "CoT" "cot_agent" "cot" "14/16"
run_test "reasoning-high" "SCCoT" "sccot_agent" "sccot" "15/16"
run_test "reasoning-high" "ToT" "tot_agent" "tot" "16/16"

echo ""
echo "✅ Todas las pruebas de GPT-OSS-120B completadas!"
echo "📊 Generando análisis comparativo..."

python3 scripts/compare_configurations.py \
  experiments/test-120b-no-reasoning-simple \
  experiments/test-120b-no-reasoning-cot \
  experiments/test-120b-no-reasoning-sccot \
  experiments/test-120b-no-reasoning-tot \
  experiments/test-120b-reasoning-low-simple \
  experiments/test-120b-reasoning-low-cot \
  experiments/test-120b-reasoning-low-sccot \
  experiments/test-120b-reasoning-low-tot \
  experiments/test-120b-reasoning-medium-simple \
  experiments/test-120b-reasoning-medium-cot \
  experiments/test-120b-reasoning-medium-sccot \
  experiments/test-120b-reasoning-medium-tot \
  experiments/test-120b-reasoning-high-simple \
  experiments/test-120b-reasoning-high-cot \
  experiments/test-120b-reasoning-high-sccot \
  experiments/test-120b-reasoning-high-tot \
  --output experiments/comparison_report_120b.html

echo "📄 Reporte generado: experiments/comparison_report_120b.html"
```

### Para usar el script:
```bash
chmod +x run_all_tests_120b.sh
./run_all_tests_120b.sh
```

---

## 📝 Resumen de Configuraciones

### Total de Pruebas: **16 configuraciones**

| # | Razonamiento | Prompt | Juegos | Oponente |
|---|--------------|--------|--------|----------|
| 1 | No | Simple | 5 juegos | MCTS |
| 2 | No | CoT | 5 juegos | MCTS |
| 3 | No | SCCoT | 5 juegos | MCTS |
| 4 | No | ToT | 5 juegos | MCTS |
| 5 | Low | Simple | 5 juegos | MCTS |
| 6 | Low | CoT | 5 juegos | MCTS |
| 7 | Low | SCCoT | 5 juegos | MCTS |
| 8 | Low | ToT | 5 juegos | MCTS |
| 9 | Medium | Simple | 5 juegos | MCTS |
| 10 | Medium | CoT | 5 juegos | MCTS |
| 11 | Medium | SCCoT | 5 juegos | MCTS |
| 12 | Medium | ToT | 5 juegos | MCTS |
| 13 | High | Simple | 5 juegos | MCTS |
| 14 | High | CoT | 5 juegos | MCTS |
| 15 | High | SCCoT | 5 juegos | MCTS |
| 16 | High | ToT | 5 juegos | MCTS |

**Nota:** Cada configuración también incluye `prisoners_dilemma` vs `titfortat_agent`.

---

## ⚡ Tiempo Estimado

- **Por configuración**: ~20-40 minutos (dependiendo del juego y razonamiento)
- **Total para 16 configuraciones**: ~8-12 horas
- **Recomendación**: Ejecutar en background o por lotes

---

## 🎯 Notas Importantes

1. **API Key**: Asegúrate de tener tu NVIDIA API key configurada
2. **Prisoners Dilemma**: Siempre usa `titfortat_agent` como oponente (MCTS no funciona)
3. **Razonamiento Alto**: Puede consumir más tokens y tiempo
4. **ToT con no-reasoning**: Puede tener alta tasa de errores (ver análisis previo)
5. **Almacenamiento**: Cada prueba genera ~50-200MB de datos

---

## 📈 Análisis Recomendado

Después de ejecutar todas las pruebas:

1. **Comparar por nivel de razonamiento**
2. **Comparar por tipo de prompt**
3. **Analizar win-rate por juego**
4. **Comparar tokens consumidos**
5. **Identificar configuración óptima**
