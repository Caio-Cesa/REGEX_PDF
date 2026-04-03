import re
import PyPDF2
from typing import List, Dict

def extract_data_from_page(page_text: str) -> dict:
    extracted_data = {}

    # Processo
    match_processo = re.search(r'^(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})', page_text, re.MULTILINE)
    extracted_data['Processo'] = match_processo.group(1).strip() if match_processo else None

    # Cálculo
    match_calculo = re.search(r'Cálculo: (\d+)', page_text)
    extracted_data['Cálculo'] = match_calculo.group(1).strip() if match_calculo else None

    # Reclamante e Data Liquidação
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

    # Carga Horária (Padrão) e Admissão
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


def extrair_dados_texto(pdf_path: str) -> List[Dict]:
    """Lê as páginas do PDF e aplica as Expressões Regulares de extração nos textos estruturados."""
    print(f"[{pdf_path}] Iniciando extração de dados brutos (Regex)...")
    
    all_extracted_data = []

    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            print(f"[{pdf_path}] PDF lido via PyPDF2. Páginas Totais: {len(pdf_reader.pages)}")
            
            for i in range(len(pdf_reader.pages)):
                page_text = pdf_reader.pages[i].extract_text()

                if 'Dados do Cálculo' in page_text:
                    print(f"Processing page {i + 1} (0-indexed page {i})")
                    extracted_info = extract_data_from_page(page_text)
                    all_extracted_data.append(extracted_info)
    except Exception as e:
        print(f"Erro ao tentar ler o PDF com PyPDF2: {e}")
        
    print(f"[{pdf_path}] Extraídos dados de texto em {len(all_extracted_data)} página(s) relevante(s).")
    return all_extracted_data
