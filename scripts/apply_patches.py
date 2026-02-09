
import re

def apply_patches():
    # Read patches
    patches = {}
    current_lang = None
    buffer = []
    
    with open('missing_patches.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('=== ') and not line.startswith('=== END '):
                current_lang = line.split(' ')[1]
                buffer = []
            elif line.startswith('=== END '):
                if current_lang:
                    patches[current_lang] = buffer
                    current_lang = None
            else:
                if current_lang:
                    buffer.append(line)

    # Read translations.py
    with open('translations.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Identify blocks
    # We look for "    'lang': {" to start tracking
    # We look for "    }," to end tracking
    
    output_lines = []
    lang_order = ['en', 'hi', 'es', 'zh', 'ar', 'fr', 'ja', 'te']
    current_block_index = -1
    inside_block = False
    
    # Regex for start of block: standard indentation
    block_start_re = re.compile(r"^\s+'([a-z]{2})': \{")
    block_end_re = re.compile(r"^\s+\},")

    for line in lines:
        match = block_start_re.match(line)
        if match:
            lang = match.group(1)
            # Find index in order
            if lang in lang_order:
                current_block_index = lang_order.index(lang)
                inside_block = True
            else:
                current_block_index = -1 # Unknown or comment
        
        # Check for end of block
        if inside_block and block_end_re.match(line):
            # We are at the closing brace of the current block
            # If we have a patch for this language, insert it
            lang_name = lang_order[current_block_index]
            if lang_name in patches:
                print(f"Applying patch for {lang_name}...")
                for patch_line in patches[lang_name]:
                    output_lines.append(patch_line)
            inside_block = False
            current_block_index = -1
        
        output_lines.append(line)

    with open('translations.py', 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    
    print("Patches applied.")

if __name__ == "__main__":
    apply_patches()
