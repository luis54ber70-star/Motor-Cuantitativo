def calcular_kelly(momio_decimal, prob_real, fraccion_kelly=0.25):
    """Calcula el tamaño de apuesta usando el Criterio de Kelly Fraccional."""
    b = momio_decimal - 1  # Ganancia neta por unidad apostada
    p = prob_real          # Probabilidad real de ganar
    q = 1 - p              # Probabilidad de perder

    # Verificamos primero si la apuesta tiene Valor Esperado positivo (+EV)
    if (p * b) - q <= 0:
        return 0.0  # Si no hay ventaja, no se apuesta nada

    # Fórmula del Kelly Completo: f = (bp - q) / b
    kelly_completo = (b * p - q) / b

    # Aplicamos la protección del Kelly Fraccional para mitigar el riesgo
    kelly_final = kelly_completo * fraccion_kelly

    return round(kelly_final, 4)

# Prueba con nuestro ejemplo anterior de los Mets (Momio 1.91, Prob 55%)
apuesta = calcular_kelly(1.91, 0.55)
print(f"Sugerencia de apuesta: {apuesta * 100}% del bankroll")

