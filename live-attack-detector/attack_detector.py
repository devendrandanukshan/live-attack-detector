import re
from fpdf import FPDF
from collections import defaultdict

FAILED_LIMIT = 5
ip_counter = defaultdict(int)
ip_logs = defaultdict(list)

def analyze_logs(log_file):
    with open(log_file) as f:
        for line in f:
            if "Failed password" in line:
                match_ip = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)
                match_time = re.search(r"^(\w+\s+\d+\s[\d:]+)", line)
                if match_ip and match_time:
                    ip = match_ip.group(1)
                    time = match_time.group(1)
                    ip_counter[ip] += 1
                    ip_logs[ip].append(time)

def generate_pdf_report(output_path="attack_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Brute Force Attack Report", ln=True, align='C')

    for ip, times in ip_logs.items():
        if ip_counter[ip] > FAILED_LIMIT:
            pdf.cell(200, 10, txt=f"\nIP: {ip} (Attempts: {ip_counter[ip]})", ln=True)
            for t in times:
                pdf.cell(200, 10, txt=f" - {t}", ln=True)

    pdf.output(output_path)
    print(f"[+] PDF report saved to {output_path}")

if __name__ == "__main__":
    analyze_logs("auth.log")
    generate_pdf_report()
