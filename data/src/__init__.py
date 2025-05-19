from os.path import abspath, dirname, join
import json

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def gerar_pdf_de_produtos(json_path, output_pdf):
    # Carrega os dados do JSON
    with open(json_path, "r", encoding="utf-8") as f:
        produtos = json.load(f)

    # Cria o documento PDF
    doc = SimpleDocTemplate(output_pdf, pagesize=A4)
    elementos = []

    # Cabeçalhos da tabela
    dados = [["Código", "Produto", "Valor Unitário (R$)"]]

    # Adiciona os dados
    for item in produtos:
        dados.append([
            item["codigo"],
            item["produto"],
            f"{item["valor_unitario"]:.2f}"
        ])

    # Cria a tabela
    tabela = Table(dados, colWidths=[80, 300, 120])

    # Estilo da tabela
    estilo = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (2, 1), (2, -1), "RIGHT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ])
    tabela.setStyle(estilo)

    elementos.append(tabela)
    doc.build(elementos)
    print(f"PDF gerado com sucesso: {output_pdf}")


if __name__ == "__main__":
    DATA_PATH = dirname(dirname(abspath(__file__)))

    print(DATA_PATH)

    source = DATA_PATH + "/src/mock/produtos.json"
    target = DATA_PATH + "/hospital_nf_mock.pdf"

    gerar_pdf_de_produtos(source, target)
