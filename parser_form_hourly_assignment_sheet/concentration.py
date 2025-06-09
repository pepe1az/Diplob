import re

def parse_medication_with_pattern(text):
    concentration_pattern = r"(\d+\.?\d*|\d+\s*тыс\.?)\s*(ЕД|МЕ|мг)/мл"
    method_pattern = r"(в/в(?: капельно| болюсно)?|п/к|внутрь|на кожу|энтерально|через зонд|промыв катетера|в/м(?: глубоко)?|гемодиализ)"
    total_dose_pattern = r"(\d+(?:[.,]\d+)?)\s*(ед|МЕ|ЕД|МГ|Мг|МЛ|Мл|Ед|мг|мл|дозсмеси)"
    
    concentration_match = re.search(concentration_pattern, text, re.IGNORECASE)
    method_match = re.search(method_pattern, text, re.IGNORECASE)
    total_dose_matches = re.findall(total_dose_pattern, text, re.IGNORECASE)

    if concentration_match:
        raw_value = concentration_match.group(1).replace(',', '.').replace(' ', '')
        if "тыс" in raw_value:
            numeric_value = float(re.search(r"\d+", raw_value).group()) * 1000
        else:
            numeric_value = float(raw_value)

        concentration_value = numeric_value
        concentration_unit = concentration_match.group(2).upper()
    else:
        return None

    method = method_match.group(1) if method_match else "не указан"

    if total_dose_matches:
        total_dose_value = float(total_dose_matches[-1][0].replace(',', '.'))
        total_dose_unit = total_dose_matches[-1][1]
        total = f"{total_dose_value} {total_dose_unit}"
    else:
        total = "не указано"

    return {
        "concentration": f"{concentration_value:.0f} {concentration_unit}/мл",
        "route": method,
        "total": total
    }
