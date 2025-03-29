import pandas as pd
from tabula import read_pdf
import zipfile

# Configurações
pdf_path = "Anexo.pdf"
output_csv = "procedimentos_saude.csv"
zip_name = "Jeferson_Augusto.zip"  

# Extrair tabelas de todas as páginas do PDF
tables = read_pdf(
    pdf_path, 
    pages="all", 
    multiple_tables=True,
    lattice=True,
    pandas_options={'header': None}
)

# Combinar tabelas e pular linhas de cabeçalho duplicadas
df = pd.concat([table.iloc[1:] for table in tables if not table.empty])

# Cabeçalho 
header = [
    "PROCEDIMENTO", "RN_alteracao", "VIGENCIA", "OD", "AMB", "HCO", 
    "HSO", "REF", "PAC", "DUT", "SUBGRUPO", "GRUPO", "CAPITULO"
]

df.columns = header

# Substituir abreviações
df.replace({
    "OD": {"OD": "Seg. Odontológica"},
    "AMB": {"AMB": "Seg. Ambulatorial"}
}, inplace=True)

# Salvar CSV
df.to_csv(output_csv, index=False)

# Compactar em ZIP
with zipfile.ZipFile(zip_name, 'w') as zipf:
    zipf.write(output_csv)
