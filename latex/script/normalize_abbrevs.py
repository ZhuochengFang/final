#!/usr/bin/env python3
import re
from pathlib import Path

# Mapping of abbreviations to (English full term, Chinese translation)
ABBR_MAP = {
    'FIA': ('Floating Inverter Amplifier', '浮动反相放大器'),
    'CMOS': ('Complementary Metal–Oxide–Semiconductor', '互补金属氧化物半导体'),
    'ADC': ('Analog-to-Digital Converter', '模数转换器'),
    # 'CDC' intentionally skipped for confirmation
    'SEFIA': ('Swing-Enhanced Floating Inverter Amplifier', '摆幅增强型浮动反相放大器'),
    'PMOS': ('P-channel Metal–Oxide–Semiconductor', 'p沟道金属氧化物半导体'),
    'NMOS': ('N-channel Metal–Oxide–Semiconductor', 'n沟道金属氧化物半导体'),
    'CI': ('CI', '浮空电容'),
    'CRES': ('CRES', '储能电容'),
    'CL': ('C_L', '负载电容'),
    'VCM': ('common-mode voltage', '共模电压'),
    'VDD': ('VDD', '电源正极'),
    'VSS': ('VSS', '电源负极'),
    'VGS': ('gate–source voltage', '栅源电压'),
    'CC1': ('CC1', '时序电容'),
    'CC2': ('CC2', '时序电容'),
    'VBP': ('VBP', '偏置电压'),
    'VBN': ('VBN', '偏置电压'),
    'LVFIA': ('Low-Voltage Floating Inverter Amplifier', '低压浮动反相放大器'),
    'SC': ('Switched-Capacitor', '开关电容'),
    'OTA': ('Operational Transconductance Amplifier', '运算跨导放大器'),
    'SNDR': ('Signal-to-Noise-and-Distortion Ratio', '信噪失真比'),
    'MASH': ('Multi-Stage Noise Shaping', '多级噪声整形'),
    'CR-CLS': ('Charge-Redistribution CLS', '电荷重分配 CLS'),
    'CLS': ('Correlated Level Shifting', '相关电平移位'),
    'A0': ('A0', '开环增益'),
}

ROOT = Path(__file__).resolve().parents[1]
TEX_FILES = list(ROOT.rglob('*.tex'))
TEX_FILES = [p for p in TEX_FILES if p.is_file()]
TEX_FILES.sort()

report_lines = []

# Helper to find if nearby text already contains the English or Chinese phrase
def context_has_fulltext(text, start_idx, english, chinese):
    window_start = max(0, start_idx - 200)
    window_end = min(len(text), start_idx + 200)
    window = text[window_start:window_end]
    if english and english in window:
        return True
    if chinese and chinese in window:
        return True
    return False

# For each abbreviation, find earliest occurrence across files and replace first standalone occurrence
for abbr, (eng, chi) in ABBR_MAP.items():
    done = False
    for f in TEX_FILES:
        s = f.read_text(encoding='utf-8')
        # match standalone word, not preceded by backslash (to avoid commands)
        pattern = re.compile(r'(?<!\\)\b' + re.escape(abbr) + r'\b')
        for m in pattern.finditer(s):
            idx = m.start()
            if context_has_fulltext(s, idx, eng, chi):
                report_lines.append(f'- {abbr}: already has full term near {f.relative_to(ROOT)} at pos {idx}')
                done = True
                break
            # make replacement: replace the token with 'English Full Term (ABBR，中文)'
            replacement = f"{eng} ({abbr}，{chi})"
            new_s = s[:m.start()] + replacement + s[m.end():]
            f.write_text(new_s, encoding='utf-8')
            report_lines.append(f'- {abbr}: inserted expansion in {f.relative_to(ROOT)} at pos {idx}')
            done = True
            break
        if done:
            break
    if not done:
        report_lines.append(f'- {abbr}: NOT FOUND in any .tex file')

# Special handling: CDC -> mark TODO occurrences
cdc_pattern = re.compile(r'(?<!\\)\bCDC\b')
cdc_found = False
for f in TEX_FILES:
    s = f.read_text(encoding='utf-8')
    if cdc_pattern.search(s):
        # insert a TODO comment at first occurrence: add '% TODO: confirm CDC meaning (Capacitance-to-Digital Converter?)' before the line
        lines = s.splitlines()
        for i, line in enumerate(lines):
            if 'CDC' in re.findall(r'(?<!\\)\bCDC\b', line):
                lines[i] = lines[i] + ' % TODO: confirm CDC meaning (Capacitance-to-Digital Converter / Charge-Domain Converter)'
                cdc_found = True
                report_lines.append(f'- CDC: annotated TODO in {f.relative_to(ROOT)} line {i+1}')
                break
        if cdc_found:
            f.write_text('\n'.join(lines), encoding='utf-8')
            break
if not cdc_found:
    report_lines.append('- CDC: not found')

# write report
report_path = ROOT / 'doc_thesis' / 'ABBREVIATIONS_CHANGES.md'
report_path.write_text('# Abbreviations normalization report\n\n' + '\n'.join(report_lines) + '\n', encoding='utf-8')
print('Done. Report written to', report_path)
