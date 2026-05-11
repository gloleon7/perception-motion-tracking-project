# Motion Tracking Project

Proyecto de la asignatura **Percepción en Automática y Robótica**.

El objetivo del proyecto es implementar y comparar técnicas de estimación de movimiento para realizar seguimiento visual de objetos en secuencias de vídeo.

---

## 1. Idea del proyecto

Este proyecto compara dos métodos de seguimiento de movimiento en vídeo:

1. **Diferencia de imágenes**
   - Compara frames consecutivos.
   - Detecta las zonas que han cambiado.
   - Extrae el contorno principal.
   - Calcula el centroide del objeto en movimiento.
   - Genera una trayectoria aproximada.

2. **Flujo óptico Lucas-Kanade**
   - Detecta puntos característicos de la imagen.
   - Sigue esos puntos entre frames consecutivos.
   - Calcula el desplazamiento de los puntos.
   - Permite estimar la dirección y magnitud del movimiento.

La idea principal no es solo aplicar los algoritmos, sino analizar su comportamiento en diferentes escenarios y comparar sus ventajas y limitaciones.

---

## 2. Relación con la asignatura

El proyecto está relacionado principalmente con:

- **Tema 3: Procesamiento de imágenes**
  - Conversión a escala de grises.
  - Filtrado gaussiano.
  - Umbralización.
  - Detección de contornos.
  - Procesamiento píxel a píxel y por vecindad.

- **Tema 5: Estimación de movimiento**
  - Diferencia de imágenes.
  - Flujo óptico.
  - Lucas-Kanade.
  - Seguimiento de objetos.
  - Cálculo de trayectorias.
  - Interpretación del movimiento en secuencias de imágenes.

También está relacionado con las prácticas de procesamiento de imágenes, detección de características y estimación de movimiento.

---

## 3. Ampliación respecto a las prácticas

En las prácticas se trabajan técnicas de procesamiento de imagen y estimación de movimiento de forma individual.

En este proyecto se amplían esas prácticas creando una pequeña aplicación completa que:

- Lee vídeos frame a frame.
- Detecta movimiento.
- Estima trayectorias.
- Compara dos métodos diferentes.
- Genera vídeos procesados.
- Calcula métricas de desplazamiento.
- Prueba distintos escenarios sintéticos.
- Analiza cuándo funciona mejor cada método.

Por tanto, el proyecto no se limita a repetir una práctica, sino que usa las técnicas vistas en clase para construir y evaluar un sistema completo de seguimiento visual.

---

## 4. Aplicación real

Este tipo de sistema puede aplicarse en:

- Robótica móvil.
- Detección de obstáculos dinámicos.
- Vigilancia automática.
- Seguimiento de personas.
- Seguimiento de vehículos.
- Análisis de movimiento en vídeo.
- Navegación visual.

La diferencia de imágenes puede ser útil para detectar rápidamente movimiento en una escena, mientras que Lucas-Kanade permite seguir puntos concretos y estimar desplazamientos de forma más detallada.

---

## 5. Métodos implementados

### 5.1. Diferencia de imágenes

El método compara dos frames consecutivos:

```text
motion = |frame_actual - frame_anterior|
```

Después se aplican los siguientes pasos:

1. Conversión a escala de grises.
2. Suavizado mediante filtro gaussiano.
3. Diferencia absoluta entre frames.
4. Umbralización.
5. Operaciones morfológicas para eliminar ruido.
6. Detección de contornos.
7. Selección del contorno principal.
8. Cálculo del centroide.
9. Dibujo de bounding box y trayectoria.

Este método es sencillo y rápido, pero puede fallar cuando hay cambios de iluminación, sombras o ruido.

---

### 5.2. Lucas-Kanade Optical Flow

Lucas-Kanade estima el movimiento de puntos característicos entre frames consecutivos.

El procedimiento seguido es:

1. Detectar puntos característicos en el primer frame.
2. Calcular el flujo óptico entre frames consecutivos.
3. Obtener la nueva posición de cada punto.
4. Dibujar las trayectorias de los puntos.
5. Calcular el desplazamiento medio en píxeles por frame.

Este método es más adecuado para seguir puntos concretos, aunque puede verse afectado por ruido o por movimientos demasiado rápidos.

---

## 6. Escenarios sintéticos

Para probar los métodos de forma controlada, se han generado varios vídeos sintéticos:

| Escenario | Archivo | Descripción |
|---|---|---|
| Clean | `synthetic_clean_circle.mp4` | Círculo moviéndose sobre fondo negro |
| Noisy | `synthetic_noisy_circle.mp4` | Círculo con ruido añadido |
| Light change | `synthetic_light_circle.mp4` | Círculo con cambios de iluminación y sombra |
| Fast motion | `synthetic_fast_circle.mp4` | Círculo moviéndose más rápido |

Estos escenarios permiten analizar la robustez de cada método ante condiciones distintas.

---

## 7. Estructura del proyecto

```text
motion-tracking-project/
│
├── data/
│   ├── input_videos/
│   └── synthetic_videos/
│
├── references/
│   ├── practices/
│   └── theory/
│
├── outputs/
│   ├── processed_videos/
│   ├── plots/
│   └── frames/
│
├── notebooks/
│   ├── 01_frame_difference_tracking.ipynb
│   ├── 02_lucas_kanade_tracking.ipynb
│   ├── 03_compare_methods_synthetic.ipynb
│   └── 04_analyze_synthetic_results.ipynb
│
├── src/
│   ├── generate_synthetic_video.py
│   ├── generate_synthetic_scenarios.py
│   └── run_synthetic_experiments.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 8. Instalación

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

## 9. Ejecución del proyecto

### 9.1. Generar vídeos sintéticos

```bash
python src/generate_synthetic_scenarios.py
```

Este comando genera los vídeos sintéticos dentro de:

```text
data/synthetic_videos/
```

---

### 9.2. Ejecutar todos los experimentos sintéticos

```bash
python src/run_synthetic_experiments.py
```

Este comando aplica los dos métodos a todos los escenarios sintéticos:

- Diferencia de imágenes.
- Lucas-Kanade.

También genera vídeos procesados, archivos CSV y una tabla resumen.

---

### 9.3. Analizar resultados en notebooks

Los notebooks se pueden ejecutar en este orden:

1. `01_frame_difference_tracking.ipynb`
2. `02_lucas_kanade_tracking.ipynb`
3. `03_compare_methods_synthetic.ipynb`
4. `04_analyze_synthetic_results.ipynb`

Estos notebooks permiten visualizar las trayectorias, desplazamientos y gráficas comparativas.

---

## 10. Salidas generadas

El proyecto genera archivos en la carpeta `outputs/`.

### Vídeos procesados

```text
outputs/processed_videos/
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

### Gráficas y datos

```text
outputs/plots/
```

Ejemplos:

```text
synthetic_experiments_summary.csv
summary_mean_displacement.png
summary_max_displacement.png
summary_detections.png
trajectory_comparison_synthetic.png
displacement_comparison_synthetic.png
```

---

## 11. Resultados obtenidos

Los primeros experimentos muestran que:

- En el escenario limpio, ambos métodos funcionan correctamente.
- La diferencia de imágenes permite detectar la región en movimiento y estimar una trayectoria mediante el centroide.
- Lucas-Kanade permite seguir puntos característicos y calcular el desplazamiento medio.
- En presencia de ruido, Lucas-Kanade puede seguir puntos inestables si aparecen características falsas.
- Con cambios de iluminación o sombras, la diferencia de imágenes empeora porque interpreta esos cambios como movimiento.
- En movimiento rápido, ambos métodos pueden funcionar, aunque aumenta el desplazamiento entre frames y Lucas-Kanade puede llegar a perder puntos si el movimiento es demasiado brusco.

---

## 12. Conclusiones preliminares

La diferencia de imágenes es un método sencillo, rápido y útil para detectar movimiento en escenas controladas. Sin embargo, es sensible a cambios de iluminación, sombras y ruido, ya que cualquier cambio entre frames puede ser interpretado como movimiento.

Lucas-Kanade ofrece un seguimiento más estable de puntos característicos, especialmente en escenarios limpios o con cambios moderados de iluminación. Sin embargo, puede verse afectado por ruido, pérdida de puntos o movimientos demasiado rápidos.

La comparación demuestra que no existe un método perfecto para todos los casos. La elección depende del tipo de escena, la calidad del vídeo y las condiciones de movimiento.

---

## 13. Próximos pasos

Los siguientes pasos del proyecto son:

1. Probar los métodos con vídeos reales grabados por el grupo.
2. Comparar los resultados reales con los escenarios sintéticos.
3. Añadir una tabla final de ventajas y limitaciones.
4. Preparar la memoria del proyecto.
5. Preparar la presentación final.

Los vídeos reales se colocarán en:

```text
data/input_videos/
```

Ejemplos recomendados:

```text
real_easy.mp4
real_person.mp4
real_shadow.mp4
```

---

## 14. Autores

Proyecto realizado para la asignatura **Percepción en Automática y Robótica**.

Grupo:

Gloria Leon y Maria Leal

---

## 15. Estado actual

Actualmente el proyecto incluye:

- Generación de vídeos sintéticos.
- Seguimiento mediante diferencia de imágenes.
- Seguimiento mediante Lucas-Kanade.
- Comparación entre métodos.
- Análisis de escenarios sintéticos.
- Gráficas y tablas resumen.

Pendiente:

- Incorporar vídeos reales.
- Redactar la memoria final.
- Preparar la presentación.