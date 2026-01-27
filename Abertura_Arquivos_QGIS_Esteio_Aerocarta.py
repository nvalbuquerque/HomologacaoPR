import os
from qgis.core import (
    QgsVectorLayer,
    QgsRasterLayer,
    QgsProject
)

# ALTERAR AQUI LINHAS 9 E 10
pasta = r"E:\Homologacao_Nathalia\Analises\Aerocarta_Lote_6_Bloco_B\2_GeoTIFF"
shp_path = r"E:\Homologacao_Nathalia\Analises\Aerocarta_Lote_6_Bloco_B\shp\Amostra_Lote_6_Bloco_B.shp"

campo_codigo = "MI_3"

# =========================
# CARREGA O SHP
# =========================
# ALTERAR LINHA 18
shp = QgsVectorLayer(shp_path, "Amostra_Lote_6_Bloco_B", "ogr")
if not shp.isValid():
    raise Exception("Erro ao carregar o shapefile")

# =========================
# LÊ OS CÓDIGOS DO SHP
# =========================
codigos = {
    str(f[campo_codigo]).strip().lower()
    for f in shp.getFeatures()
    if f[campo_codigo] is not None
}

print(f"{len(codigos)} códigos lidos do SHP.")

# =========================
# GRUPO NO QGIS
# =========================
projeto = QgsProject.instance()
grupo = projeto.layerTreeRoot().addGroup("Arquivos filtrados")

contador = 0

# =========================
# PERCORRE OS TIFFS
# =========================
for arquivo in os.listdir(pasta):
    nome = arquivo.lower()

    if not nome.endswith((".tif", ".tiff")):
        continue

    # remove extensão
    base = os.path.splitext(nome)[0]

    # exemplo:
    # ES_L01_D_E_IMG_HC_2753-3-SO-B-IV_R0
    partes = base.split("_")

    if "hc" not in partes:
        continue

    idx = partes.index("hc")

    try:
        codigo_arquivo = partes[idx + 1]
    except IndexError:
        continue

    if codigo_arquivo in codigos:
        caminho = os.path.join(pasta, arquivo)
        raster = QgsRasterLayer(caminho, arquivo)

        if raster.isValid():
            projeto.addMapLayer(raster, False)
            grupo.addLayer(raster)
            contador += 1
        else:
            print(f"Erro ao carregar: {arquivo}")

print(f"{contador} arquivos carregados no projeto.")
