def ejecutar_ciclo_90_10(utilidad_bruta):
    """
    Aplica el ciclo de 24 horas: 90% para Víctor Hugo Ramírez Salgado (VHRS),
    10% para el sistema Intertopía.
    """
    SPLIT_VHRS = 0.90
    SPLIT_INTERTOPIA = 0.10

    beneficio_vhrs = round(utilidad_bruta * SPLIT_VHRS, 2)
    beneficio_intertopia = round(utilidad_bruta * SPLIT_INTERTOPIA, 2)

    return {
        "beneficio_vhrs": beneficio_vhrs,
        "beneficio_intertopia": beneficio_intertopia,
        "split": "90/10",
    }
