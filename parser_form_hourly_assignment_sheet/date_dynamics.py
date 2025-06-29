import os
import json
import hashlib
from collections import defaultdict

# Функция для создания уникального хеша словаря
# Используется для определения, одинаковы ли записи по содержимому
# Это позволяет отличать препараты с разным составом, но одинаковым названием
def dict_hash(d):
    """Создаёт хеш словаря (чтобы можно было сравнивать по содержимому)."""
    return hashlib.md5(json.dumps(d, sort_keys=True).encode()).hexdigest()

# Функция для извлечения полных записей о применении лекарств с указанием интервалов дней
# Группирует дни с одинаковыми параметрами препарата (по хешу словаря) и объединяет их в периоды
# Поддерживает препараты с несколькими названиями (через запятую)
def extract_full_entries_with_periods(treatment):
    med_usage = defaultdict(list)
    
    # Сбор всех вхождений препарата по дням, с учётом хеша содержания
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

        # Группировка по смежным дням
        for day_num, details in day_entries:
            if not current_group or (prev_day is not None and day_num == prev_day + 1):
                current_group.append((day_num, details))
            else:
                # Завершение текущего периода и начало нового
                start = current_group[0][0]
                end = current_group[-1][0]
                entry = current_group[0][1].copy()
                entry["name"] = name
                entry["period"] = f"{start}-{end}"
                result.append(entry)
                current_group = [(day_num, details)]
            prev_day = day_num

        # Добавление последнего периода, если остался
        if current_group:
            start = current_group[0][0]
            end = current_group[-1][0]
            entry = current_group[0][1].copy()
            entry["name"] = name
            entry["period"] = f"{start}-{end}"
            result.append(entry)

    return result

# Основная функция для пакетной обработки всех JSON-файлов в директории
# Извлекает динамику назначения лекарств и сохраняет в выходную папку
# Использует extract_full_entries_with_periods для анализа

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
