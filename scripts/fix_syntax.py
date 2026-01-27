
import re

def fix_commas():
    with open('translations.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    # Regex to match lines like: "        'key': 'value'" or "        'key': "value"" that DON'T end with comma
    # We assume values are strings.
    # Be careful with comments or multi-line strings (though none seem present).
    # We target lines indented with 8 spaces.
    
    pattern = re.compile(r"^(\s{8}'[^']+'\s*:\s*(?:'[^']*'|\"[^\"]*\"))\s*$")
    
    for line in lines:
        line_stripped = line.rstrip()
        match = pattern.match(line_stripped)
        if match:
             # It matches a key-value pair without a trailing comma
             # We append a comma
             fixed_lines.append(line_stripped + ",\n")
        else:
             fixed_lines.append(line)
             
    with open('translations.py', 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
        
    print("Fixed missing commas.")

if __name__ == "__main__":
    fix_commas()
