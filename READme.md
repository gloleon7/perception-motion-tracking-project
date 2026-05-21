# Seguimiento visual de objetos móviles en vídeo

Proyecto de la asignatura **Percepción en Automática y Robótica**.

El objetivo del proyecto es implementar y comparar técnicas de estimación de movimiento para el seguimiento visual de objetos móviles en secuencias de vídeo. La aplicación planteada está orientada a entornos interiores, donde este tipo de análisis puede ser útil para robótica móvil, vigilancia, análisis de movimiento o detección de obstáculos dinámicos.

---

## 1. Idea del proyecto

El proyecto compara dos métodos clásicos de estimación de movimiento:

1. **Diferencia de imágenes**
   - Compara frames consecutivos.
   - Detecta las zonas que han cambiado.
   - Extrae la región principal de movimiento.
   - Calcula el centroide del objeto o región móvil.
   - Permite estimar una trayectoria aproximada.

2. **Flujo óptico Lucas-Kanade**
   - Detecta puntos característicos en la imagen.
   - Sigue esos puntos entre frames consecutivos.
   - Calcula el desplazamiento de los puntos.
   - Permite estimar la dirección y magnitud del movimiento local.

La finalidad del proyecto es analizar cómo se comportan ambos métodos en diferentes condiciones: vídeo limpio, ruido, cambios de iluminación y movimiento rápido.

---

## 2. Relación con la asignatura

El proyecto está relacionado principalmente con los siguientes contenidos de la asignatura:

### Tema 3: Procesamiento de imágenes

- Conversión a escala de grises.
- Filtrado gaussiano.
- Umbralización.
- Detección de contornos.
- Procesamiento píxel a píxel y por vecindad.
- Extracción de características visuales.

### Tema 5: Estimación de movimiento

- Diferencia de imágenes.
- Procesamiento de secuencias de vídeo.
- Flujo óptico.
- Método de Lucas-Kanade.
- Seguimiento de objetos.
- Cálculo de trayectorias.
- Interpretación del movimiento en secuencias de imágenes.

También se relaciona con las prácticas de procesamiento de imágenes, detección de características y estimación de movimiento.

---

## 3. Aplicación real

Este tipo de análisis puede aplicarse en:

- Robótica móvil.
- Detección de obstáculos dinámicos.
- Vigilancia automática.
- Seguimiento de objetos.
- Seguimiento de personas.
- Navegación visual.
- Análisis de movimiento en escenas interiores.

La diferencia de imágenes puede ser útil para detectar rápidamente zonas de movimiento. Lucas-Kanade, por su parte, permite seguir puntos concretos y estimar desplazamientos locales con mayor estabilidad en algunos escenarios.

---

## 4. Dataset utilizado

El proyecto utiliza un **dataset propio**, dividido en dos partes:

1. **Vídeos sintéticos generados por código**
   - Permiten validar los algoritmos en condiciones controladas.
   - Se usan para estudiar casos concretos como ruido, cambios de iluminación y movimiento rápido.

2. **Vídeos reales grabados por el grupo**
   - Permiten probar los métodos en una situación más cercana a una aplicación real.
   - Se graban con cámara fija, fondo relativamente estable y un objeto móvil con textura.
   - Para cada escenario real se utilizan dos tomas diferentes, con el objetivo de no basar el análisis en un único ejemplo.

---

## 5. Vídeos sintéticos

Los vídeos sintéticos se generan mediante código Python y OpenCV.

| Archivo | Escenario | Objetivo |
|---|---|---|
| `synthetic_clean_circle.mp4` | Caso limpio | Validación básica |
| `synthetic_noisy_circle.mp4` | Ruido | Robustez ante ruido |
| `synthetic_light_circle.mp4` | Cambio de iluminación | Robustez ante variaciones de luz |
| `synthetic_fast_circle.mp4` | Movimiento rápido | Análisis de limitaciones ante desplazamientos rápidos |

Estos vídeos permiten comprobar que los métodos funcionan correctamente en condiciones controladas antes de aplicarlos a vídeos reales.

---

## 6. Vídeos reales

Los vídeos reales se colocan en:

```text
data/input_videos/
```

La configuración prevista utiliza dos vídeos por escenario:

| Archivo | Escenario | Objetivo |
|---|---|---|
| `real_normal_1.mp4` | Movimiento normal | Validación real básica |
| `real_normal_2.mp4` | Movimiento normal | Segunda toma del caso normal |
| `real_noisy_1.mp4` | Vídeo con ruido | Robustez ante ruido |
| `real_noisy_2.mp4` | Vídeo con ruido | Segunda toma con ruido |
| `real_light_change_1.mp4` | Cambio de iluminación | Robustez ante variaciones de luz |
| `real_light_change_2.mp4` | Cambio de iluminación | Segunda toma con cambio de luz |
| `real_fast_1.mp4` | Movimiento rápido | Análisis de limitaciones ante movimiento rápido |
| `real_fast_2.mp4` | Movimiento rápido | Segunda toma con movimiento rápido |

Los vídeos con ruido pueden generarse automáticamente a partir de los vídeos normales mediante el script:

```bash
python src/create_noisy_real_video.py
```

De esta forma, el ruido añadido es controlado y reproducible.

---

## 7. Métodos implementados

### 7.1. Diferencia de imágenes

El método compara dos frames consecutivos:

```text
motion = |frame_actual - frame_anterior|
```

Después se aplican los siguientes pasos:

1. Conversión a escala de grises.
2. Suavizado mediante filtro gaussiano.
3. Diferencia absoluta entre frames.
4. Umbralización.
5. Operaciones morfológicas para limpiar la máscara.
6. Detección de contornos.
7. Selección del contorno principal.
8. Cálculo del centroide.
9. Dibujo del bounding box y centroide.
10. Exportación de métricas.

Este método es sencillo y rápido, pero puede fallar cuando hay cambios de iluminación, sombras, ruido o movimiento de elementos secundarios.

---

### 7.2. Lucas-Kanade Optical Flow

Lucas-Kanade estima el movimiento de puntos característicos entre frames consecutivos.

El procedimiento seguido es:

1. Detectar puntos característicos.
2. Calcular el flujo óptico entre frames consecutivos.
3. Obtener la nueva posición de cada punto.
4. Dibujar los desplazamientos recientes.
5. Calcular el desplazamiento de los puntos.
6. Exportar métricas para análisis.

Este método es más adecuado para seguir puntos concretos, aunque puede verse afectado por ruido, cambios bruscos de iluminación o movimientos demasiado rápidos.

---

## 8. Métricas utilizadas

Para comparar ambos métodos se calculan varias métricas:

| Métrica | Descripción |
|---|---|
| `detections` | Número de frames o detecciones procesadas |
| `mean_displacement` | Desplazamiento medio |
| `median_displacement` | Mediana del desplazamiento |
| `p95_displacement` | Percentil 95 del desplazamiento |
| `max_displacement` | Desplazamiento máximo |
| `mean_area` | Área media detectada por diferencia de imágenes |
| `mean_points_per_frame` | Número medio de puntos seguidos por Lucas-Kanade |

La mediana y el percentil 95 son especialmente útiles en vídeos reales, porque el desplazamiento máximo puede verse afectado por errores puntuales u outliers.

---

## 9. Estructura del proyecto

```text
motion-tracking-project/
│
├── data/
│   ├── input_videos/
│   ├── synthetic_videos/
│   └── dataset_description.csv
│
├── references/
│   ├── practices/
│   └── theory/
│
├── outputs/
│   ├── processed_videos/
│   │   ├── synthetic/
│   │   └── real/
│   │
│   ├── plots/
│   │   ├── synthetic/
│   │   └── real/
│   │
│   └── frames/
│
├── notebooks/
│   ├── 01_frame_difference_tracking.ipynb
│   ├── 02_lucas_kanade_tracking.ipynb
│   ├── 03_compare_methods_synthetic.ipynb
│   ├── 04_analyze_synthetic_results.ipynb
│   └── 05_analyze_real_results.ipynb
│
├── src/
│   ├── create_noisy_real_video.py
│   ├── generate_synthetic_video.py
│   ├── generate_synthetic_scenarios.py
│   ├── run_synthetic_experiments.py
│   └── run_real_experiments.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 10. Instalación

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activar el entorno en Windows:

```bash
.venv\Scripts\activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Si todavía no existe el archivo `requirements.txt`, se puede generar con:

```bash
pip freeze > requirements.txt
```

---

## 11. Ejecución del proyecto

### 11.1. Generar vídeos sintéticos

```bash
python src/generate_synthetic_scenarios.py
```

Este comando genera los vídeos sintéticos en:

```text
data/synthetic_videos/
```

---

### 11.2. Ejecutar experimentos sintéticos

```bash
python src/run_synthetic_experiments.py
```

Este script procesa todos los vídeos sintéticos con:

- diferencia de imágenes;
- Lucas-Kanade.

Los resultados se guardan en:

```text
outputs/processed_videos/synthetic/
outputs/plots/synthetic/
```

---

### 11.3. Generar vídeos reales con ruido

Si se quieren generar los vídeos con ruido a partir de las tomas normales:

```bash
python src/create_noisy_real_video.py
```

Los vídeos generados se guardan en:

```text
data/input_videos/
```

---

### 11.4. Ejecutar experimentos reales

```bash
python src/run_real_experiments.py
```

Este script procesa los vídeos reales con:

- diferencia de imágenes;
- Lucas-Kanade.

Los resultados se guardan en:

```text
outputs/processed_videos/real/
outputs/plots/real/
```

---

## 12. Notebooks

Los notebooks se pueden ejecutar en este orden:

1. `01_frame_difference_tracking.ipynb`
2. `02_lucas_kanade_tracking.ipynb`
3. `03_compare_methods_synthetic.ipynb`
4. `04_analyze_synthetic_results.ipynb`
5. `05_analyze_real_results.ipynb`

| Notebook | Descripción |
|---|---|
| `01_frame_difference_tracking.ipynb` | Explica y prueba el método de diferencia de imágenes |
| `02_lucas_kanade_tracking.ipynb` | Explica y prueba el método Lucas-Kanade |
| `03_compare_methods_synthetic.ipynb` | Compara ambos métodos en el caso sintético base |
| `04_analyze_synthetic_results.ipynb` | Analiza todos los escenarios sintéticos |
| `05_analyze_real_results.ipynb` | Analiza todos los vídeos reales |

---

## 13. Salidas generadas

### Vídeos procesados sintéticos

```text
outputs/processed_videos/synthetic/
```

Ejemplos:

```text
frame_difference_clean.mp4
lucas_kanade_clean.mp4
frame_difference_noisy.mp4
lucas_kanade_noisy.mp4
frame_difference_light_change.mp4
lucas_kanade_light_change.mp4
frame_difference_fast_motion.mp4
lucas_kanade_fast_motion.mp4
```

### Vídeos procesados reales

```text
outputs/processed_videos/real/
```

Ejemplos:

```text
frame_difference_real_normal_1.mp4
lucas_kanade_real_normal_1.mp4
frame_difference_real_normal_2.mp4
lucas_kanade_real_normal_2.mp4
```

### Gráficas y datos sintéticos

```text
outputs/plots/synthetic/
```

Ejemplos:

```text
synthetic_experiments_summary.csv
summary_mean_displacement.png
summary_median_displacement.png
summary_p95_displacement.png
summary_max_displacement.png
summary_detections.png
```

### Gráficas y datos reales

```text
outputs/plots/real/
```

Ejemplos:

```text
real_experiments_summary.csv
real_mean_displacement.png
real_median_displacement.png
real_p95_displacement.png
real_max_displacement.png
real_detections.png
real_frame_difference_mean_area.png
real_lucas_kanade_mean_points.png
```

---

## 14. Resultados esperados

En los vídeos sintéticos se espera que ambos métodos funcionen correctamente en el caso limpio. En los escenarios con ruido, cambio de iluminación y movimiento rápido aparecen diferencias entre métodos.

En los vídeos reales, Lucas-Kanade suele proporcionar un seguimiento más estable de puntos característicos, especialmente si el objeto tiene textura. La diferencia de imágenes permite detectar regiones móviles, pero puede ser más sensible a sombras, cambios de iluminación o movimientos de otros elementos de la escena.

---

## 15. Limitaciones observadas

Durante las pruebas se han observado varias limitaciones:

- La diferencia de imágenes no detecta objetos como tal, sino zonas cambiantes.
- Los cambios de iluminación pueden interpretarse como movimiento.
- Las sombras pueden generar falsas detecciones.
- Lucas-Kanade puede perder puntos si el movimiento es muy rápido.
- El ruido puede generar puntos característicos falsos.
- El desplazamiento máximo puede estar afectado por outliers.

Por este motivo, se utilizan métricas robustas como la mediana y el percentil 95.

---

## 16. Conclusiones preliminares

La diferencia de imágenes es un método sencillo, rápido y útil para detectar movimiento en escenas controladas. Sin embargo, es sensible a cambios de iluminación, sombras, ruido y movimientos secundarios.

Lucas-Kanade ofrece un seguimiento más estable de puntos característicos, especialmente en escenarios normales o con ruido moderado. Aun así, también presenta limitaciones ante cambios bruscos de iluminación, pérdida de puntos o movimientos rápidos.

La comparación muestra que no existe un método perfecto para todos los casos. La elección depende del tipo de escena, la calidad del vídeo y las condiciones de movimiento.

---

## 17. Autoras

Proyecto realizado para la asignatura **Percepción en Automática y Robótica**.

Grupo:

- Gloria León
- María Leal