import json

def compilar_cv_markdown():
    print("[Vhrs- Terminal] Generando interfaz visual del CV en Markdown...")
    
    with open("cvu_estandar_intertopia.json", "r", encoding="utf-8") as f:
        cv = json.load(f)
        
    md = f"# Currículum Vitae Único - {cv['identidad_soberana']['nombre_legal']}\n\n"
    md += f"**ORCID ID:** {cv['identidad_soberana']['orcid_id']} | **Perfil:** {cv['identidad_soberana']['perfil_objetivo']}\n"
    md += f"**Administrador Único y Soberano [Intertopía]**\n\n---\n\n"
    
    md += "## 🏛 Formación Académica\n"
    for item in cv["formacion_academica"]:
        md += f"- **{item['grado']}** — {item['institucion']} ({item['año_inicio']})\n"
        
    md += "\n## ⚙️ Trayectoria Profesional\n"
    for item in cv["trayectoria_profesional"]:
        md += f"- **{item['cargo']}** — {item['institucion']} ({item['año_inicio']})\n"
        
    md += "\n## 📜 Producción, Patentes y Tecnología\n"
    for item in cv["produccion_y_tecnologia"]["propiedad_intelectual_y_patentes"]:
        md += f"- 🔹 {item['titulo']} [Enlace/DOI: {item['identificador_doi_url']}]\n"
        
    for item in cv["produccion_y_tecnologia"]["publicaciones"]:
        md += f"- 📄 {item['titulo']} [Enlace/DOI: {item['identificador_doi_url']}]\n"

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(md)
        
    print("[ÉXITO] README.md actualizado. El perfil público ha sido sincronizado con los datos de ORCID.")

# compilar_cv_markdown()
