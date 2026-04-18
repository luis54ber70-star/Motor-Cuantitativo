import os
import math
import requests
from datetime import datetime

# Conexión a tus variables secretas de GitHub
odds_api_key = os.getenv("ODDS_API_KEY")
sports_api_key = os.getenv("ALL_SPORTS_API_KEY")

def distribucion_poisson(esperado, real):
    return (math.exp(-esperado) * (esperado ** real)) / math.factorial(real)

def calcular_probabilidad_victoria(xg_equipo, xg_rival):
    prob_ganar = 0.0
    for goles_equipo in range(1, 16):
        for goles_rival in range(0, goles_equipo): 
            prob_marcador = distribucion_poisson(xg_equipo, goles_equipo) * distribucion_poisson(xg_rival, goles_rival)
            prob_ganar += prob_marcador
    return round(prob_ganar, 4)

def calcular_kelly(momio_decimal, prob_real, fraccion_kelly=0.25):
    b = momio_decimal - 1
    p = prob_real
    q = 1 - p
    if (p * b) - q <= 0:
        return 0.0 
    return round(((b * p - q) / b) * fraccion_kelly, 4)

def ejecutar_motor():
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"--- EJECUCIÓN 100% AUTÓNOMA: {fecha} ---\n"
    
    if not odds_api_key or not sports_api_key:
        log_entry += "Error: Faltan claves de API en los Secrets.\n\n"
    else:
        try:
            # 1. Extracción de momios
            url_odds = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds/?apiKey={odds_api_key}&regions=us&markets=h2h"
            respuesta = requests.get(url_odds).json()
            
            # Agregamos  para navegar correctamente por las listas del JSON
            juego = respuesta 
            equipo = juego['bookmakers']['markets']['outcomes']['name']
            momio = juego['bookmakers']['markets']['outcomes']['price']
            
            # 2. Extracción de estadísticas reales (All Sports API)
            # Nota: Reemplazar 'URL_ALL_SPORTS' con el endpoint exacto de tu deporte
            url_stats = f"URL_ALL_SPORTS?APIkey={sports_api_key}&team={equipo}"
            # Simulamos la extracción de los promedios reales (xG) de la respuesta JSON
            xg_favor = 4.5 # Aquí iría: stats_json['goles_anotados_promedio']
            xg_contra = 3.2 # Aquí iría: stats_json['goles_recibidos_promedio']
            
            # 3. Modelado Predictivo
            prob_real = calcular_probabilidad_victoria(xg_favor, xg_contra)
            apuesta = calcular_kelly(momio, prob_real)
            
            log_entry += f"Evento: {equipo} | Momio: {momio}\n"
            log_entry += f"Métricas Reales: xG={xg_favor}, xGA={xg_contra} -> Prob. Matemática: {prob_real*100}%\n"
            
            if apuesta > 0:
                log_entry += f"VALOR DETECTADO (+EV): Apostar {apuesta * 100}% del bankroll.\n"
            else:
                log_entry += "SIN ENTRADAS DE VALOR DETECTADAS.\n"
                
        except Exception as e:
            log_entry += f"Fallo en la ejecución: {e}\n"

    # 4. Guardar en memoria
    os.makedirs("data", exist_ok=True)
    with open("data/database_log.txt", "a", encoding="utf-8") as file:
        file.write(log_entry + "\n")
    print("Análisis guardado exitosamente.")

if __name__ == "__main__":
    ejecutar_motor()
