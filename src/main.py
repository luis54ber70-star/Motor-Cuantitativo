import os
from datetime import datetime

def calcular_kelly(momio_decimal, prob_real, fraccion_kelly=0.25):
    """Calcula el tamaño de apuesta usando el Criterio de Kelly Fraccional."""
    b = momio_decimal - 1  
    p = prob_real          
    q = 1 - p              

    # Verificamos si hay Valor Esperado positivo (+EV)
    if (p * b) - q <= 0:
        return 0.0  

    # Kelly Completo y Fraccional
    kelly_completo = (b * p - q) / b
    return round(kelly_completo * fraccion_kelly, 4)

# 1. Simulación de ejecución (Ejemplo Mets)
momio = 1.91
prob = 0.55
apuesta = calcular_kelly(momio, prob)

# 2. Construir el Bloque de Estado (Memoria)
fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_entry = f"""
--- EJECUCIÓN: {fecha} ---
Resultado Kelly: Sugerencia de apuesta del {apuesta * 100}% del bankroll.

ESTADO_DEL_MODELO_ACTUAL (DATABASE LOG)
Último Error Auditado: Ninguno. Ejecución base exitosa.
Umbrales de Búsqueda Activos: Probabilidad real > 50%, +EV.
Regla de Oro Vigente: Ejecución estricta de gestión de riesgo (Cuarto de Kelly).
\n"""

# 3. Escribir y guardar en el archivo de texto
os.makedirs("data", exist_ok=True) # Crea la carpeta si no existe
with open("data/database_log.txt", "a", encoding="utf-8") as file:
    file.write(log_entry)
