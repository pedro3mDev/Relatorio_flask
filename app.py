from flask import Flask, render_template, Response, make_response
import psycopg2
import psycopg2.extras
from fpdf import FPDF

app = Flask(__name__)

db_config = {
    'dbname': 'ucan.aulaJdbc',
    'user': 'postgres',
    'password': '0000',
    'host': 'localhost',
    'port': '5432'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download/report/pdf')
def download_report():
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM teste")
        result = cursor.fetchall()

        pdf = FPDF()
        pdf.add_page()
        page_width = pdf.w - 2 * pdf.l_margin
        pdf.set_font('arial', 'B', 14.0)
        pdf.cell(page_width, 0.0, 'Relatório (Ismael)', align='C')
        pdf.ln(10)
        pdf.set_font('arial', '', 12)
        
        col_width = page_width / 4
        th = pdf.font_size

        pdf.cell(col_width, th, 'ID', border=1)
        pdf.cell(col_width, th, 'Nome', border=1)
        pdf.ln(th)


        for i in range(0, len(result), 2):
            for j in range(2):  
                if i + j < len(result): 
                    pdf.cell(col_width, th, str(result[i + j]['id']), border=1)
                    pdf.cell(col_width, th, str(result[i + j]['nome']), border=1)
            pdf.ln(th)
        pdf.ln(40)

        pdf.set_font('arial', '', 10)
        pdf.cell(page_width, 0.0, '- -------------- - ', align='C')

        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
                        headers={'Content-Disposition': 'attachment;filename=relatorio.pdf'})

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro: {error}")
        return make_response("Erro ao gerar relatório", 500)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    app.run()




