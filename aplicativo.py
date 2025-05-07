from flask import Flask, render_template, request, jsonify
import pyodbc
from datetime import datetime

app = Flask(__name__)

# Conexão com o banco de dados
def conectar():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=servidorprojecaoecom.database.windows.net;'
        'DATABASE=projecao_db;'
        'UID=rayaanminervinoecom;'
        'PWD=Novasenha123@;'
    )

@app.route('/')
def index():
    filtro_data = request.args.get("filtro_data")
    filtro_mes = request.args.get("filtro_mes")
    conn = conectar()
    cursor = conn.cursor()

    if filtro_data:
        cursor.execute("SELECT Data, Valor FROM ProjecaoVendas WHERE CAST(Data AS DATE) = ?", filtro_data)
    elif filtro_mes:
        cursor.execute("""
            SELECT Data, Valor FROM ProjecaoVendas
            WHERE MONTH(Data) = ? AND YEAR(Data) = ?
            ORDER BY Data
        """, (int(filtro_mes[5:]), int(filtro_mes[:4])))
    else:
        cursor.execute("SELECT Data, Valor FROM ProjecaoVendas ORDER BY Data")

    dados = []
    for row in cursor.fetchall():
        data = row[0]
        if isinstance(data, str):
            data_formatada = data.split(" ")[0]
        else:
            data_formatada = data.strftime("%Y-%m-%d")
        dados.append({"Data": data_formatada, "Valor": row[1]})

    conn.close()
    return render_template("index.html", dados=dados)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    data = request.json['data']
    valor = float(request.json['valor'])
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ProjecaoVendas (Data, Valor) VALUES (?, ?)", (data, valor))
    conn.commit()
    conn.close()
    return jsonify({'status': 'sucesso'})

@app.route('/editar', methods=['POST'])
def editar():
    data = request.json['data']
    valor = float(request.json['valor'])
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE ProjecaoVendas SET Valor = ? WHERE Data = ?", (valor, data))
    conn.commit()
    conn.close()
    return jsonify({'status': 'sucesso'})

@app.route('/excluir', methods=['POST'])
def excluir():
    data = request.json['data']
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ProjecaoVendas WHERE Data = ?", (data,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'sucesso'})

if __name__ == '__main__':
    app.run(debug=True)
