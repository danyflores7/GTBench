#!/bin/bash
# run_all_tests.sh - Ejecuta todas las configuraciones de pruebas de GPT-OSS-20B

export PYTHONPATH=.

# Configuración
GAMES="${GAME:-tictactoe}"  # Usar variable de entorno GAME o por defecto tictactoe
NUM_MATCHES="${NUM_MATCHES:-10}"

# Verificar que existe NVIDIA_API_KEY
if [ -z "$NVIDIA_API_KEY" ]; then
    echo "❌ ERROR: NVIDIA_API_KEY no está configurada"
    echo "Por favor ejecuta: export NVIDIA_API_KEY=tu_api_key"
    exit 1
fi

echo "🚀 Iniciando pruebas completas de GPT-OSS-20B..."
echo "   Juego: $GAMES"
echo "   Partidas por prueba: $NUM_MATCHES"
echo ""

# Grupo 1: Sin razonamiento
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Grupo 1: Sin razonamiento"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "  1/9: Simple (sin razonamiento)..."
./.venv/bin/python gamingbench/main.py --game-names $GAMES \
  --agent-configs gamingbench/configs/agent_configs/prompt_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
  --num-matches $NUM_MATCHES --exp-root ./experiments/test-no-reasoning-simple --exchange-first-player

echo "  2/9: CoT (sin razonamiento)..."
./.venv/bin/python gamingbench/main.py --game-names $GAMES \
  --agent-configs gamingbench/configs/agent_configs/cot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
  --num-matches $NUM_MATCHES --exp-root ./experiments/test-no-reasoning-cot --exchange-first-player

echo "  3/9: ToT (sin razonamiento)..."
./.venv/bin/python gamingbench/main.py --game-names $GAMES \
  --agent-configs gamingbench/configs/agent_configs/tot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-no-reasoning.yaml \
  --num-matches $NUM_MATCHES --exp-root ./experiments/test-no-reasoning-tot --exchange-first-player

# Grupo 2: Razonamiento bajo
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Grupo 2: Razonamiento bajo"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "  4/9: Simple (razonamiento bajo)..."
./.venv/bin/python gamingbench/main.py --game-names $GAMES \
  --agent-configs gamingbench/configs/agent_configs/prompt_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-reasoning-low.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-reasoning-low.yaml \
  --num-matches $NUM_MATCHES --exp-root ./experiments/test-reasoning-low-simple --exchange-first-player

echo "  5/9: CoT (razonamiento bajo)..."
./.venv/bin/python gamingbench/main.py --game-names $GAMES \
  --agent-configs gamingbench/configs/agent_configs/cot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-reasoning-low.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-reasoning-low.yaml \
  --num-matches $NUM_MATCHES --exp-root ./experiments/test-reasoning-low-cot --exchange-first-player

echo "  6/9: ToT (razonamiento bajo)..."
./.venv/bin/python gamingbench/main.py --game-names $GAMES \
  --agent-configs gamingbench/configs/agent_configs/tot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-reasoning-low.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-reasoning-low.yaml \
  --num-matches $NUM_MATCHES --exp-root ./experiments/test-reasoning-low-tot --exchange-first-player

# Grupo 3: Razonamiento medio
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Grupo 3: Razonamiento medio"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "  7/9: Simple (razonamiento medio)..."
./.venv/bin/python gamingbench/main.py --game-names $GAMES \
  --agent-configs gamingbench/configs/agent_configs/prompt_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
  --num-matches $NUM_MATCHES --exp-root ./experiments/test-reasoning-medium-simple --exchange-first-player

echo "  8/9: CoT (razonamiento medio)..."
./.venv/bin/python gamingbench/main.py --game-names $GAMES \
  --agent-configs gamingbench/configs/agent_configs/cot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
  --num-matches $NUM_MATCHES --exp-root ./experiments/test-reasoning-medium-cot --exchange-first-player

echo "  9/9: ToT (razonamiento medio)..."
./.venv/bin/python gamingbench/main.py --game-names $GAMES \
  --agent-configs gamingbench/configs/agent_configs/tot_agent.yaml \
                 gamingbench/configs/agent_configs/mcts_agent.yaml \
  --model-configs gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
                  gamingbench/configs/model_configs/gpt-oss-20b-reasoning-medium.yaml \
  --num-matches $NUM_MATCHES --exp-root ./experiments/test-reasoning-medium-tot --exchange-first-player

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Todas las pruebas completadas!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
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

echo ""
echo "📄 Análisis comparativo guardado en: experiments/comparative_analysis.txt"
echo ""
echo "💡 Para ver los resultados:"
echo "   cat experiments/comparative_analysis.txt"
echo ""
echo "💡 Para analizar una prueba específica:"
echo "   ./.venv/bin/python scripts/analyze_performance.py experiments/test-no-reasoning-simple/"
echo ""
