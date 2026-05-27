# Seguimiento visual de objetos móviles en vídeo

Proyecto de la asignatura **Percepción en Automática y Robótica**.

El objetivo del proyecto es implementar y comparar técnicas clásicas de estimación de movimiento para el seguimiento visual de objetos móviles en secuencias de vídeo. El trabajo se centra en analizar el comportamiento de dos métodos: **diferencia de imágenes** y **flujo óptico Lucas-Kanade**.

La aplicación planteada está orientada a escenas con cámara fija, donde se desea detectar y analizar movimiento de forma sencilla. Este tipo de sistema puede ser útil en vigilancia automática, análisis de movimiento, seguimiento de objetos, detección de actividad en una escena o como etapa previa en sistemas de percepción para robótica.

---

## 1. Idea del proyecto

El proyecto compara dos métodos clásicos de estimación de movimiento:

### 1.1. Diferencia de imágenes

La diferencia de imágenes compara frames consecutivos para detectar qué zonas de la imagen han cambiado.

Este método permite:

- detectar regiones móviles;
- extraer el contorno principal de movimiento;
- calcular un bounding box;
- obtener el centroide de la región detectada;
- estimar una trayectoria aproximada del objeto o región móvil.

Es un método sencillo y rápido, pero sensible a ruido, sombras, cambios de iluminación y elementos secundarios que también puedan moverse en la escena.

### 1.2. Flujo óptico Lucas-Kanade

Lucas-Kanade es un método de flujo óptico que sigue puntos característicos entre frames consecutivos.

Este método permite:

- detectar puntos relevantes en la imagen;
- seguir esos puntos a lo largo del vídeo;
- calcular el desplazamiento de cada punto;
- estimar la dirección y magnitud del movimiento local;
- analizar la estabilidad del seguimiento mediante el número de puntos mantenidos.

A diferencia de la diferencia de imágenes, Lucas-Kanade no trabaja con una región completa, sino con puntos característicos. Por eso puede ser más estable en algunas escenas, aunque depende de que existan puntos con textura suficiente.

---

## 2. Objetivo del proyecto

El objetivo principal es comparar ambos métodos bajo diferentes condiciones de vídeo para estudiar su robustez.

Las condiciones evaluadas son:

- movimiento normal;
- vídeo con ruido;
- cambios de iluminación;
- movimiento rápido.

A partir de estas condiciones se pretende responder a la siguiente pregunta:

> ¿Qué método mantiene una estimación de movimiento más estable cuando cambian las condiciones de la escena?

---

## 3. Relación con la asignatura

El proyecto está relacionado principalmente con los contenidos de procesamiento de imágenes y estimación de movimiento vistos en la asignatura.

### Tema 3: Procesamiento de imágenes

El proyecto utiliza conceptos como:

- conversión a escala de grises;
- filtrado gaussiano;
- umbralización;
- operaciones morfológicas;
- detección de contornos;
- extracción de características visuales;
- procesamiento píxel a píxel y por vecindad.

### Tema 5: Estimación de movimiento

El proyecto también aplica contenidos de estimación de movimiento, como:

- diferencia de imágenes;
- procesamiento de secuencias de vídeo;
- flujo óptico;
- método de Lucas-Kanade;
- seguimiento de puntos;
- cálculo de trayectorias;
- análisis del desplazamiento entre frames.

---

## 4. Aplicación real

Una aplicación sencilla del proyecto sería una cámara fija situada en una escena cotidiana, por ejemplo la entrada de una vivienda, una mesa de trabajo o una zona de paso.

El sistema no necesita reconocer exactamente qué objeto aparece en la imagen. Su objetivo es detectar que existe movimiento y estimar cómo se desplaza.

Por ejemplo, una cámara podría detectar:

- una persona acercándose a una puerta;
- un objeto moviéndose sobre una mesa;
- un paquete siendo colocado en una entrada;
- actividad en una zona vigilada;
- movimiento en una escena interior controlada.

La diferencia de imágenes puede utilizarse como una primera etapa para detectar actividad en la escena. Lucas-Kanade puede complementar este análisis siguiendo puntos concretos y estimando desplazamientos más localizados.

---

## 5. Dataset utilizado

El proyecto utiliza un dataset propio, dividido en dos partes:

1. **Vídeos sintéticos generados por código**
2. **Vídeos reales**

Esta división permite analizar primero los métodos en un entorno controlado y después probarlos en vídeos reales, donde aparecen condiciones más cercanas a una aplicación práctica.

---

## 6. Vídeos sintéticos

Los vídeos sintéticos se generan mediante Python y OpenCV.

Estos vídeos permiten controlar el movimiento, la forma del objeto y las condiciones de la escena. De esta forma se puede comprobar que los métodos funcionan correctamente antes de pasar a vídeos reales.

| Archivo | Escenario | Objetivo |
|---|---|---|
| `synthetic_clean_circle.mp4` | Caso limpio | Validación básica del movimiento |
| `synthetic_noisy_circle.mp4` | Ruido | Evaluar robustez ante ruido |
| `synthetic_light_circle.mp4` | Cambio de iluminación | Evaluar sensibilidad ante variaciones de luz |
| `synthetic_fast_circle.mp4` | Movimiento rápido | Analizar el comportamiento ante desplazamientos rápidos |

Los escenarios sintéticos permiten observar el comportamiento de los algoritmos en condiciones controladas. Esto resulta útil porque el movimiento esperado es conocido y las diferencias entre escenarios están introducidas de forma intencionada.

---

## 7. Vídeos reales

Los vídeos reales se colocan en la carpeta:

```text
data/input_videos/
```

El conjunto real final está formado por cuatro condiciones de prueba:

- movimiento normal;
- ruido;
- cambio de iluminación;
- movimiento rápido.

Para cada condición se utilizan cuatro escenarios reales, numerados del `1` al `4`.

| Archivo | Escenario | Objetivo |
|---|---|---|
| `real_normal_1.mp4` | Movimiento normal | Validación real básica |
| `real_normal_2.mp4` | Movimiento normal | Segunda toma del caso normal |
| `real_normal_3.mp4` | Movimiento normal | Tercera toma del caso normal |
| `real_normal_4.mp4` | Movimiento normal | Cuarta toma del caso normal |
| `real_noisy_1.mp4` | Vídeo con ruido | Evaluar robustez ante ruido |
| `real_noisy_2.mp4` | Vídeo con ruido | Segunda toma con ruido |
| `real_noisy_3.mp4` | Vídeo con ruido | Tercera toma con ruido |
| `real_noisy_4.mp4` | Vídeo con ruido | Cuarta toma con ruido |
| `real_light_change_1.mp4` | Cambio de iluminación | Evaluar sensibilidad ante variaciones de luz |
| `real_light_change_2.mp4` | Cambio de iluminación | Segunda toma con cambio de luz |
| `real_light_change_3.mp4` | Cambio de iluminación | Tercera toma con cambio de luz |
| `real_light_change_4.mp4` | Cambio de iluminación | Cuarta toma con cambio de luz |
| `real_fast_1.mp4` | Movimiento rápido | Evaluar el comportamiento ante movimiento rápido |
| `real_fast_2.mp4` | Movimiento rápido | Segunda toma con movimiento rápido |
| `real_fast_3.mp4` | Movimiento rápido | Tercera toma con movimiento rápido |
| `real_fast_4.mp4` | Movimiento rápido | Cuarta toma con movimiento rápido |

Las versiones con ruido, cambio de iluminación y movimiento rápido se generan a partir de los vídeos normales. De esta forma, los escenarios modificados parten de una base visual comparable, y el cambio principal entre vídeos es la condición evaluada: ruido, luminosidad o velocidad.

---

## 8. Métodos implementados

## 8.1. Diferencia de imágenes

El método de diferencia de imágenes compara dos frames consecutivos:

```text
motion = |frame_actual - frame_anterior|
```

El pipeline seguido es:

1. Leer el vídeo frame a frame.
2. Convertir cada frame a escala de grises.
3. Aplicar un filtro gaussiano para suavizar ruido.
4. Calcular la diferencia absoluta entre el frame actual y el anterior.
5. Aplicar un umbral para obtener una máscara binaria de movimiento.
6. Aplicar operaciones morfológicas para limpiar la máscara.
7. Detectar contornos.
8. Seleccionar el contorno principal.
9. Calcular el bounding box y el centroide.
10. Guardar el vídeo procesado y las métricas obtenidas.

Este método permite detectar regiones móviles de forma directa. Sin embargo, no distingue si el cambio se debe a un objeto en movimiento, una sombra, ruido o una variación global de iluminación.

---

## 8.2. Lucas-Kanade Optical Flow

Lucas-Kanade estima el movimiento de puntos característicos entre frames consecutivos.

El pipeline seguido es:

1. Leer el vídeo frame a frame.
2. Convertir el primer frame a escala de grises.
3. Detectar puntos característicos.
4. Calcular el flujo óptico entre el frame anterior y el frame actual.
5. Obtener la nueva posición de cada punto.
6. Calcular el desplazamiento de cada punto.
7. Dibujar las líneas de desplazamiento y los puntos seguidos.
8. Re-detectar puntos si el seguimiento se pierde.
9. Guardar el vídeo procesado y las métricas obtenidas.

Este método permite analizar el movimiento de forma más localizada. Su rendimiento depende de que existan puntos característicos suficientes y de que el desplazamiento entre frames no sea demasiado brusco.

---

## 9. Métricas utilizadas

Para comparar ambos métodos se calculan varias métricas.

| Métrica | Descripción |
|---|---|
| `detections` | Número de detecciones o frames con información útil |
| `mean_displacement` | Desplazamiento medio |
| `median_displacement` | Mediana del desplazamiento |
| `p95_displacement` | Percentil 95 del desplazamiento |
| `max_displacement` | Desplazamiento máximo |
| `mean_area` | Área media detectada por diferencia de imágenes |
| `mean_points_per_frame` | Número medio de puntos seguidos por Lucas-Kanade |

La media y el máximo pueden verse afectados por errores puntuales. Por eso, en el análisis se da especial importancia a:

- **mediana del desplazamiento**, porque representa el comportamiento típico del método;
- **percentil 95**, porque permite detectar saltos grandes sin depender solo del máximo;
- **área media**, para estudiar cómo responde la diferencia de imágenes;
- **puntos medios por frame**, para estudiar la calidad del seguimiento de Lucas-Kanade.

---

## 10. Estructura del proyecto

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

## 11. Instalación

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activar el entorno en Windows:

```bash
.venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## 12. Ejecución del proyecto

### 12.1. Generar vídeos sintéticos

```bash
python src/generate_synthetic_scenarios.py
```

Los vídeos generados se guardan en:

```text
data/synthetic_videos/
```

---

### 12.2. Ejecutar experimentos sintéticos

```bash
python src/run_synthetic_experiments.py
```

Este script procesa todos los vídeos sintéticos con los dos métodos:

- diferencia de imágenes;
- Lucas-Kanade.

Los resultados se guardan en:

```text
outputs/processed_videos/synthetic/
outputs/plots/synthetic/
```

---

### 12.3. Ejecutar experimentos reales

```bash
python src/run_real_experiments.py
```

Este script procesa todos los vídeos reales disponibles en:

```text
data/input_videos/
```

Los resultados se guardan en:

```text
outputs/processed_videos/real/
outputs/plots/real/
```

---

## 13. Notebooks

Los notebooks se pueden ejecutar en este orden:

| Notebook | Descripción |
|---|---|
| `01_frame_difference_tracking.ipynb` | Explica y prueba el método de diferencia de imágenes |
| `02_lucas_kanade_tracking.ipynb` | Explica y prueba el método Lucas-Kanade |
| `03_compare_methods_synthetic.ipynb` | Compara ambos métodos en el caso sintético base |
| `04_analyze_synthetic_results.ipynb` | Analiza todos los escenarios sintéticos |
| `05_analyze_real_results.ipynb` | Analiza todos los vídeos reales |

---

## 14. Salidas generadas

### 14.1. Vídeos procesados sintéticos

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

---

### 14.2. Vídeos procesados reales

```text
outputs/processed_videos/real/
```

Ejemplos:

```text
frame_difference_real_normal_1.mp4
lucas_kanade_real_normal_1.mp4
frame_difference_real_noisy_1.mp4
lucas_kanade_real_noisy_1.mp4
frame_difference_real_light_change_1.mp4
lucas_kanade_real_light_change_1.mp4
frame_difference_real_fast_1.mp4
lucas_kanade_real_fast_1.mp4
```

---

### 14.3. Resultados sintéticos

```text
outputs/plots/synthetic/
```

Ejemplos:

```text
synthetic_experiments_summary.csv
synthetic_median_displacement.png
synthetic_p95_displacement.png
synthetic_mean_displacement.png
synthetic_max_displacement.png
synthetic_detections.png
```

---

### 14.4. Resultados reales

```text
outputs/plots/real/
```

Ejemplos:

```text
real_experiments_summary.csv
real_median_displacement.png
real_p95_displacement.png
real_mean_displacement.png
real_max_displacement.png
real_detections.png
real_frame_difference_mean_area.png
real_lucas_kanade_mean_points.png
```

---

## 15. Análisis de resultados

Los resultados se analizan a partir de los archivos CSV generados por los scripts de experimentación.

Para los vídeos sintéticos:

```text
outputs/plots/synthetic/synthetic_experiments_summary.csv
```

Para los vídeos reales:

```text
outputs/plots/real/real_experiments_summary.csv
```

El análisis compara los dos métodos en función de las métricas obtenidas. No se utiliza únicamente la media del desplazamiento, ya que puede verse afectada por errores puntuales. Por este motivo, se da mayor importancia a la mediana y al percentil 95.

En términos generales:

- la diferencia de imágenes es sencilla, rápida y útil para detectar movimiento;
- la diferencia de imágenes es sensible a ruido, sombras y cambios de iluminación;
- Lucas-Kanade permite seguir puntos concretos de la escena;
- Lucas-Kanade suele ofrecer un seguimiento más estable si hay suficientes puntos con textura;
- Lucas-Kanade puede perder puntos en movimientos rápidos o escenas con poca textura.

---

## 16. Limitaciones observadas

Durante el desarrollo se han identificado varias limitaciones:

- La diferencia de imágenes no detecta objetos como tal, sino zonas cambiantes.
- Los cambios de iluminación pueden interpretarse como movimiento.
- Las sombras pueden generar falsas detecciones.
- El ruido puede provocar regiones de movimiento no deseadas.
- Lucas-Kanade depende de la calidad de los puntos característicos.
- Lucas-Kanade puede perder puntos si el movimiento es rápido.
- El desplazamiento máximo puede estar muy influido por outliers.
- Las escenas reales son más difíciles de analizar que las sintéticas porque incluyen textura, iluminación y movimiento menos controlados.

Estas limitaciones no invalidan el sistema, sino que ayudan a entender en qué condiciones funciona mejor cada método.

---

## 17. Conclusiones

La diferencia de imágenes permite detectar movimiento de forma sencilla y rápida. Es un método útil como primera aproximación, especialmente en escenas con cámara fija y condiciones controladas. Sin embargo, su principal limitación es que cualquier cambio visual puede aparecer como movimiento, aunque no corresponda realmente al objeto que se quiere seguir.

Lucas-Kanade ofrece un seguimiento más localizado mediante puntos característicos. Esto permite analizar el desplazamiento de forma más fina, aunque su rendimiento depende de que la escena tenga textura suficiente y de que los puntos no se pierdan entre frames.

La comparación muestra que no existe un método perfecto para todos los casos. La elección depende del tipo de escena, la iluminación, el ruido, la velocidad del movimiento y la textura disponible.

Una mejora natural del sistema sería combinar ambos enfoques: utilizar diferencia de imágenes para localizar regiones móviles y Lucas-Kanade para seguir puntos dentro de esas regiones.

---

## 18. Trabajo futuro

Como posibles mejoras futuras se plantean:

- combinar diferencia de imágenes y Lucas-Kanade en un único pipeline;
- aplicar seguimiento solo dentro de la región móvil detectada;
- añadir estabilización frente a cambios de iluminación;
- filtrar outliers en los desplazamientos;
- comparar con métodos más avanzados de tracking;
- añadir detección semántica mediante modelos de visión por computador;
- probar el sistema en vídeos más largos y variados.

---

## 19. Autoras

Proyecto realizado para la asignatura **Percepción en Automática y Robótica**.

Grupo:

- Gloria León
- María Leal