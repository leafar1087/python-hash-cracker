# -----------------------------------------------------------------
# MASTERCLASS DE HERRAMIENTAS DE CIBERSEGURIDAD (MÓDULO 2.6 - v0.9)
# -----------------------------------------------------------------
# Proyecto: Cracker de Hashes por Diccionario
# Lección 2.6: La Herramienta Multihilo (¡LA ARQUITECTURA CORRECTA!)

import hashlib
import sys
import argparse
import threading
from queue import Queue, Empty
from tqdm import tqdm # ¡Importante!
import time # ¡Importante para el bucle de espera!

# --- Función de Ayuda (sin cambios) ---
def hashear_palabra(palabra, algoritmo):
    palabra_limpia = palabra.strip()
    palabra_en_bytes = palabra_limpia.encode('utf-8')
    
    if algoritmo == 'md5':
        hash_obj = hashlib.md5(palabra_en_bytes)
    elif algoritmo == 'sha1':
        hash_obj = hashlib.sha1(palabra_en_bytes)
    elif algoritmo == 'sha256':
        hash_obj = hashlib.sha256(palabra_en_bytes)
    else:
        return None
        
    return hash_obj.hexdigest()

# --- 1. FUNCIÓN "TRABAJADOR" (Consumidor) ---
def trabajador(q, hash_objetivo, algoritmo, lock_impresion, stop_event, resultados, tqdm_bar):
    """Toma palabras de la cola (q) y las hashea."""
    
    while True:
        try:
            # "Intenta tomar una palabra. Espera MÁXIMO 1 segundo".
            palabra = q.get(timeout=1) 
            
        except Empty:
            # Si la cola estuvo vacía por 1 seg, 
            # y el 'main' thread (que es el alimentador) ya no está vivo,
            # entonces el trabajo terminó.
            if not threading.main_thread().is_alive():
                 break
            continue 
        
        # --- Si llegamos aquí, SÍ tenemos una palabra ---
        
        try:
            if not stop_event.is_set():
                hash_calculado = hashear_palabra(palabra, algoritmo)
                
                if hash_calculado == hash_objetivo:
                    with lock_impresion:
                        # Usamos tqdm.write() para no romper la barra de progreso
                        tqdm.write("\n" + "="*30)
                        tqdm.write(f"[ÉXITO] ¡Contraseña encontrada!")
                        tqdm.write(f"  Hash: {hash_objetivo}")
                        tqdm.write(f"  Palabra: '{palabra.strip()}'")
                        tqdm.write("="*30)
                    
                    resultados['palabra'] = palabra.strip()
                    stop_event.set() # ¡Presiona el botón de parada!
        
        finally:
            # --- ¡CRUCIAL! ---
            # Le avisamos a q.join() que esta tarea terminó,
            # PASE LO QUE PASE (éxito, fallo o parada).
            q.task_done()
            tqdm_bar.update(1) # ¡Actualiza la barra de progreso!

# --- 2. ¡NUEVA FUNCIÓN "ALIMENTADOR"! (Productor) ---
# (La quitamos, 'main' volverá a ser el alimentador, ¡pero lo haremos bien!)

# -----------------------------------------------------------------
# --- FUNCIÓN PRINCIPAL (main) - ¡AHORA ES UN "GERENTE"! ---
# -----------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Cracker de Hashes Multihilo en Python")
    parser.add_argument("-H", "--hash", dest="hash_objetivo", required=True, help="El hash que se desea crackear.")
    parser.add_argument("-w", "--wordlist", dest="wordlist_path", required=True, help="Ruta al archivo de diccionario (wordlist).")
    parser.add_argument("-a", "--algoritmo", dest="algoritmo", default="md5", help="Algoritmo de hash (md5, sha1, sha256). Default: md5")
    parser.add_argument("-t", "--threads", dest="num_hilos", type=int, default=100, help="Número de hilos (trabajadores) (default: 100)")
    args = parser.parse_args()
    
    if args.algoritmo not in ['md5', 'sha1', 'sha256']:
        print(f"[ERROR] Algoritmo no soportado: {args.algoritmo}.")
        sys.exit()

    print("--- Iniciando Cracker de Hashes v0.9 (Multihilo Corregido) ---")

    palabra_queue = Queue()
    lock_impresion = threading.Lock()
    stop_event = threading.Event()
    resultados = {'palabra': None}

    try:
        with open(args.wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            total_lineas = sum(1 for _ in f)
        print(f"Diccionario cargado. {total_lineas:,} palabras a probar.")
    except FileNotFoundError:
        print(f"[ERROR] No se pudo encontrar el diccionario en: {args.wordlist_path}")
        sys.exit()
    
    # Creamos la barra de progreso
    tqdm_bar = tqdm(total=total_lineas, desc="[+] Crackeando", unit=" palabras", dynamic_ncols=True)
    
    print(f"Lanzando {args.num_hilos} hilos 'Trabajadores'...")

    # "Contratamos" y lanzamos los hilos "Trabajadores"
    for _ in range(args.num_hilos):
        t = threading.Thread(
            target=trabajador,
            args=(palabra_queue, args.hash_objetivo, args.algoritmo, lock_impresion, stop_event, resultados, tqdm_bar),
            daemon=True
        )
        t.start()

    # --- 3. ¡EL HILO 'MAIN' ES EL ALIMENTADOR! ---
    try:
        # Abrimos el archivo de nuevo para leerlo
        with open(args.wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for palabra in f:
                # Si un hilo ya encontró el hash, dejamos de leer.
                if stop_event.is_set():
                    break
                palabra_queue.put(palabra)
        
        # --- 4. ¡LA LÓGICA DE ESPERA CORRECTA! ---
        # Le decimos al 'main' (Alimentador) que espere
        # hasta que la cola que él llenó, se vacíe.
        # (q.join() espera hasta que q.task_done() se llame 14.3M de veces)
        palabra_queue.join()
        
    except KeyboardInterrupt:
        print("\n[INFO] Ataque cancelado por el usuario.")
        stop_event.set()
    finally:
        # Pase lo que pase, nos aseguramos de que todos los hilos
        # (que están en 'except Empty: continue') sepan que deben parar.
        stop_event.set()
        tqdm_bar.close() # Cerramos la barra de progreso

    # Reporte Final
    print("\n--- Cracker finalizado ---")
    if resultados['palabra']:
        pass # El éxito ya fue impreso por el hilo
    else:
        print("[FALLO] La contraseña no fue encontrada en el diccionario.")

# --- Punto de Entrada (sin cambios) ---
if __name__ == "__main__":
    main()