import pandas as pd
from tabula import read_pdf
import zipfile
import os  

# Configurações
pdf_path = "Anexo.pdf"
output_dir = "output"
output_csv = os.path.join(output_dir, "procedimentos_saude.csv")
zip_name = os.path.join(output_dir, "Jeferson_Augusto.zip")

# Criar diretório de saída, se não existir
os.makedirs(output_dir, exist_ok=True)

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
