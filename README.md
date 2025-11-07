# Python Hash Cracker

Herramienta multihilo para crackear hashes mediante ataques de diccionario (wordlist).

## Descripción

Este proyecto es un cracker de hashes que utiliza múltiples hilos para probar contraseñas desde un diccionario (wordlist) contra un hash objetivo. Soporta los algoritmos MD5, SHA1 y SHA256.

## Requisitos

- Python 3.x
- Biblioteca `tqdm` (para la barra de progreso)

## Instalación

1. Clona o descarga este repositorio
2. Instala las dependencias:

```bash
pip install tqdm
```

## Descarga de rockyou.txt

El archivo `rockyou.txt` es una wordlist muy popular en ciberseguridad que contiene millones de contraseñas comunes.

### Opción 1: Desde Kali Linux (si tienes acceso)
Si tienes Kali Linux instalado, el archivo se encuentra en:
```
/usr/share/wordlists/rockyou.txt
```

### Opción 2: Descarga directa
Puedes descargar `rockyou.txt` desde las siguientes fuentes:

- **GitHub**: https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt
- **SecLists**: https://github.com/danielmiessler/SecLists/blob/master/Passwords/Leaked-Databases/rockyou.txt.tar.gz
- **Kali Linux Repository**: El archivo está disponible en los repositorios de Kali Linux

**Nota**: El archivo `rockyou.txt` es grande (aproximadamente 133 MB sin comprimir) y contiene millones de contraseñas. Asegúrate de tener suficiente espacio en disco.

## Uso

```bash
python cracker.py -H <hash> -w <ruta_wordlist> -a <algoritmo> -t <num_hilos>
```

### Parámetros

- `-H, --hash`: El hash que deseas crackear (requerido)
- `-w, --wordlist`: Ruta al archivo de diccionario/wordlist (requerido)
- `-a, --algoritmo`: Algoritmo de hash (`md5`, `sha1`, `sha256`). Por defecto: `md5`
- `-t, --threads`: Número de hilos trabajadores. Por defecto: 100

### Ejemplo

```bash
python cracker.py -H 5f4dcc3b5aa765d61d8327deb882cf99 -w rockyou.txt -a md5 -t 100
```

Este ejemplo intentará crackear el hash MD5 `5f4dcc3b5aa765d61d8327deb882cf99` usando el archivo `rockyou.txt` con 100 hilos.

## Características

- ✅ Soporte multihilo para procesamiento rápido
- ✅ Barra de progreso en tiempo real
- ✅ Soporte para MD5, SHA1 y SHA256
- ✅ Manejo de interrupciones (Ctrl+C)
- ✅ Detección automática cuando se encuentra la contraseña

## Notas

- Este proyecto es solo para fines educativos y de prueba de seguridad autorizada
- Asegúrate de tener permiso antes de usar esta herramienta en sistemas que no te pertenecen
- El tiempo de crackeo depende del tamaño de la wordlist y de la complejidad de la contraseña

