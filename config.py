import json

input_file = "C:\\ir\\result_v3_utf8_2500_docs.json"
output_file = "C:\\ir\\barcelona_docs.json"

keywords = ["barcelona", "messi", "camp nou", "xavi", "la masia", "fc barcelona", "catalonia"]

out = open(output_file, "w", encoding="utf-8")

with open(input_file, "r", encoding="utf-8") as f:
    while True:
        id_line = f.readline()
        text_line = f.readline()
        if not text_line:
            break

        try:
            text_obj = json.loads(text_line)
            text = text_obj.get("text", "").lower()

            if any(k in text for k in keywords):
                out.write(id_line)
                out.write(text_line)
        except:
            pass

out.close()

print("Extraction complete!")
