from transformers import BertTokenizer, BertForSequenceClassification
import torch
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Загрузка предобученной модели и токенизатора
model_path = 'RuBioBert_model/rubio_bert_classifier'
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)

# Функция для определения наличия лекарства в тексте
# Возвращает метку класса: 1 - есть лекарство, 0 - нет
# Также логирует информацию об обработке строки
def is_drug_in_text(text):
    try:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        logits = outputs.logits
        prob = torch.softmax(logits, dim=1).detach()
        label = torch.argmax(prob, dim=1).item()
        logging.info(f"Строка обработана: {text[:50]}...")
        return label
    except Exception as e:
        logging.error(f"Ошибка обработки строки '{text}': {e}")
        return 0  # В случае ошибки считаем, что строка не содержит лекарства

# Основная функция поиска строк, содержащих упоминания лекарств
# Принимает путь к входному и выходному файлу
# Выводит обработанные строки в выходной файл, если они содержат лекарства
# Также логирует общее количество строк и число строк с лекарствами
def search_medicine(input_txt, output_file):
    total_lines = 0  # Счетчик всех строк
    drug_lines = 0   # Счетчик строк с лекарствами

    try:
        with open(input_txt, 'r', encoding='utf-8') as file, open(output_file, 'w', encoding='utf-8') as output_txt:
            for line in file:
                stripped = line.strip()
                total_lines += 1

                # Пропуск маркера конца блока
                if stripped.startswith('====== КОНЕЦ'):
                    output_txt.write(line)
                    continue

                # Проверка строки на наличие лекарства
                result = is_drug_in_text(stripped)
                if result == 1:
                    drug_lines += 1
                    output_txt.write(line)

        logging.info(f"Общее количество строк в файле: {total_lines}")
        logging.info(f"Количество строк, содержащих лекарства: {drug_lines}")

    except FileNotFoundError as fnf_error:
        logging.error(f"Файл не найден: {fnf_error}")
    except Exception as e:
        logging.error(f"Ошибка при обработке файлов: {e}")
