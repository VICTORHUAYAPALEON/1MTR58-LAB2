# 1MTR58 – Laboratorio 2

**Fundamentos y Aplicaciones de Biomecatrónica – PUCP**  
Semestre 2026-2

## Tema
Reconocimiento de patrones aplicado a **Eye Tracking** y **electrooculografía (EOG)**.

## Archivos principales

- `01_EyeTracking.ipynb`: Experiencia 1 – detección ocular, cálculo de EAR, calibración, PERCLOS y pruebas de robustez.
- `02_EOG_Procesamiento.ipynb`: Experiencia 2 – carga, exploración, construcción de EOGh/EOGv, preprocesamiento, segmentación, ventaneo y extracción de características.
- `03_GripperVirtual.py`: HMI para demostrar la acción del clasificador sobre un gripper virtual.
- `hmi_demo.csv`: archivo de prueba para verificar el funcionamiento de la HMI.
- `data/`: archivos EOG utilizados durante la sesión.
- `requirements.txt`: dependencias del laboratorio.

## Preparación del entorno

Se recomienda trabajar con **Python 3.11 o 3.12**.

1. Abra el notebook `.ipynb` en Visual Studio Code.
2. Seleccione Python 3.11 o 3.12 como intérprete.
3. Si VS Code lo solicita, cree un entorno virtual (`venv`).
4. Seleccione ese mismo entorno como **kernel** del notebook.
5. Ejecute la primera celda; esta verificará e instalará las librerías necesarias.
6. Si se instalaron dependencias, reinicie el kernel y ejecute nuevamente desde el inicio.

> El kernel debe corresponder al mismo entorno virtual donde se instalaron las librerías.

## Trabajo durante la sesión

### Experiencia 1 – Eye Tracking

Se trabajará con detección facial y ocular, cálculo de EAR, calibración del umbral, PERCLOS y evaluación de distintas condiciones de captura.

### Experiencia 2 – EOG

Se trabajará con el sujeto S1 hasta obtener un `features_df` y comparar características entre clases.

Flujo general:

`Carga → exploración → EOGh/EOGv → preprocesamiento → segmentación → ventaneo → características`

## Trabajo para el informe

A partir de los datos de los siete sujetos, cada grupo deberá:

- entrenar y comparar al menos dos modelos supervisados;
- reservar un sujeto para evaluación;
- seleccionar y evaluar el modelo final;
- exportar el modelo y los objetos de preprocesamiento necesarios;
- integrar el resultado con `03_GripperVirtual.py` como prueba de concepto de HMI.

El código desarrollado para el informe debe mantenerse en el repositorio GitHub del grupo.

## HMI

La correspondencia utilizada en la demostración es:

- Clase 1: saccade outward → **abrir**.
- Clase 2: return saccade → **cerrar**.
- Clase 3: blink → **rotar / confirmar**.

`hmi_demo.csv` permite probar la interfaz sin utilizar todavía un modelo entrenado.
