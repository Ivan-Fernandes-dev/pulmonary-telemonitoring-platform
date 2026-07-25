from flask import Flask, render_template, request, jsonify, Response, send_file
import sqlite3
import io
from reportlab.pdfgen import canvas
app = Flask(__name__)

def get_latest_measurement():
    conn = sqlite3.connect("pulmonary_monitoring.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM measurements
        ORDER BY id DESC
        LIMIT 1
    """)

    measurement = cursor.fetchone()

    if measurement is None:
        measurement = {
            "id": 0,
            "patient_id": 1,
            "oxygen_saturation": 0,
            "heart_rate": 0,
            "temperature": 0,
            "respiratory_rate": 0,
            "movement": "Sem medição",
            "ambient_temperature": 0,
            "humidity": 0
        }
    else:
        measurement = dict(measurement)

    if "movement" not in measurement or measurement["movement"] is None:
        measurement["movement"] = "Sem movimento"

    if "ambient_temperature" not in measurement or measurement["ambient_temperature"] is None:
        measurement["ambient_temperature"] = 27.0

    if "humidity" not in measurement or measurement["humidity"] is None:
        measurement["humidity"] = 60

    conn.close()

    return measurement

@app.route("/")
def index():
    latest_measurement = get_latest_measurement()
    return render_template(
        "dashboard.html",
        measurement=latest_measurement
    )
@app.route("/reports")
def reports():
    conn = sqlite3.connect("pulmonary_monitoring.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM measurements
        ORDER BY id DESC
    """)

    measurements = cursor.fetchall()

    conn.close()

    return render_template(
    "reports.html",
    measurements=measurements,
    ids=[m["id"] for m in measurements],
    spo2=[m["oxygen_saturation"] for m in measurements],
    fc=[m["heart_rate"] for m in measurements],
    temp=[m["temperature"] for m in measurements],
    fr=[m["respiratory_rate"] for m in measurements]
)
@app.route("/api/reports-data")
def reports_data():
    conn = sqlite3.connect("pulmonary_monitoring.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, oxygen_saturation, heart_rate, temperature, respiratory_rate
        FROM measurements
        ORDER BY id DESC
        LIMIT 30
    """)

    rows = cursor.fetchall()
    conn.close()

    rows = list(reversed(rows))

    return jsonify({
        "ids": [row["id"] for row in rows],
        "spo2": [row["oxygen_saturation"] for row in rows],
        "fc": [row["heart_rate"] for row in rows],
        "temp": [row["temperature"] for row in rows],
        "fr": [row["respiratory_rate"] for row in rows]
    })    
@app.route("/api/measurement", methods=["POST"])
def receive_measurement():
    data = request.get_json()
    data["movement"] = data.get("movement", "Sem movimento")  
     
    conn = sqlite3.connect("pulmonary_monitoring.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO measurements
        (patient_id,oxygen_saturation, heart_rate, temperature, respiratory_rate, movement, ambient_temperature, humidity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        1,
        data["spo2"],
        data["heart_rate"],
        data["temperature"],
        data["respiratory_rate"],
        data["movement"],
        data["ambient_temperature"],
        data["humidity"]
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "Medição salva com sucesso",
        "dados": data
    })
@app.route("/export/csv")
def export_csv():
    conn = sqlite3.connect("pulmonary_monitoring.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, patient_id, oxygen_saturation, heart_rate, temperature,
               respiratory_rate, movement, ambient_temperature, humidity, measured_at
        FROM measurements
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    csv_data = "\ufeffsep=;\nID;Paciente;SpO2;Frequencia Cardiaca;Temperatura Corporal;Frequencia Respiratoria;Movimento;Temperatura Ambiente;Umidade;Data/Hora\n"

    for row in rows:
        csv_data += f"{row['id']};{row['patient_id']};{row['oxygen_saturation']};{row['heart_rate']};{row['temperature']};{row['respiratory_rate']};{row['movement']};{row['ambient_temperature']};{row['humidity']};{row['measured_at']}\n"

    return Response(
        csv_data,
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=relatorio_monitoramento_pulmonar.csv"}
    )

@app.route("/export/pdf")
def export_pdf():
    conn = sqlite3.connect("pulmonary_monitoring.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, patient_id, oxygen_saturation, heart_rate, temperature,
               respiratory_rate, movement,
               ambient_temperature, humidity, measured_at
        FROM measurements
        ORDER BY id DESC
        LIMIT 20
    """)

    rows = cursor.fetchall()
    conn.close()

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.setTitle("Relatorio de Monitoramento Pulmonar")

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 800, "Smart Pulmonary Recovery Monitoring Project")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, 780, "Relatorio clinico de acompanhamento do paciente")

    y = 740

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, y, "ID")
    pdf.drawString(90, y, "Paciente")
    pdf.drawString(150, y, "SpO2")
    pdf.drawString(200, y, "FC")
    pdf.drawString(250, y, "Temp.")
    pdf.drawString(310, y, "FR")
    pdf.drawString(360, y, "Movimento")
    pdf.drawString(460, y, "Data/Hora")

    y -= 20
    pdf.setFont("Helvetica", 9)

    for row in rows:
        pdf.drawString(50, y, str(row["id"]))
        pdf.drawString(90, y, str(row["patient_id"]))
        pdf.drawString(150, y, str(row["oxygen_saturation"]))
        pdf.drawString(200, y, str(row["heart_rate"]))
        pdf.drawString(250, y, str(row["temperature"]))
        pdf.drawString(310, y, str(row["respiratory_rate"]))
        pdf.drawString(360, y, str(row["movement"]))
        pdf.drawString(460, y, str(row["measured_at"]))
        y -= 18

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="relatorio_monitoramento_pulmonar.pdf",
        mimetype="application/pdf"
    )





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
            
    
