import json
import subprocess
from pathlib import Path

BASE_COMMIT = "11643ac8f2df87018064bb98da62f350acb6f4ba"
NB = Path("01_EyeTracking.ipynb")

# Recuperar la versión anterior del notebook y aplicar SOLO el guardado de PNG.
raw = subprocess.check_output(
    ["git", "show", f"{BASE_COMMIT}:01_EyeTracking.ipynb"],
    text=True,
    encoding="utf-8",
)
nb = json.loads(raw)


def cell(cell_id):
    for c in nb["cells"]:
        if c.get("id") == cell_id:
            return c
    raise KeyError(cell_id)


def get(c):
    return "".join(c["source"])


def put(c, text):
    c["source"] = text.splitlines(keepends=True)


# Cambiar solo la nota general.
c = cell("20d0f122")
s = get(c).replace(
    "Para el reporte, tomar la captura directamente durante cada prueba. Los datos también se guardan en `.csv` por si se necesitan revisar después.",
    "Al finalizar cada prueba se guarda automáticamente una imagen `.png` de la ventana mostrada y un archivo `.csv` con los datos."
)
put(c, s)

# Modificación mínima dentro de run_ear_session.
c = cell("9ebcfdfa")
s = get(c)

# Variable para conservar la última imagen mostrada durante el registro.
s = s.replace(
    "    user_quit = False\n",
    "    user_quit = False\n    last_capture = None\n",
    1,
)

# Guardar el último frame combinado SOLO durante la etapa de registro.
needle = "            combined = _combine_camera_and_plot(frame, plot_img)\n            cv2.imshow(window_name, combined)"
first = s.find(needle)
second = s.find(needle, first + 1) if first != -1 else -1
if second == -1:
    raise RuntimeError("No se encontró el bloque de registro")

replacement = (
    "            combined = _combine_camera_and_plot(frame, plot_img)\n"
    "            last_capture = combined.copy()\n"
    "            cv2.imshow(window_name, combined)"
)
s = s[:second] + s[second:].replace(needle, replacement, 1)

# Guardar PNG junto al CSV al finalizar.
old = '''    if save_outputs:\n        csv_path = OUTPUT_DIR / f"{stamp}_{file_tag}.csv"\n        df.to_csv(csv_path, index=False)\n        print(f"CSV guardado: {csv_path}")\n\n    # No se crea una gráfica al terminar:\n    # la evidencia es el screenshot de la ventana en vivo.\n'''
new = '''    if save_outputs:\n        csv_path = OUTPUT_DIR / f"{stamp}_{file_tag}.csv"\n        df.to_csv(csv_path, index=False)\n        print(f"CSV guardado: {csv_path}")\n\n        if last_capture is not None:\n            png_path = OUTPUT_DIR / f"{stamp}_{file_tag}.png"\n            cv2.imwrite(str(png_path), last_capture)\n            print(f"PNG guardado: {png_path}")\n\n'''
if old not in s:
    raise RuntimeError("No se encontró el bloque final de guardado")
s = s.replace(old, new)
put(c, s)

# Nota final de archivos generados.
c = cell("2754782f")
s = get(c).replace(
    "Para el reporte, usar las capturas tomadas directamente durante la ejecución.",
    "Para el reporte, usar las imágenes `.png` generadas automáticamente al finalizar cada prueba."
)
put(c, s)

NB.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print("01_EyeTracking.ipynb actualizado: solo se añadió guardado automático de PNG")
