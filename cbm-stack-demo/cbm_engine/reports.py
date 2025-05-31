from .utils import load_sensor_data, compute_rms, compute_fft, migrated_rms, detect_threshold
from fpdf import FPDF


def generate_report(filepath, output_path="report.pdf"):
    signal = load_sensor_data(filepath)

    all_accel = []
    for sensor in signal:
        all_accel.extend(sensor['data']['acceleration'])

    rms = compute_rms(all_accel)
    fft_vals = compute_fft(all_accel)
    alert = bool(detect_threshold(rms, threshold=0.6))
    migrated = migrated_rms(all_accel)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Rapport CBM", ln=True, align="C")

    pdf.cell(200, 10, txt=f"RMS : {rms:.4f}", ln=True)
    pdf.cell(200, 10, txt=f"RMS MATLAB : {migrated:.4f}", ln=True)
    pdf.cell(200, 10, txt=f"Alerte Seuil : {'OUI' if alert else 'NON'}", ln=True)
    pdf.cell(200, 10, txt="FFT (top 10) :", ln=True)

    for val in fft_vals[:10]:
        pdf.cell(200, 10, txt=f"{val:.4f}", ln=True)

    pdf.output(output_path)
