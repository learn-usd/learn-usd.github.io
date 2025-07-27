import re

def extract_titles_and_code(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    pattern_title = re.compile(r'^(#{1,3})\s+11.*')
    inside_code_block = False
    output = []
    code_block = []

    for line in lines:
        # Check for start or end of a python code block
        if line.strip().startswith("```python") and not inside_code_block:
            inside_code_block = True
            code_block = [line]
            continue
        elif line.strip() == "```" and inside_code_block:
            code_block.append(line)
            output.append(''.join(code_block))
            inside_code_block = False
            continue

        if inside_code_block:
            code_block.append(line)
            continue

        # Check for matching titles
        match = pattern_title.match(line)
        if match:
            output.append(line)

    return output

# Example usage
if __name__ == "__main__":
    chapter_number = 11
    filepath = f"./{chapter_number}.md"  # replace with your actual file
    extracted = extract_titles_and_code(filepath) # Hardcoded chapter number????????????
    
    with open(f"extracted_{chapter_number}_titles_and_code.md", "w", encoding="utf-8") as out_file:
        out_file.writelines(extracted)
