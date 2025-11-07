# Proyecto: Cracker de Hashes por Diccionario
# Lección 2.1: Comparar un solo hash

# 1. Importamos la librería de hashing
import hashlib

print("--- Iniciando Cracker de Hashes v0.1 ---")

# 2. Definimos nuestros objetivos
#    Este es el hash que "encontramos" y queremos crackear.
#    (Sabemos que este es el hash MD5 de la palabra 'hola')
hash_objetivo = "4d186321c1a7f0f354b297e8914ab240"

#    Esta es la palabra que vamos a "probar"
palabra_de_prueba = "hola"

print(f"Objetivo del Hash (MD5): {hash_objetivo}")
print(f"Probando palabra: '{palabra_de_prueba}'")

# 3. ¡Aquí empieza la lógica de Hashing!
try:
    # 4. Codificamos nuestro string 'palabra_de_prueba' a bytes
    palabra_en_bytes = palabra_de_prueba.encode('utf-8')
    
    # 5. Creamos un objeto hash MD5 y le pasamos los bytes
    hash_calculado_obj = hashlib.md5(palabra_en_bytes)
    
    # 6. Obtenemos el resultado en formato de texto hexadecimal
    hash_calculado_str = hash_calculado_obj.hexdigest()
    
    print(f"Hash calculado:       {hash_calculado_str}")

    # 7. ¡La Comparación! (El núcleo de nuestro cracker)
    if hash_calculado_str == hash_objetivo:
        print("\n[ÉXITO] ¡Contraseña encontrada!")
        print(f"El hash {hash_objetivo} corresponde a la palabra: '{palabra_de_prueba}'")
    else:
        print("\n[FALLO] La palabra no coincide.")

except Exception as e:
    print(f"[ERROR] Ocurrió un error: {e}")

print("--- Prueba de hash finalizada ---")