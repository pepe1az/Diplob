from transformers import BertTokenizer, BertForSequenceClassification
import torch
model_path = 'RuBioBert_model/rubio_bert_classifier'
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)

def is_drug_in_text(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    prob = torch.softmax(logits, dim=1).detach()
    label = torch.argmax(prob, dim=1).item()
    print(f"строка {text} обработана")
    return label

def search_medicine(input_txt, output_file):
    with open(input_txt, 'r', encoding='utf-8') as file:
        total_lines = 0
        drug_lines = 0
        with open(output_file, 'w', encoding='utf-8') as output_txt:
            for line in file:
                stripped = line.strip()
                total_lines += 1

                if stripped.startswith('====== КОНЕЦ'):
                    output_txt.write(line)
                    continue

                result = is_drug_in_text(stripped)
                if result == 1:
                    drug_lines += 1
                    output_txt.write(line)

    print(f"Общее количество строк в файле: {total_lines}")
    print(f"Количество строк, содержащих лекарства: {drug_lines}")