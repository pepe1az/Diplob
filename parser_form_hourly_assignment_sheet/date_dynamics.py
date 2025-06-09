import os
import json
import hashlib
from collections import defaultdict

#INPUT_DIR = "end"
#OUTPUT_DIR = "date_dynamics"

def dict_hash(d):
    """Создаёт хеш словаря (чтобы можно было сравнивать по содержимому)."""
    return hashlib.md5(json.dumps(d, sort_keys=True).encode()).hexdigest()

def extract_full_entries_with_periods(treatment):
    med_usage = defaultdict(list)

    for day_key in sorted(treatment.keys(), key=lambda d: int(d.split('_')[-1])):
        day_num = int(day_key.split('_')[-1])
        for combined_name, details in treatment[day_key].items():
            names = [name.strip() for name in combined_name.split(',')]
            for name in names:
                h = dict_hash(details)
                med_usage[(name, h)].append((day_num, details))

    result = []
    for (name, h), day_entries in med_usage.items():
        day_entries.sort()
        current_group = []
        prev_day = None
        for day_num, details in day_entries:
            if not current_group or (prev_day is not None and day_num == prev_day + 1):
                current_group.append((day_num, details))
            else:
                start = current_group[0][0]
                end = current_group[-1][0]
                entry = current_group[0][1].copy()
                entry["name"] = name
                entry["period"] = f"{start}-{end}"
                result.append(entry)
                current_group = [(day_num, details)]
            prev_day = day_num
        if current_group:
            start = current_group[0][0]
            end = current_group[-1][0]
            entry = current_group[0][1].copy()
            entry["name"] = name
            entry["period"] = f"{start}-{end}"
            result.append(entry)

    return result

"""for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".json"):
        filepath = os.path.join(INPUT_DIR, filename)
        with open(filepath, encoding="utf-8") as f:
            try:
                data = json.load(f)
                treatment = data.get("treatment", {})
                result = extract_full_entries_with_periods(treatment)
                output_path = os.path.join(OUTPUT_DIR, filename)
                with open(output_path, "w", encoding="utf-8") as out:
                    json.dump(result, out, ensure_ascii=False, indent=2)
                print(f"Обработан: {filename}")
            except Exception as e:
                print(f"Ошибка при обработке {filename}: {e}")"""

def process_date_dynamics(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(input_dir, filename)
            with open(filepath, encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    treatment = data.get("treatment", {})
                    result = extract_full_entries_with_periods(treatment)
                    output_path = os.path.join(output_dir, filename)
                    with open(output_path, "w", encoding="utf-8") as out:
                        json.dump(result, out, ensure_ascii=False, indent=2)
                    print(f"Обработан: {filename}")
                except Exception as e:
                    print(f"Ошибка при обработке {filename}: {e}")

