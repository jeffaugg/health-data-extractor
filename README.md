# Health Data Extractor - Processamento de PDFs da ANS

Este projeto tem como objetivo extrair tabelas de um PDF específico da Agência Nacional de Saúde Suplementar (ANS), processar os dados e gerar um arquivo CSV compactado. O script utiliza `tabula-py` para extração de tabelas e `pandas` para manipulação dos dados, com suporte a containerização via Docker para isolamento de dependências.

## Sumário

- [Tecnologias e Dependências](#tecnologias-e-dependências)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Java Requirement](#java-requirement)
- [Instalação e Configuração](#instalação-e-configuração)
    - [Execução Local (Com Java)](#execução-local-com-java)
    - [Execução via Docker (Sem Java Local)](#execução-via-docker-sem-java-local)
- [Fluxo de Processamento](#fluxo-de-processamento)
- [Considerações Técnicas](#considerações-técnicas)

## Tecnologias e Dependências

### Core Components
- **Linguagem:** Python 3.9
- **PDF Processing:** `tabula-py` (Java-based PDF table extraction)
- **Data Manipulation:** `pandas`, `numpy`
- **Containerização:** Docker + Docker Compose

### Dependências Python (`requirements.txt`)
```
pandas==1.5.3
numpy==1.23.5
tabula-py==2.8.0
```

## Java Requirement

### Por que Java é necessário?
O tabula-py é um wrapper Python para a biblioteca Java Tabula. Esta dependência é crucial porque:

- **Engine de Extração:** Todo o processamento de PDF é feito pela engine Java
- **Desempenho:** O Java oferece melhor performance para parsing de PDFs complexos
- **Compatibilidade:** Garante extração precisa de tabelas em layout complexo

### Solução Docker
O Docker resolve automaticamente a dependência do Java através:

```dockerfile
RUN apt-get install -y openjdk-17-jre-headless
```

Isso elimina a necessidade de instalação manual do Java no sistema host.

## Estrutura do Projeto

```
.
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── src/
│   └── script.py          # Script principal de processamento
├── Anexo.pdf              # Arquivo PDF de entrada
└── output/                # Pasta gerada com resultados
        ├── procedimentos_saude.csv
        └── Jeferson_Augusto.zip
```

## Instalação e Configuração

### Execução Local (Com Java)
Pré-requisitos:

- Java JDK/JRE 17+ ([Download Oracle](https://www.oracle.com/java/technologies/downloads/))
- Python 3.9+

Verifique a instalação do Java:

```bash
java -version
# Deve retornar: openjdk 17.0.x ou superior
```

Instale as dependências Python:

```bash
pip install -r requirements.txt
```

Execute o script:

```bash
python src/script.py
```

### Execução via Docker (Sem Java Local)
Pré-requisitos:

- Docker Engine 20.10+
- Docker Compose 2.0+

Construa e execute:

```bash
docker-compose build && docker-compose up
```

Resultados:
- Arquivos gerados em `./output/`

## Fluxo de Processamento

### Configuração Inicial

```python
pdf_path = "Anexo.pdf"  # Input PDF
output_dir = "output"   # Output directory
```

### Extração de Tabelas

```python
tables = read_pdf(
        pdf_path, 
        pages="all",
        lattice=True  # Detect table borders
)
```

### Consolidação de Dados

```python
df = pd.concat([table.iloc[1:] for table in tables])
```

### Padronização de Cabeçalhos

```python
header = [
        "PROCEDIMENTO", "RN_alteracao", "VIGENCIA", 
        "OD", "AMB", "HCO", "HSO", "REF", 
        "PAC", "DUT", "SUBGRUPO", "GRUPO", "CAPITULO"
]
```

### Transformação de Dados

```python
df.replace({
        "OD": {"OD": "Seg. Odontológica"},
        "AMB": {"AMB": "Seg. Ambulatorial"}
}, inplace=True)
```

### Saída dos Resultados

- Geração do CSV
- Compactação para ZIP

## Considerações Técnicas

### Java no Docker

- Versão 17 do OpenJDK
- Configuração automática de PATH
- Isolamento completo do ambiente

### Processamento de PDF

- Suporte a múltiplas tabelas por página
- Detecção automática de bordas (`lattice=True`)
- Paginação completa (`pages="all"`)

### Gestão de Dependências

- Versões fixas no `requirements.txt`
- Build reproduzível via Docker

