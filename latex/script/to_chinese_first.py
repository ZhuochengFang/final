#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX_FILES = list(ROOT.rglob('*.tex'))
TEX_FILES = [p for p in TEX_FILES if p.is_file()]
TEX_FILES.sort()

# Pairs of (English full, abbreviation, Chinese)
PAIRS = [
    ('Floating Inverter Amplifier', 'FIA', '浮动反相放大器'),
    ('Complementary Metal–Oxide–Semiconductor', 'CMOS', '互补金属氧化物半导体'),
    ('Analog-to-Digital Converter', 'ADC', '模数转换器'),
    ('Swing-Enhanced Floating Inverter Amplifier', 'SEFIA', '摆幅增强型浮动反相放大器'),
    ('P-channel Metal–Oxide–Semiconductor', 'PMOS', 'p沟道金属氧化物半导体'),
    ('N-channel Metal–Oxide–Semiconductor', 'NMOS', 'n沟道金属氧化物半导体'),
    ('common-mode voltage', 'VCM', '共模电压'),
    ('VDD', 'VDD', '电源正极'),
    ('VSS', 'VSS', '电源负极'),
    ('gate–source voltage', 'VGS', '栅源电压'),
    ('Low-Voltage Floating Inverter Amplifier', 'LVFIA', '低压浮动反相放大器'),
    ('Switched-Capacitor', 'SC', '开关电容'),
    ('Operational Transconductance Amplifier', 'OTA', '运算跨导放大器'),
    ('Signal-to-Noise-and-Distortion Ratio', 'SNDR', '信噪失真比'),
    ('Multi-Stage Noise Shaping', 'MASH', '多级噪声整形'),
    ('Charge-Redistribution CLS', 'CR-CLS', '电荷重分配 CLS'),
    ('Correlated Level Shifting', 'CLS', '相关电平移位'),
]

report = []

for f in TEX_FILES:
    s = f.read_text(encoding='utf-8')
    orig = s
    changed = False
    for eng, abbr, chi in PAIRS:
        # match patterns like "English (ABBR，中文)" or "English (ABBR, 中文)"
        pattern = re.compile(re.escape(eng) + r"\s*\(\s*" + re.escape(abbr) + r"[，,]\s*" + re.escape(chi) + r"\s*\)")
        # replacement: Chinese (English, ABBR)
        repl = f"{chi} ({eng}, {abbr})"
        s, n = pattern.subn(repl, s)
        if n > 0:
            changed = True
            report.append(f'- Replaced {eng} ({abbr}，{chi}) -> {chi} ({eng}, {abbr}) in {f.relative_to(ROOT)}: {n} occurrence(s)')
    if changed:
        f.write_text(s, encoding='utf-8')

# Also handle cases where previous script inserted exactly "{eng} ({abbr}，{chi})" with chinese comma
# Ensure we also match unicode variants of dash in eng term; above uses exact eng strings

report_path = ROOT / 'doc_thesis' / 'ABBREVIATIONS_CHANGES_CN.md'
report_path.write_text('# Chinese-first replacements report\n\n' + '\n'.join(report) + '\n', encoding='utf-8')
print('Done. Report:', report_path)
