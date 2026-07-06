def split_profit(total_profit: float):
    """
    Reparte la ganancia total según la regla fija de Intertopía:
    70% para el sistema/proyecto Intertopía
    30% para Víctor Hugo Ramírez Salgado
    """
    if total_profit < 0:
        raise ValueError("La ganancia no puede ser negativa")

    intertopia_share = round(total_profit * 0.70, 2)
    victor_share = round(total_profit * 0.30, 2)

    return {
        "total": total_profit,
        "intertopia": intertopia_share,
        "victor_hugo_ramirez_salgado": victor_share
    }

