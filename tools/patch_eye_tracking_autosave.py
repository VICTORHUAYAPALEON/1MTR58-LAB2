import json
from pathlib import Path

NB = Path("01_EyeTracking.ipynb")
nb = json.loads(NB.read_text(encoding="utf-8"))


def cell(cell_id):
    for c in nb["cells"]:
        if c.get("id") == cell_id:
            return c
    raise KeyError(cell_id)


def get(c):
    return "".join(c["source"])


def put(c, text):
    c["source"] = text.splitlines(keepends=True)


# ------------------------------------------------------------------
# Instrucciones generales: ahora la evidencia se guarda automáticamente
# ------------------------------------------------------------------
c = cell("20d0f122")
s = get(c)
s = s.replace(
    "Para el reporte, tomar la captura directamente durante cada prueba. Los datos también se guardan en `.csv` por si se necesitan revisar después.",
    "Al finalizar cada prueba, el notebook guarda automáticamente un archivo `.png` con la ventana mostrada y un archivo `.csv` con los datos en `resultados_eye_tracking/`."
)
put(c, s)

# ------------------------------------------------------------------
# Función principal run_ear_session
# ------------------------------------------------------------------
c = cell("9ebcfdfa")
s = get(c)

s = s.replace(
    "    save_outputs=True,\n):",
    "    save_outputs=True,\n    participant_name=None,\n):"
)

s = s.replace(
    "    La captura para el reporte debe hacerse directamente durante la ejecución.\n    Presionar q para terminar.",
    "    Al finalizar el registro se guarda automáticamente un PNG con la ventana mostrada, además del CSV.\n    Presionar q para terminar."
)

s = s.replace(
    "    condition_name = str(condition_name)\n    file_tag = _safe_name(condition_name)\n    stamp = datetime.now().strftime(\"%Y%m%d_%H%M%S\")",
    "    condition_name = str(condition_name)\n\n    if participant_name is None:\n        participant_name = input(\"Nombre o código del integrante: \" ).strip()\n\n    participant_name = participant_name.strip() if participant_name else \"sin_nombre\"\n    file_tag = _safe_name(f\"{condition_name}_{participant_name}\")\n    stamp = datetime.now().strftime(\"%Y%m%d_%H%M%S\")"
)

s = s.replace(
    "    user_quit = False\n",
    "    user_quit = False\n    last_capture = None\n",
    1
)

s = s.replace(
    "        print(f\"\\n[{condition_name}] CALIBRACIÓN: mantén los ojos abiertos.\")",
    "        print(f\"\\n[{condition_name}] Integrante: {participant_name}\")\n        print(f\"[{condition_name}] CALIBRACIÓN: mantén los ojos abiertos.\")"
)

s = s.replace(
    "            \"Parpadea normalmente y toma el screenshot cuando desees.\"",
    "            \"Parpadea normalmente. La imagen PNG se guardará automáticamente.\""
)

s = s.replace(
    "                \"Screenshot: captura esta ventana | q: salir\",",
    "                \"PNG + CSV se guardan automaticamente | q: salir\","
)

# Guardar el último frame combinado del REGISTRO (segunda aparición del bloque)
needle = "            combined = _combine_camera_and_plot(frame, plot_img)\n            cv2.imshow(window_name, combined)"
first = s.find(needle)
second = s.find(needle, first + 1) if first != -1 else -1
if second == -1:
    raise RuntimeError("No se encontró el bloque de registro para insertar last_capture")
s = s[:second] + s[second:].replace(
    needle,
    "            combined = _combine_camera_and_plot(frame, plot_img)\n            last_capture = combined.copy()\n            cv2.imshow(window_name, combined)",
    1
)

s = s.replace(
    "    result = {\n        \"condicion\": condition_name,",
    "    result = {\n        \"integrante\": participant_name,\n        \"condicion\": condition_name,"
)

old_save = '''    if save_outputs:\n        csv_path = OUTPUT_DIR / f"{stamp}_{file_tag}.csv"\n        df.to_csv(csv_path, index=False)\n        print(f"CSV guardado: {csv_path}")\n\n    # No se crea una gráfica al terminar:\n    # la evidencia es el screenshot de la ventana en vivo.\n'''
new_save = '''    if save_outputs:\n        csv_path = OUTPUT_DIR / f"{stamp}_{file_tag}.csv"\n        df.to_csv(csv_path, index=False)\n        print(f"CSV guardado: {csv_path}")\n\n        if last_capture is not None:\n            png_path = OUTPUT_DIR / f"{stamp}_{file_tag}.png"\n            ok = cv2.imwrite(str(png_path), last_capture)\n            if ok:\n                result["archivo_png"] = str(png_path)\n                print(f"PNG guardado: {png_path}")\n            else:\n                print("Advertencia: no se pudo guardar la imagen PNG.")\n\n'''
if old_save not in s:
    raise RuntimeError("No se encontró el bloque final de guardado")
s = s.replace(old_save, new_save)
put(c, s)

# ------------------------------------------------------------------
# 1.1: cada integrante ejecuta la prueba y obtiene su PNG
# ------------------------------------------------------------------
c = cell("4b9faa0f")
put(c, """# 1. Experiencia 1 – Detección de parpadeo y evaluación de robustez\n\n## 1.1 Detección y calibración del EAR\n\n**Cada integrante** debe realizar esta prueba una vez, en posición frontal y sin lentes.\n\nEjecute la celda una vez por integrante. Al finalizar cada ejecución se guardará automáticamente un `.png` con la cámara, la señal EAR y el umbral obtenido.\n""")

c = cell("49850411")
put(c, '''# 1.1 – Ejecutar ESTA CELDA una vez por integrante\nintegrante_11 = input("Nombre o código del integrante: ").strip()\n\nresultado_11, datos_11 = run_ear_session(\n    condition_name="1.1_Frontal_sin_lentes",\n    calibration_time=4,\n    record_time=20,\n    participant_name=integrante_11,\n)\n''')

c = cell("ff7782ec")
put(c, """### Para el reporte\n\nAdjuntar el `.png` generado para cada integrante y describir brevemente qué ocurre con el valor de EAR durante un parpadeo.\n""")

# ------------------------------------------------------------------
# 1.2.1 y 1.2.2: mismo integrante
# ------------------------------------------------------------------
c = cell("319ab777")
put(c, """## 1.2 Aplicación a condiciones reales\n\n### 1.2.1 Condición base: calibración y umbral de parpadeo\n\nEsta prueba la realiza el integrante asignado a las secciones **1.2.1 y 1.2.2**. Registrar el `EAR_THRESHOLD` obtenido y usar el `.png` generado automáticamente.\n""")

c = cell("6d1121fb")
put(c, '''# 1.2.1 – Condición base\nintegrante_a = input("Nombre o código del integrante asignado a 1.2.1 y 1.2.2: ").strip()\n\nresultado_base, datos_base = run_ear_session(\n    condition_name="1.2.1_Base_frontal_sin_lentes",\n    calibration_time=4,\n    record_time=20,\n    participant_name=integrante_a,\n)\n''')

c = cell("ce05bc8b")
s = get(c)
s = s.replace(
    "    record_time=20,\n)",
    "    record_time=20,\n    participant_name=integrante_a,\n)",
    1
)
put(c, s)

# ------------------------------------------------------------------
# 1.2.3: otro integrante, tres ángulos
# ------------------------------------------------------------------
c = cell("1c4fa25b")
put(c, """### 1.2.3 Efecto del ángulo de cámara\n\nEsta sección la realiza otro integrante. Realizar la prueba en tres posiciones de cámara:\n\n1. superior;\n2. frontal;\n3. inferior.\n\nMover la cámara antes de ejecutar cada celda. Se guardará automáticamente un `.png` por cada posición.\n""")

c = cell("f5d01229")
put(c, '''# 1.2.3A – Cámara en posición SUPERIOR\nintegrante_b = input("Nombre o código del integrante asignado a 1.2.3: ").strip()\n\nresultado_superior, datos_superior = run_ear_session(\n    condition_name="1.2.3_Superior",\n    calibration_time=4,\n    record_time=20,\n    participant_name=integrante_b,\n)\n''')

for cid in ("2fccac7a", "32833587"):
    c = cell(cid)
    s = get(c)
    s = s.replace(
        "    record_time=20,\n)",
        "    record_time=20,\n    participant_name=integrante_b,\n)",
        1
    )
    put(c, s)

# ------------------------------------------------------------------
# 1.2.4: todos los integrantes
# ------------------------------------------------------------------
c = cell("c2de7589")
s = get(c).replace(
    "Al final se muestran los valores de EAR threshold, PERCLOS y número de parpadeos para compararlos.",
    "Al final se muestran los valores de EAR threshold, PERCLOS y número de parpadeos para compararlos. Cada ejecución guarda automáticamente su `.png` y `.csv`."
)
put(c, s)

c = cell("a03335ef")
s = get(c)
s = s.replace(
    "    condition_name=f\"1.2.4_{integrante}\",",
    "    condition_name=\"1.2.4_Comparacion_integrantes\","
)
s = s.replace(
    "    record_time=20,\n)",
    "    record_time=20,\n    participant_name=integrante,\n)",
    1
)
put(c, s)

# ------------------------------------------------------------------
# Archivos generados
# ------------------------------------------------------------------
c = cell("2754782f")
put(c, """## Archivos generados\n\nCada ejecución guarda automáticamente en:\n\n`resultados_eye_tracking/`\n\n- un `.png` con la evidencia visual de la prueba;\n- un `.csv` con los valores EAR registrados.\n\nPara el reporte, usar los archivos `.png` correspondientes a cada prueba.\n""")

NB.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print("01_EyeTracking.ipynb actualizado correctamente")
