import os

import pandas as pd
import glob
from fpdf import FPDF
import pathlib


def generate(input_path, pdf_path, product_id, product_name, amount_purchased,
             price_per_unit, total_price):
    """
    This is to create invoice Excel files to pdf
    :param input_path:
    :param pdf_path:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :return:
    """
    filepaths = glob.glob(f"{input_path}/*.xlsx")

    for files in filepaths:

        filepath = pathlib.Path(files).stem

        name, date = filepath.split('-')
        pdf = FPDF(orientation='P', unit="mm", format='A4')

        pdf.add_page()
        pdf.set_font(family='Times', style='B', size=20)
        pdf.cell(w=50, h=10, txt=f"Invoice No. {name}", border=0, align="L", ln=1)
        pdf.cell(w=50, h=10, txt=f"Date {date}", border=0, align="L", ln=1)
        pdf.ln(2)
        df = pd.read_excel(files, sheet_name="Sheet 1")

        # Processing and adding headers
        columns = df.columns
        columns = [item.replace("_", " ").title() for item in columns]
        pdf.set_font(family='Times', size=12, style='B')
        pdf.cell(w=30, h=8, txt=columns[0], border=1)
        pdf.cell(w=70, h=8, txt=columns[1], border=1)
        pdf.cell(w=36, h=8, txt=columns[2], border=1)
        pdf.cell(w=30, h=8, txt=columns[3], border=1)
        pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)

        # Processing and adding columns
        for index, row in df.iterrows():
            pdf.set_font(family='Times', size=12)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
            pdf.cell(w=70, h=8, txt=str(row[product_name]), border=1)
            pdf.cell(w=36, h=8, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[total_price]), border=1, ln=1)

        if not os.path.exists(pdf_path):
            os.makedirs(pdf_path)
        pdf.output(f"{pdf_path}/{filepath}.pdf")