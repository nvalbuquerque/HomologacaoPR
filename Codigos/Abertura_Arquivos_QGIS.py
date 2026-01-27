import re
import os
from qgis.core import (
    QgsVectorLayer,
    QgsRasterLayer,
    QgsProject
)

# =========================
# CAMINHOS - ALTERAR LINHAS 12 E 13: Conteúdo entre aspas
# =========================
pasta = r"E:\Homologacao_Nathalia\Analises\Engefoto_Lote_10_Bloco_E\2_GeoTIFF"
shp_path = r"E:\Homologacao_Nathalia\Analises\Engefoto_Lote_10_Bloco_E\Amostra_Engefoto_Lote10_BlocoE.shp"

campo_codigo = "MI_3"

# =========================
# CARREGA O SHP - ALTERAR LINHA 20: Conteúdo entre aspas
# =========================
shp = QgsVectorLayer(shp_path, "Amostra_Engefoto_Lote10_BlocoE", "ogr")
if not shp.isValid():
    raise Exception("Erro ao carregar o shapefile")

# =========================
# LÊ OS CÓDIGOS DO SHP
# =========================
codigos = {
    str(f[campo_codigo]).strip().lower().replace("_", "-")
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

    base = os.path.splitext(nome)[0]

    # procura tudo após _HC_
    match = re.search(r"_hc_(.+)", base)
    if not match:
        continue

    codigo_arquivo = match.group(1)

    # remove sufixos tipo _R0
    codigo_arquivo = codigo_arquivo.split("_r")[0]

    # normaliza separadores
    codigo_arquivo_norm = codigo_arquivo.replace("_", "-")

    # compara com códigos do SHP
    if codigo_arquivo_norm in codigos:
        caminho = os.path.join(pasta, arquivo)
        raster = QgsRasterLayer(caminho, arquivo)

        if raster.isValid():
            projeto.addMapLayer(raster, False)
            grupo.addLayer(raster)
            contador += 1
        else:
            print(f"Erro ao carregar: {arquivo}")

print(f"{contador} arquivos carregados no projeto.")
