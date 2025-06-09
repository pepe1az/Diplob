import os
import json
from collections import defaultdict
from datetime import datetime, timedelta
import hashlib


def dict_hash_ignore_comment(d):
    # создаём копию без ключа 'comment'
    filtered = {k: v for k, v in d.items() if k != "comment"}
    # сериализуем и хешируем для уникальности
    return hashlib.md5(json.dumps(filtered, sort_keys=True).encode()).hexdigest()

def extract_date_groups(treatment):
    groups = defaultdict(list)

    all_dates = []

    for name, info in treatment.items():
        if not all(k in info for k in ("date_start", "date_end")):
            continue
        try:
            start = datetime.strptime(info["date_start"], "%d.%m.%Y")
            end = datetime.strptime(info["date_end"], "%d.%m.%Y")
        except ValueError:
            continue
        all_dates.append(start)
        all_dates.append(end)
        h = dict_hash_ignore_comment(info)
        groups[(name, h)].append((start, end, info))

    if not all_dates:
        return []

    min_date = min(all_dates)

    result = []
    for (name, h), entries in groups.items():
        entries.sort()
        current_group = []
        prev_end = None
        for start, end, info in entries:
            if not current_group or (prev_end and start == prev_end + timedelta(days=1)):
                current_group.append((start, end, info))
            else:
                start_g = current_group[0][0]
                end_g = current_group[-1][1]
                data = current_group[0][2].copy()
                data["name"] = name
                period_start = (start_g - min_date).days + 1
                period_end = (end_g - min_date).days + 1
                data["period"] = f"{period_start}-{period_end}"
                data.pop("date_start", None)
                data.pop("date_end", None)
                result.append(data)
                current_group = [(start, end, info)]
            prev_end = end
        if current_group:
            start_g = current_group[0][0]
            end_g = current_group[-1][1]
            data = current_group[0][2].copy()
            data["name"] = name
            period_start = (start_g - min_date).days + 1
            period_end = (end_g - min_date).days + 1
            data["period"] = f"{period_start}-{period_end}"
            data.pop("date_start", None)
            data.pop("date_end", None)
            result.append(data)

    def parse_period_start(period):
        try:
            return int(period.split("-")[0])
        except Exception:
            return 999999

    result.sort(key=lambda x: parse_period_start(x["period"]))
    return result
def process_date_dynamics(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(input_dir, filename)
            with open(filepath, encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    treatment = data.get("treatment", {})
                    result = extract_date_groups(treatment)
                    output_path = os.path.join(output_dir, filename)
                    with open(output_path, "w", encoding="utf-8") as out:
                        json.dump(result, out, ensure_ascii=False, indent=2)
                    print(f"Обработан: {filename}")
                except Exception as e:
                    print(f"Ошибка при обработке {filename}: {e}")
