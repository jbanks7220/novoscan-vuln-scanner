from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTextEdit,
    QFileDialog, QLabel, QLineEdit, QProgressBar
)
from PyQt5.QtCore import QTimer
from scanner.safe_scan import run_safe_scan
from exporter.exporter import export_report


class ScannerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NovoScan Vulnerability Scanner")
        self.setGeometry(250, 150, 900, 650)

        self.setStyleSheet("""
            QWidget {
                background-color: #0b0b0d;
                color: #e6e6eb;
                font-family: Consolas;
            }
            QPushButton {
                background-color: #6d3cff;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #5930cc;
            }
            QLineEdit {
                background-color: #2f2f33;
                padding: 8px;
                border-radius: 4px;
            }
            QTextEdit {
                background-color: #111114;
                border: 1px solid #2f2f33;
            }
            QProgressBar {
                background-color: #2f2f33;
                height: 18px;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background-color: #6d3cff;
            }
        """)

        layout = QVBoxLayout()

        self.title = QLabel("NovoScan — Advanced Vulnerability Scanner")
        self.title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.title)

        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Enter target domain(s) — example: localhost, testsite.local")
        layout.addWidget(self.target_input)

        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        layout.addWidget(self.terminal)

        self.scan_btn = QPushButton("Start Scan")
        self.scan_btn.clicked.connect(self.start_scan)
        layout.addWidget(self.scan_btn)

        self.export_btn = QPushButton("Export Report")
        self.export_btn.clicked.connect(self.export_results)
        layout.addWidget(self.export_btn)

        self.setLayout(layout)
        self.results = []
        self.timer = QTimer()
        self.fake_steps = []
        self.step_index = 0

    def start_scan(self):
        self.terminal.clear()
        self.progress.setValue(0)

        targets = self.target_input.text().strip()
        if not targets:
            self.terminal.append("[!] No target specified.")
            return

        self.fake_steps = [
            "[*] Initializing scan engine...",
            "[*] Resolving DNS...",
            "[*] Mapping attack surface...",
            "[*] Scanning open ports...",
            "[*] Fingerprinting services...",
            "[*] Enumerating databases...",
            "[*] Calculating CVSS scores...",
            "[*] Finalizing report..."
        ]
        self.step_index = 0

        self.timer.timeout.connect(lambda: self.fake_terminal_output(targets))
        self.timer.start(400)

    def fake_terminal_output(self, targets):
        if self.step_index < len(self.fake_steps):
            self.terminal.append(self.fake_steps[self.step_index])
            self.progress.setValue(int((self.step_index + 1) / len(self.fake_steps) * 100))
            self.step_index += 1
        else:
            self.timer.stop()
            self.results = run_safe_scan(targets)
            self.terminal.append("\n=== SCAN RESULTS ===\n")
            for r in self.results:
                self.terminal.append(
                    f"[{r['severity']} | CVSS {r['cvss']}] {r['name']} — {r['description']}"
                )

    def export_results(self):
        if not self.results:
            self.terminal.append("\n[!] No results to export.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Report", "", "All Files (*)")
        if file_path:
            export_report(self.results, file_path)
            self.terminal.append(f"\n[+] Report exported to {file_path}")
