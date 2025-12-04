import pdfplumber
import os
import json

# folder containing your PDFs
case_folder = "../legal_docs"
output_file = "legal_data.json"

data = []

for file in os.listdir(case_folder):
    if file.endswith(".pdf") or file.endswith(".PDF"):
        file_path = os.path.join(case_folder, file)

        # extract text
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"

        # save in JSON-friendly format
        entry = {
            "file_name": file,
            "content": text.strip()
        }
        data.append(entry)

print(len(data))


# Save JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Extracted {len(data)} documents into {output_file}")