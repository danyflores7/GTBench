# 📊 Script de Comparación de Configuraciones

## 🎯 Descripción

`compare_configurations.py` es un script que genera un **reporte HTML interactivo** comparando el rendimiento de GPT-OSS-20B en diferentes configuraciones de razonamiento y estrategias de prompt.

## ✨ Características

El reporte incluye:

### 📈 **Visualizaciones Interactivas:**
- Gráfico de barras: Tasa de victoria por configuración
- Gráfico de líneas: Tiempo promedio de ejecución
- Gráfico de líneas: Tokens promedio consumidos

### 📊 **Tabla Comparativa Detallada:**
- Configuración (Razonamiento + Estrategia de Prompt)
- Resultados por juego
- Número de victorias, derrotas y empates
- Porcentaje de victoria
- Partidas normales vs anormales
- Tiempo promedio por partida
- Tokens promedio consumidos

### 🎨 **Diseño Moderno:**
- Interfaz responsiva y moderna
- Gráficos interactivos con Chart.js
- Códigos de colores para fácil interpretación
- Badges para identificar configuraciones

## 🚀 Uso

### **Básico:**

```bash
./.venv/bin/python scripts/compare_configurations.py \
  experiments/test-no-reasoning-simple/ \
  experiments/test-no-reasoning-cot/ \
  experiments/test-reasoning-low-simple/
```

### **Con archivo de salida personalizado:**

```bash
./.venv/bin/python scripts/compare_configurations.py \
  experiments/test-*/ \
  --output mi_reporte.html
```

### **Todas las carpetas de experimentos:**

```bash
./.venv/bin/python scripts/compare_configurations.py \
  experiments/test-no-reasoning-simple/ \
  experiments/test-no-reasoning-cot/ \
  experiments/test-no-reasoning-tot/ \
  experiments/test-reasoning-low-simple/ \
  experiments/test-reasoning-low-cot/ \
  experiments/test-reasoning-low-tot/ \
  experiments/test-reasoning-medium-simple/ \
  experiments/test-reasoning-medium-cot/ \
  experiments/test-reasoning-medium-tot/ \
  --output comparison_full.html
```

### **Usando wildcards (bash):**

```bash
./.venv/bin/python scripts/compare_configurations.py \
  experiments/test-*/ \
  --output comparison_all.html
```

## 📋 Opciones

```
positional arguments:
  folders              Carpetas de experimentos a comparar

options:
  -h, --help           Muestra este mensaje de ayuda
  --output, -o FILE    Archivo HTML de salida (default: comparison_report.html)
```

## 📂 Estructura de Entrada

El script busca automáticamente archivos `.jsonl` en las carpetas especificadas y extrae:

- **Configuración de razonamiento:** Desde el nombre de la carpeta
  - `test-no-reasoning-*` → Sin Razonamiento
  - `test-reasoning-low-*` → Razonamiento Bajo
  - `test-reasoning-medium-*` → Razonamiento Medio

- **Estrategia de prompt:** Desde el nombre de la carpeta
  - `*-simple` → Prompt Simple
  - `*-cot` → Chain of Thought (CoT)
  - `*-tot` → Tree of Thoughts (ToT)

- **Juegos:** Desde la estructura de subdirectorios
  - `experiments/test-*/tictactoe/*.jsonl`
  - `experiments/test-*/kuhn_poker/*.jsonl`
  - etc.

## 📊 Métricas Calculadas

Para cada configuración y juego:

| Métrica | Descripción |
|---------|-------------|
| **Partidas** | Total de partidas jugadas |
| **Victorias** | Número de partidas ganadas por GPT-OSS |
| **Derrotas** | Número de partidas perdidas |
| **Empates** | Número de partidas empatadas |
| **% Victoria** | Porcentaje de victorias (victorias/total) |
| **Normal/Anormal** | Partidas completadas correctamente vs con errores |
| **Tiempo Promedio** | Duración promedio por partida en segundos |
| **Tokens Promedio** | Número promedio de tokens consumidos |

## 🎨 Interpretación de Colores

### **Tasa de Victoria:**
- 🟢 **Verde** (≥60%): Excelente rendimiento
- 🟡 **Amarillo** (40-59%): Rendimiento moderado
- 🔴 **Rojo** (<40%): Bajo rendimiento

### **Badges de Configuración:**
- 🔵 **Azul**: Sin razonamiento
- 🟡 **Amarillo**: Razonamiento bajo
- 🔴 **Rojo**: Razonamiento medio

- 💙 **Azul claro**: Prompt Simple
- 💚 **Verde**: Chain of Thought (CoT)
- 💗 **Rosa**: Tree of Thoughts (ToT)

## 💡 Ejemplos

### **Comparar solo configuraciones sin razonamiento:**

```bash
./.venv/bin/python scripts/compare_configurations.py \
  experiments/test-no-reasoning-*/ \
  -o no_reasoning_comparison.html
```

### **Comparar solo estrategia CoT:**

```bash
./.venv/bin/python scripts/compare_configurations.py \
  experiments/test-*-cot/ \
  -o cot_comparison.html
```

### **Comparar razonamiento bajo:**

```bash
./.venv/bin/python scripts/compare_configurations.py \
  experiments/test-reasoning-low-*/ \
  -o low_reasoning_comparison.html
```

## 🔧 Solución de Problemas

### **Error: No se encontraron archivos JSONL**
- Verifica que las carpetas contengan archivos `.jsonl`
- Asegúrate de ejecutar los experimentos primero

### **Gráficos no se muestran**
- Verifica tu conexión a internet (Chart.js se carga desde CDN)
- O descarga Chart.js localmente

### **Configuraciones no detectadas correctamente**
- Verifica que los nombres de carpetas sigan el formato:
  - `test-[no-reasoning|reasoning-low|reasoning-medium]-[simple|cot|tot]`

## 📝 Notas

- El script funciona con cualquier juego de OpenSpiel compatible
- Los resultados se calculan automáticamente desde los archivos JSONL
- El HTML generado es completamente autónomo (excepto Chart.js)
- Puedes compartir el archivo HTML directamente

## 🎯 Próximos Pasos

Después de analizar el reporte:

1. **Identificar la mejor configuración** por juego
2. **Comparar eficiencia** (tokens vs rendimiento)
3. **Analizar trade-offs** (tiempo vs precisión)
4. **Optimizar configuraciones** basándose en resultados

---

**Generado por GTBench Analysis Tool**
