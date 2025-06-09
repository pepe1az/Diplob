import re

date_pattern = re.compile(r'\d{2}\.\d{2}\.\d{4}\s+\d{2}\.\d{2}\.\d{4}$')

#input_file = 'new_parser/end/drug_detection_results.txt'
#output_file = 'new_parser/end/drugs_with_date.txt'
def sort_by_date(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
        open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            stripped = line.strip()
            if stripped.startswith("====== КОНЕЦ"):
                outfile.write(line)
                continue
            if date_pattern.search(stripped):
                outfile.write(line)
