import os
import shutil

FUNCIONES = {
    "LanguagePoC": "lpoc",
    "HttpTrigger": "httr"
}

SUBMODULOS = ["validators", "orchestrator", "shared", "jira_connector"]

def renombrar_submodulos():
    for funcion, prefijo in FUNCIONES.items():
        for sub in SUBMODULOS:
            old_path = os.path.join(funcion, sub)
            new_name = f"{prefijo}_{sub}"
            new_path = os.path.join(funcion, new_name)
            if os.path.isdir(old_path):
                print(f"Renombrando {old_path} → {new_path}")
                shutil.move(old_path, new_path)

def actualizar_imports():
    for funcion, prefijo in FUNCIONES.items():
        base_dir = os.path.join(os.getcwd(), funcion)
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    original = content
                    for sub in SUBMODULOS:
                        old_import = f"{funcion}.{sub}"
                        new_import = f"{funcion}.{prefijo}_{sub}"
                        content = content.replace(old_import, new_import)
                        # También cubrir casos de import relativos dentro del módulo
                        content = content.replace(f"from {sub}", f"from {prefijo}_{sub}")
                        content = content.replace(f"import {sub}", f"import {prefijo}_{sub}")
                    if content != original:
                        print(f"Actualizando imports en {full_path}")
                        with open(full_path, "w", encoding="utf-8") as f:
                            f.write(content)

if __name__ == "__main__":
    renombrar_submodulos()
    actualizar_imports()
    print("✅ Refactorización completada.")
