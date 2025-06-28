import re

# Функция для извлечения концентрации, способа введения и общей дозы из строки текста
def parse_medication_with_pattern(text):
    # Шаблон для поиска концентрации (например, 500 ЕД/мл или 0.25 мг/мл)
    concentration_pattern = r"(\d+\.?\d*|\d+\s*тыс\.?)\s*(ЕД|МЕ|мг)/мл"

    # Шаблон для распознавания способа введения препарата
    method_pattern = r"(в/в(?: капельно| болюсно)?|п/к|внутрь|на кожу|энтерально|через зонд|промыв катетера|в/м(?: глубоко)?|гемодиализ)"

    # Шаблон для извлечения общей дозы (например, 10 мг, 10000 ЕД и т.д.)
    total_dose_pattern = r"(\d+(?:[.,]\d+)?)\s*(ед|МЕ|ЕД|МГ|Мг|МЛ|Мл|Ед|мг|мл|дозсмеси)"

    # Поиск совпадений в тексте
    concentration_match = re.search(concentration_pattern, text, re.IGNORECASE)
    method_match = re.search(method_pattern, text, re.IGNORECASE)
    total_dose_matches = re.findall(total_dose_pattern, text, re.IGNORECASE)

    # Обработка концентрации, если найдена
    if concentration_match:
        raw_value = concentration_match.group(1).replace(',', '.').replace(' ', '')
        # Обработка случая с «тыс.» (например, «2 тыс.» → 2000)
        if "тыс" in raw_value:
            numeric_value = float(re.search(r"\d+", raw_value).group()) * 1000
        else:
            numeric_value = float(raw_value)

        concentration_value = numeric_value
        concentration_unit = concentration_match.group(2).upper()
    else:
        return None  # Если концентрация не найдена — ничего не возвращаем

    # Извлечение способа введения, если найден, иначе пометка «не указан»
    method = method_match.group(1) if method_match else "не указан"

    # Извлечение общей дозы: берётся последняя найденная пара (число + единица)
    if total_dose_matches:
        total_dose_value = float(total_dose_matches[-1][0].replace(',', '.'))
        total_dose_unit = total_dose_matches[-1][1]
        total = f"{total_dose_value} {total_dose_unit}"
    else:
        total = "не указано"

    # Формирование итогового результата в виде словаря
    return {
        "concentration": f"{concentration_value:.0f} {concentration_unit}/мл",
        "route": method,
        "total": total
    }
