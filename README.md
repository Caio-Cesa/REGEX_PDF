# PDF Data Extractor - Automação de Cálculos Judiciais ⚖️

Este projeto automatiza a extração, limpeza e consolidação de dados de cálculos judiciais a partir de arquivos PDF volumosos. Ele transforma milhares de páginas de informações não estruturadas em planilhas Excel organizadas, prontas para análise e integração com bancos de dados.

---

## 📌 Contexto e Problema
O processamento manual de documentos jurídicos, especialmente de cálculos que podem ultrapassar **4.400 páginas**, é inviável, propenso a erros e extremamente demorado. O desafio consistia em:
- Extrair tabelas complexas que se quebram entre várias páginas.
- Capturar dados específicos (Número do Processo, Reclamante, Datas de Admissão/Demissão) espalhados pelo texto.
- Padronizar valores monetários brasileiros (Vírgulas/Pontos) para o formato decimal computacional (`float`).

## 💡 A Solução Desenvolvida
Foi desenvolvida uma aplicação robusta em Python com arquitetura **modular**, garantindo que cada parte do processo de extração seja independente e fácil de manter. 

A solução utiliza:
1.  **Extração de Tabelas (Tabula-py):** Varredura de grades de dados com reconstrução inteligente de cabeçalhos.
2.  **Processamento de Texto (Regex + PyPDF2):** Uso de Expressões Regulares avançadas para capturar metadados críticos em milhares de páginas.
3.  **Engenharia de Dados (Pandas):** Cruzamento de dados (Merge) e sanitização financeira.

---

## 🚀 Funcionalidades
- [x] **Arquitetura Modular:** Divisão em `main`, `table_extractor`, `text_extractor` e `data_processor`.
- [x] **Processamento em Larga Escala:** Testado com sucesso em documentos de +4.400 páginas.
- [x] **Limpeza de Dados:** Conversão automática de padrões monetários e tratativa de valores nulos.
- [x] **Interface Amigável:** Logs de progresso em tempo real no terminal.

## 🛠️ Tecnologias Utilizadas
- **Python 3.11+**
- **Pandas:** Manipulação e Cruzamento de DataFrames.
- **Tabula-py / JPype1:** Extração de tabelas via Java Bridge.
- **PyPDF2:** Leitura e análise de texto em PDF.
- **OpenPyXL:** Exportação de planilhas Excel (`.xlsx`).

---

## 📂 Arquitetura do Projeto
A modularização foi implementada seguindo os princípios de responsabilidade única:

- `main.py`: Orquestrador central e ponto de entrada.
- `table_extractor.py`: Lógica específica para o Tabula e limpeza de tabelas.
- `text_extractor.py`: Regras de Regex e extração de texto bruto.
- `data_processor.py`: Tratamento de dados e exportação final.

---

## 📝 Como usar
1.  Garanta que o **Java** e o **Python** estejam instalados.
2.  Instale as dependências:
    ```bash
    pip install PyPDF2 tabula-py jpype1 pandas openpyxl
    ```
3.  Coloque os arquivos `dados.pdf` e `dados1.pdf` na pasta raiz.
4.  Execute a aplicação:
    ```bash
    python main.py
    ```

---

## 📊 Resultados Alcançados
No último benchmark realizado:
- **Páginas Analisadas:** 4.445
- **Registros Relevantes Identificados:** 1.051
- **Tempo Estimado de Economia:** ~30 horas de trabalho manual por arquivo processado.

> [!IMPORTANT]
> Os arquivos de entrada (`.pdf`) e saída (`.xlsx`) são automaticamente ignorados pelo controle de versão para garantir a privacidade de dados sensíveis.

---
**Desenvolvido por Caio Cesar de Albuquerque**  
📫 [caioalbuquerquedev@gmail.com](mailto:caioalbuquerquedev@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/caio-cesar-for-hire) | [GitHub](https://github.com/Caio-Cesa)
