"""Ejecuta los cuatro hitos y prepara la carpeta 04_Entrega_Final:

- figuras/                 copia de las figuras usadas en la memoria
- resumen_indicadores.csv  indicadores por sesion + clase detectada
- Memoria.pdf              si hay pandoc + pdflatex disponibles
"""
import shutil
import subprocess

import pandas as pd

import hito1_analisis
import hito2_preprocesado
import hito3_caracteristicas
import hito4_deteccion
from carrera import caracteristicas as cr, carga

FIGURAS_MEMORIA = [
    "Hito_1_Analisis_Senal/figuras/h1_senales_originales.png",
    "Hito_1_Analisis_Senal/figuras/h1_histograma_muestreo.png",
    "Hito_1_Analisis_Senal/figuras/h1_anomalias.png",
    "Hito_2_Preprocesado/figuras/h2_espectros.png",
    "Hito_2_Preprocesado/figuras/h2_comparativa_filtros.png",
    "Hito_2_Preprocesado/figuras/h2_limpieza.png",
    "Hito_3_Extraccion_Caracteristicas/figuras/h3_parciales_2026-01-11.png",
    "Hito_3_Extraccion_Caracteristicas/figuras/h3_deriva_2026-01-11.png",
    "Hito_3_Extraccion_Caracteristicas/figuras/h3_pendiente_2026-01-15.png",
    "Hito_3_Extraccion_Caracteristicas/figuras/h3_zonas_fc.png",
    "Hito_4_Clasificacion_o_Deteccion/figuras/h4_sesiones_reales.png",
    "Hito_4_Clasificacion_o_Deteccion/figuras/h4_validacion_sintetica.png",
]


def resumen_indicadores(resultados):
    filas = []
    for nombre, r in resultados.items():
        s = r["resumen"]
        filas.append({
            "fecha": nombre, "tipo_sesion": r["tipo"],
            "distancia_km": s["distancia_km"], "distancia_strava_km": s["distancia_strava_km"],
            "duracion_min": s["duracion_min"], "tiempo_corriendo_min": s["tiempo_carrera_min"],
            "ritmo_carrera_min_km": cr.formato_ritmo(s["ritmo_carrera_min_km"]),
            "v_carrera_kmh": s["v_carrera_kmh"], "cv_velocidad_pct": s["cv_velocidad_pct"],
            "fc_media_ppm": s["fc_media"], "fc_max_ppm": s["fc_max"],
            "t_Z3_pct": s["t_Z3_pct"], "t_Z4_pct": s["t_Z4_pct"],
            "desnivel_pos_m": s["desnivel_pos_m"], "pendiente_max_pct": s["pendiente_max_pct"],
            "estabilizacion_fc_min": s["t_estab_fc_min"],
            "desacoplamiento_pct": s["desacoplamiento_pct"],
            "metros_por_latido": s["ef_m_por_latido"],
            "cambios_ritmo": len(r["cortes"]),
        })
    return pd.DataFrame(filas)


def compilar_pdf():
    try:
        import pypandoc
        pandoc = pypandoc.get_pandoc_path()
    except (ImportError, OSError):
        pandoc = shutil.which("pandoc")
    if not pandoc or not shutil.which("pdflatex"):
        print("pandoc/pdflatex no disponibles: no se genera Memoria.pdf")
        return
    subprocess.run([pandoc, "Memoria.md", "-o", "Memoria.pdf", "--pdf-engine=pdflatex",
                    "-V", "geometry:margin=2.2cm", "-V", "lang=es", "-V", "fontsize=10pt",
                    "-V", "colorlinks=true"],
                   cwd=carga.DIR_ENTREGA, check=True)
    print("Generado", carga.DIR_ENTREGA / "Memoria.pdf")


def main():
    hito1_analisis.main()
    hito2_preprocesado.main()
    hito3_caracteristicas.main()
    resultados = hito4_deteccion.main()

    destino = carga.DIR_ENTREGA / "figuras"
    destino.mkdir(parents=True, exist_ok=True)
    for f in FIGURAS_MEMORIA:
        shutil.copy(carga.DIR_HITOS / f, destino)

    tabla = resumen_indicadores(resultados)
    tabla.to_csv(carga.DIR_ENTREGA / "resumen_indicadores.csv", index=False, float_format="%.2f")
    print(tabla.round(2).to_markdown(index=False))
    if (carga.DIR_ENTREGA / "Memoria.md").exists():
        compilar_pdf()


if __name__ == "__main__":
    main()
