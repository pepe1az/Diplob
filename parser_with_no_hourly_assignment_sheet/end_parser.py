import re
import json
import os

def clean_line(line, extracted_parts):
    """
    Удаляет все извлечённые фрагменты из строки, чтобы получить comment.
    """
    for part in extracted_parts:
        if part:
            # Удаляем только первое вхождение каждого фрагмента
            line = re.sub(re.escape(part), '', line, count=1)
    return re.sub(r'\s+', ' ', line).strip(" .,:;–—\n\t")

def parse_medicine_line(line):
    """
    Преобразует строку с лекарством в структуру словаря и добавляет всё необработанное в comment.
    """
    original_line = line.strip()
    extracted_parts = []

    # Извлекаем даты
    date_pattern = r"\d{2}\.\d{2}\.\d{4}"
    dates = re.findall(date_pattern, line)
    if len(dates) >= 2:
        date_start, date_end = dates[-2], dates[-1]
        extracted_parts += [date_start, date_end]
    else:
        date_start = date_end = ""

    # Название (всё до первого числа или дозировки)
    parts = original_line.split()
    name_parts = []
    for part in parts:
        if re.search(r"\d", part) or "мг" in part or "мл" in part or "ЕД" in part:
            break
        name_parts.append(part)
    name = " ".join(name_parts).strip()
    extracted_parts.append(name)

    route_match = re.search(
        r"(в/в(?: капельно| болюсно)?|п/к|инфузомат|внутрь|ингаляционно|наружно|в глаза|перевязка|энтерально|местно|Местно|изотонический гемодиализ|ТБД|внутриплеврально|эпидурально|на кожу|внутрипузырно|парентерально|через зонд|промыв катетера|в/м(?: глубоко)?)",
        original_line,
        flags=re.IGNORECASE
    )
    route = route_match.group(1) if route_match else ""
    if route:
        extracted_parts.append(route)
    dosage_match = re.search(r"(\d+\.?\d*)\s*(мг|мл|ЕД)", original_line)
    dosage = f"{dosage_match.group(1)} {dosage_match.group(2)}" if dosage_match else ""
    if dosage:
        extracted_parts.append(dosage_match.group(0))  
    comment = clean_line(original_line, extracted_parts)

    return {
        name: {
            "route": route,
            "dosage": dosage,
            "date_start": date_start,
            "date_end": date_end,
            "comment": comment
        }
    }

def split_groups_by_separator(content):
    pattern = r"====== КОНЕЦ (.*?) ======"
    matches = list(re.finditer(pattern, content))

    groups = []
    start = 0
    for match in matches:
        end = match.start()
        file_name = match.group(1).strip()
        group_text = content[start:end].strip()
        groups.append((file_name, group_text))
        start = match.end()
    return groups

def process_group(group_text):
    lines = group_text.strip().splitlines()
    treatment_dict = {}

    for line in lines:
        line = line.strip()
        if not line or not re.search(r"\d{2}\.\d{2}\.\d{4}", line):
            continue
        parsed = parse_medicine_line(line)
        treatment_dict.update(parsed)

    if treatment_dict:
        return {"treatment": treatment_dict}
    return None

def main(input_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    groups = split_groups_by_separator(content)
    print(f"Найдено групп: {len(groups)}")

    for file_name, group_text in groups:
        parsed_group = process_group(group_text)
        if parsed_group:
            json_path = os.path.join(output_dir, file_name.replace(".html", ".json"))
            with open(json_path, "w", encoding="utf-8") as out_f:
                json.dump(parsed_group, out_f, ensure_ascii=False, indent=2)
            print(f"Сохранено: {json_path} ({len(parsed_group['treatment'])} записей)")

if __name__ == "__main__":
    main("new_parser/end/drugs_with_date.txt")
