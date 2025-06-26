import re
import json
import os
from datetime import datetime
from typing import List, Optional, Dict, Any

method_pattern = r"(внутрь|в/в|в/м|п/к|подкожно|перорально|ингаляц|парабульбарно)"

def extract_all_dates(text: str) -> List[str]:
    dates = re.findall(r"\d{2}\.\d{2}\.\d{4}", text)
    return sorted(set(dates), key=lambda d: datetime.strptime(d, "%d.%m.%Y"))

def parse_period(start: str, end: str, min_date_str: str) -> str:
    date_format = "%d.%m.%Y"
    min_date = datetime.strptime(min_date_str, date_format)
    start_date = datetime.strptime(start, date_format)
    end_date = datetime.strptime(end, date_format)
    start_day = (start_date - min_date).days + 1
    end_day = (end_date - min_date).days + 1
    return f"{start_day}-{end_day}"

def extract_medicine_name(text: str) -> str:
    pattern = r"([А-ЯЁA-Z][^\d,]*)"
    match = re.match(pattern, text.strip())
    if match:
        name = match.group(1).strip()
        name = re.split(r"[\d,]", name)[0].strip()
        return name
    return "неизвестно"

def parse_medicines_from_line(line: str, min_date_str: str) -> Optional[Dict[str, Any]]:
    dates = re.findall(r"\d{2}\.\d{2}\.\d{4}", line)
    if len(dates) >= 2:
        date_start, date_end = dates[-2], dates[-1]
        period = parse_period(date_start, date_end, min_date_str)
    else:
        period = ""

    route_match = re.search(method_pattern, line, re.IGNORECASE)
    route = route_match.group(1).lower() if route_match else ""

    total_match = re.search(r"(\d+(?:[.,]\d+)?)\s*р/д", line)
    total = total_match.group(1).replace(',', '.') if total_match else ""

    if "Смесь" in line:
        line_wo_dates = re.sub(r"\d{2}\.\d{2}\.\d{4}", "", line).strip()
        parts = re.findall(r"(Смесь|[А-ЯЁ][^А-ЯЁ]*)", line_wo_dates)
        result = {}
        idx = 1
        for part in parts:
            part = part.strip()
            if not part:
                continue
            if part == "Смесь":
                result["name"] = "Смесь"
                result["route"] = route
                result["total"] = total
                continue
            name_match = re.match(r"([А-ЯЁ][^0-9%]*)", part)
            name = name_match.group(1).strip() if name_match else "неизвестно"
            dose_match = re.search(r"(\d+(?:[.,]\d+)?\s*%?\s*(мг|мл|ед|ЕД))", part, re.IGNORECASE)
            dosage = dose_match.group(1).strip() if dose_match else ""
            result[f"name_{idx}"] = name
            result[f"dosage_{idx}"] = dosage
            result[f"period_{idx}"] = period
            idx += 1
        return result if result else None
    else:
        name_match = re.match(r"([А-ЯЁ][^0-9%]*)", line)
        name = name_match.group(1).strip() if name_match else "неизвестно"
        dose_match = re.search(r"(\d+(?:[.,]\d+)?\s*%?\s*(мг|мл|ед|ЕД))", line, re.IGNORECASE)
        dosage = dose_match.group(1).strip() if dose_match else ""
        return {
            "name": name,
            "route": route,
            "dosage": dosage,
            "period": period,
            "total_day": total
        }

def process_block(block_text: str) -> Optional[List[Dict[str, Any]]]:
    all_dates = extract_all_dates(block_text)
    if not all_dates:
        return None
    min_date = all_dates[0]
    result = []
    for line in block_text.strip().splitlines():
        if re.search(r"\d{2}\.\d{2}\.\d{4}", line):
            med = parse_medicines_from_line(line, min_date)
            if med:
                result.append(med)
    return result if result else None

def process_file(input_path: str, output_dir: str = "output"):
    os.makedirs(output_dir, exist_ok=True)
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = r"====== КОНЕЦ (\d+)\.html ======"
    matches = list(re.finditer(pattern, content))
    prev_pos = 0
    for match in matches:
        file_number = match.group(1)
        end_pos = match.start()
        block_text = content[prev_pos:end_pos]
        parsed = process_block(block_text)
        if parsed:
            output_path = os.path.join(output_dir, f"{file_number}.json")
            with open(output_path, "w", encoding="utf-8") as out:
                json.dump({"treatment": parsed}, out, ensure_ascii=False, indent=2)
                print(f"[+] Успешно записаны данные для файла {file_number}.json")
        prev_pos = match.end()

if __name__ == "__main__":
    process_file("parser_with_no_hourly_assignment_sheet/medicine_with_date.txt", output_dir="end")
