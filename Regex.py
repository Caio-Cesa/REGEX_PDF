# Instale as dependências no terminal usando:
# pip install PyPDF2 tabula-py "camelot-py[cv]" openpyxl pandas

import PyPDF2
import tabula
import re
import pandas as pd

pdf_file = open('dados1.pdf', 'rb')
pdf = PyPDF2.PdfReader(pdf_file)
paginas = len(pdf.pages)
print(f"Páginas (dados1.pdf): {paginas}")

tabelacomum = tabula.read_pdf('dados1.pdf', pages='all')
for tabela in tabelacomum:
    print(tabela)

print("--- Conteúdo original da tabelacomum[1] (equivalente à 'Tabela 2') ---")
print(tabelacomum[1])

cleaned_tables = []

# A tabela com o cabeçalho correto é tabelacomum[1] (a 'Tabela 2' do usuário).
# Vamos extrair os nomes das colunas dela para usar como referência.
if len(tabelacomum) > 1:
    # A primeira tabela de dados relevante (Tabela 2) é tabelacomum[1]
    reference_columns = tabelacomum[1].columns.tolist()
    cleaned_tables.append(tabelacomum[1]) # Adiciona a Tabela 2 com seu cabeçalho original
else:
    print("Não há tabelas suficientes para processar. Esperado pelo menos tabelacomum[1].")

# Itera sobre as tabelas extraídas, a partir de tabelacomum[2] (Tabela 3) até tabelacomum[29] (Tabela 30).
for i in range(2, min(30, len(tabelacomum))):
    table_df = tabelacomum[i]

    if not table_df.empty:
        # Remove a primeira linha (cabeçalho repetido)
        processed_df = table_df.iloc[1:].copy().reset_index(drop=True)

        # Se o DataFrame processado não estiver vazio e tiver o número correto de colunas,
        # renomeia as colunas para o padrão de referência. Caso contrário, adiciona um DataFrame vazio
        # com as colunas corretas para garantir consistência na concatenação.
        if not processed_df.empty and len(processed_df.columns) == len(reference_columns):
            processed_df.columns = reference_columns
            cleaned_tables.append(processed_df)
        elif not processed_df.empty:
            print(f"Aviso: Tabela {i+1} (originalmente tabelacomum[{i}]) tem número de colunas inconsistente. Tentando reindexar.")
            # Se o número de colunas for diferente, podemos tentar reindexar ou preencher com NaN
            temp_df = pd.DataFrame(columns=reference_columns) # Cria um DF vazio com as colunas certas
            for col_idx, col_name in enumerate(reference_columns):
                if col_idx < len(processed_df.columns):
                    temp_df[col_name] = processed_df.iloc[:, col_idx]
            cleaned_tables.append(temp_df)
        else:
            # Se o DataFrame processado estiver vazio (ex: só tinha cabeçalho), adiciona um DataFrame vazio
            cleaned_tables.append(pd.DataFrame(columns=reference_columns))
    else:
        # Se o DataFrame original já estiver vazio, adiciona um DataFrame vazio com as colunas de referência
        cleaned_tables.append(pd.DataFrame(columns=reference_columns))

print("Tabelas processadas (cabeçalhos repetidos removidos das páginas seguintes e ignorando tabelas fora do intervalo solicitado):")
# Agora, 'cleaned_tables' contém as tabelas sem os cabeçalhos repetidos e no intervalo desejado.
# Ajustamos a numeração para corresponder à percepção do usuário (Tabela 2, Tabela 3, etc.).
for j, cleaned_table in enumerate(cleaned_tables):
    print(f"\n--- Tabela {j+2} (originalmente tabelacomum[{j+1}]) ---")
    print(cleaned_table)

# Concatenar as tabelas limpas em um único DataFrame final
try:
    final_combined_df = pd.concat(cleaned_tables, ignore_index=True)
    print("\n--- Todas as tabelas concatenadas --- ")
    print(final_combined_df)
except Exception as e:
    print(f"\nNão foi possível concatenar as tabelas devido a um erro: {e}")
    print("Verifique se as colunas são consistentes entre as tabelas antes de concatenar.")
final_combined_df.info()

output_filename = 'saida.xlsx'
final_combined_df.to_excel(output_filename, index=False, engine='openpyxl')

print(f"O DataFrame foi exportado com sucesso para '{output_filename}'")

pdf_file = open('dados.pdf', 'rb')
pdf = PyPDF2.PdfReader(pdf_file)
paginas = len(pdf.pages)
print(f"Páginas do dados.pdf: {paginas}")

#função nova com melhorias caso de erro para todas as paginas pegar a função la de baixo pois e mais antiga
def extract_data_from_page(page_text):
    extracted_data = {}

    # Processo
    match_processo = re.search(r'^(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})', page_text, re.MULTILINE)
    extracted_data['Processo'] = match_processo.group(1).strip() if match_processo else None

    # Cálculo
    match_calculo = re.search(r'Cálculo: (\d+)', page_text)
    extracted_data['Cálculo'] = match_calculo.group(1).strip() if match_calculo else None

    # Reclamante e Data Liquidação:
    match_reclamante_liquidacao = re.search(
        r'.*(\d{2}/\d{2}/\d{4})([A-Z\sÇÉÃÕÚúáéíóúâêîôûÄËÏÖÜÿàèìòù\u00C0-\u017F-]+)\nData Liquidação:Reclamado:',
        page_text, re.DOTALL)

    if match_reclamante_liquidacao:
        extracted_data['Data Liquidação'] = match_reclamante_liquidacao.group(1).strip()
        extracted_data['Reclamante'] = match_reclamante_liquidacao.group(2).strip()
    else:
        match_reclamante_liquidacao_alt = re.search(
            r'.*(\d{2}/\d{2}/\d{4})\s*([A-Z\sÇÉÃÕÚúáéíóúâêîôûÄËÏÖÜÿàèìòù\u00C0-\u017F-]+)\s*\nData Liquidação:',
            page_text, re.DOTALL)
        if match_reclamante_liquidacao_alt:
            extracted_data['Data Liquidação'] = match_reclamante_liquidacao_alt.group(1).strip()
            extracted_data['Reclamante'] = match_reclamante_liquidacao_alt.group(2).strip()
        else:
            extracted_data['Data Liquidação'] = None
            extracted_data['Reclamante'] = None

    # Período do Cálculo
    match_periodo_calculo = re.search(r'Reclamante:\n(\d{2}/\d{2}/\d{4} a \d{2}/\d{2}/\d{4})', page_text, re.DOTALL)
    extracted_data['Período do Cálculo'] = match_periodo_calculo.group(1).strip() if match_periodo_calculo else None

    # Data Ajuizamento
    match_data_ajuizamento = re.search(r'(\d{2}/\d{2}/\d{4}) Data Ajuizamento:', page_text)
    extracted_data['Data Ajuizamento'] = match_data_ajuizamento.group(1).strip() if match_data_ajuizamento else None

    # Carga Horária (Padrão) and Admissão
    match_carga_admissao = re.search(r'Não\n(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)(\d{2}/\d{2}/\d{4})\nNão', page_text)
    if match_carga_admissao:
        extracted_data['Carga Horária (Padrão)'] = match_carga_admissao.group(1).strip()
        extracted_data['Admissão'] = match_carga_admissao.group(2).strip()
    else:
        extracted_data['Carga Horária (Padrão)'] = None
        extracted_data['Admissão'] = None

    # Demissão
    match_demissao = re.search(r'Sim\nSim\nSim(\d{2}/\d{2}/\d{4})', page_text)
    extracted_data['Demissão'] = match_demissao.group(1).strip() if match_demissao else None

    # Regime de Trabalho
    match_regime_trabalho = re.search(r'BELO HORIZONTE\n(Tempo Integral)', page_text)
    extracted_data['Regime de Trabalho'] = match_regime_trabalho.group(1).strip() if match_regime_trabalho else None

    return extracted_data

# Re-opening the PDF file as it might have been closed or the pointer moved
pdf_file_path = 'dados.pdf'
pdf_file = open(pdf_file_path, 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)

all_extracted_data = []

for i in range(len(pdf_reader.pages)):
    page_text = pdf_reader.pages[i].extract_text()

    if 'Dados do Cálculo' in page_text:
        print(f"Processing page {i + 1} (0-indexed page {i})")
        extracted_info = extract_data_from_page(page_text)
        all_extracted_data.append(extracted_info)
    else:
        pass

pdf_file.close()

print(f"\nExtracted data from {len(all_extracted_data)} relevant pages.")
if all_extracted_data:
    print("First 3 extracted data entries:")
    for j, data_entry in enumerate(all_extracted_data[:3]):
        print(f"Entry {j+1}: {data_entry}")
else:
    print("No data was extracted.")

extracted_df = pd.DataFrame(all_extracted_data)

print("--- DataFrame created from extracted data ---")
extracted_df.info()
print(extracted_df.head(105))
print(f"Total rows in DataFrame: {len(extracted_df)}")

# Renomear a coluna 'Reclamante' em extracted_df para 'Nome Reclamante'
extracted_df_renamed = extracted_df.rename(columns={'Reclamante': 'Nome Reclamante'})

# Realizar a junção dos DataFrames
merged_df = pd.merge(final_combined_df, extracted_df_renamed, on='Nome Reclamante', how='left')

print("--- DataFrame combinado (merged_df) --- ")
print(merged_df.head())
merged_df.info()

def clean_numeric_value(value):
    if isinstance(value, str):
        cleaned_value = value.replace('.', '').replace(',', '.')
        try:
            return float(cleaned_value)
        except ValueError:
            return None
    return value

# Apply the cleaning function to 'Carga Horária (Padrão)' column
if 'Carga Horária (Padrão)' in merged_df.columns:
    merged_df['Carga Horária (Padrão)'] = merged_df['Carga Horária (Padrão)'].apply(clean_numeric_value)
    
if 'Cálculo' in merged_df.columns:
    merged_df['Cálculo'] = pd.to_numeric(merged_df['Cálculo'], errors='coerce')

# Convert other columns to numeric if they exist
if 'Bruto por Reclamante' in merged_df.columns:
    merged_df['Bruto por Reclamante'] = merged_df['Bruto por Reclamante'].apply(clean_numeric_value)
if 'Líquido por Reclamante' in merged_df.columns:
    merged_df['Líquido por Reclamante'] = merged_df['Líquido por Reclamante'].apply(clean_numeric_value)
if 'Total Devido pelo Reclamado' in merged_df.columns:
    merged_df['Total Devido pelo Reclamado'] = merged_df['Total Devido pelo Reclamado'].apply(clean_numeric_value)
if 'Débitos por Reclamante' in merged_df.columns:
    merged_df['Débitos por Reclamante'] = merged_df['Débitos por Reclamante'].apply(clean_numeric_value)

merged_df.info()
print(merged_df.head())

output_filename_extracted = 'Dados_Calculo_Extraidos.xlsx'
merged_df.to_excel(output_filename_extracted, index=False, engine='openpyxl')

print(f"The extracted data has been successfully exported to '{output_filename_extracted}'")