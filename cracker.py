# Proyecto: Cracker de Hashes por Diccionario
# Herramienta CLI Profesional con 'argparse'

import hashlib
import sys
import argparse # ¡Nuestra librería para argumentos de CLI!

# -----------------------------------------------------------------
# --- FUNCIONES DE AYUDA (Helpers) ---
# -----------------------------------------------------------------

def hashear_palabra(palabra, algoritmo):
    """
    Toma una palabra (string) y un algoritmo (string),
    y devuelve el hash de esa palabra.
    """
    # 1. Limpiamos la palabra (¡crucial!)
    palabra_limpia = palabra.strip()
    
    # 2. La codificamos a bytes
    palabra_en_bytes = palabra_limpia.encode('utf-8')
    
    # 3. Creamos el objeto hash basado en el algoritmo
    if algoritmo == 'md5':
        hash_obj = hashlib.md5(palabra_en_bytes)
    elif algoritmo == 'sha1':
        hash_obj = hashlib.sha1(palabra_en_bytes)
    elif algoritmo == 'sha256':
        hash_obj = hashlib.sha256(palabra_en_bytes)
    else:
        # Si el algoritmo no es soportado, devolvemos None
        return None
        
    # 4. Devolvemos el hash en formato texto
    return hash_obj.hexdigest()

# -----------------------------------------------------------------
# --- FUNCIÓN PRINCIPAL (main) ---
# -----------------------------------------------------------------
def main():
    # 1. Creamos el "parser" de argumentos
    parser = argparse.ArgumentParser(description="Cracker de Hashes por Diccionario en Python")
    
    # 2. Definimos los argumentos que aceptamos
    parser.add_argument("-H", "--hash", dest="hash_objetivo", required=True, help="El hash que se desea crackear.")
    parser.add_argument("-w", "--wordlist", dest="wordlist_path", required=True, help="Ruta al archivo de diccionario (wordlist).")
    parser.add_argument("-a", "--algoritmo", dest="algoritmo", default="md5", help="Algoritmo de hash (md5, sha1, sha256). Default: md5")

    # 3. Leemos los argumentos del terminal
    args = parser.parse_args()
    
    # Validamos el algoritmo
    algoritmos_soportados = ['md5', 'sha1', 'sha256']
    if args.algoritmo not in algoritmos_soportados:
        print(f"[ERROR] Algoritmo no soportado: {args.algoritmo}. Soportados: {algoritmos_soportados}")
        sys.exit()

    print("--- Iniciando Cracker de Hashes v0.3 (CLI) ---")
    print(f"Objetivo del Hash ({args.algoritmo.upper()}): {args.hash_objetivo}")
    print(f"Cargando diccionario: {args.wordlist_path}")

    # 4. Creamos una variable para saber si la encontramos
    encontrada = False

    # 5. Lógica del Cracker (con manejo de errores)
    try:
        with open(args.wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            
            # Leemos el archivo línea por línea
            for palabra in f:
                
                # 6. Hasheamos la palabra usando nuestra función de ayuda
                hash_calculado = hashear_palabra(palabra, args.algoritmo)
                
                # 7. Comparamos
                if hash_calculado == args.hash_objetivo:
                    print("\n[ÉXITO] ¡Contraseña encontrada!")
                    print(f"El hash {args.hash_objetivo} corresponde a la palabra: '{palabra.strip()}'")
                    encontrada = True
                    break # ¡Rompemos el bucle!
        
        # 8. Reporte final
        if not encontrada:
            print(f"\n[FALLO] La contraseña no fue encontrada en el diccionario.")

    except FileNotFoundError:
        print(f"[ERROR] No se pudo encontrar el diccionario en: {args.wordlist_path}")
        sys.exit()
    except Exception as e:
        print(f"[ERROR] Ocurrió un error inesperado: {e}")

    print("--- Cracker finalizado ---")

# -----------------------------------------------------------------
# --- PUNTO DE ENTRADA ---
# -----------------------------------------------------------------
if __name__ == "__main__":
    main()