import subprocess
import sys
import re
import os

def execute_command(file_name, new_file_name):
    command = f"/home/apps/g16/newzmat -ichk -step 999 {file_name} {new_file_name}"
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Command executed successfully for {file_name}: {result.stdout.decode('utf-8')}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error occurred processing {file_name}: {e.stderr.decode('utf-8')}")
        return False

def add_lines_to_gjf(file_name, new_file_name, keywords):
    oldchk_filename = os.path.basename(file_name)
    newchk_filename = os.path.basename(new_file_name).replace('.gjf', '.chk')

    lines_to_add = [
        f"%oldchk={oldchk_filename}",
        "%nprocshared=128",
        "%mem=50GB",
        f"%chk={newchk_filename}"
    ]

    with open(new_file_name, 'r') as original_file:
        original_content = original_file.read()

    original_lines = original_content.split('\n')
    route_line_index = -1
    for i, line in enumerate(original_lines):
        if line.strip().startswith('#'):
            route_line_index = i
            break

    if route_line_index != -1:
        route_line = original_lines[route_line_index]
        route_parts = route_line.strip().split()
        route_keywords = route_parts[1:]  # Exclude the '#'

        keyword_dict = {}
        for kw in keywords:  # User-provided keywords from command line
            base = kw.split('=')[0] if '=' in kw else kw
            keyword_dict[base] = kw

        new_route_keywords = []
        for kw in route_keywords:
            base = kw.split('=')[0] if '=' in kw else kw
            if base in keyword_dict:
                new_route_keywords.append(keyword_dict.pop(base))
            else:
                new_route_keywords.append(kw)

        new_route_keywords.extend(keyword_dict.values())

        # Always add these two keywords if missing
        required_keywords = {'geom': 'geom=checkpoint', 'guess': 'guess=read'}
        for base, full_kw in required_keywords.items():
            if not any(k.startswith(base + '=') for k in new_route_keywords):
                new_route_keywords.append(full_kw)

        new_route_line = '# ' + ' '.join(new_route_keywords)
        original_lines[route_line_index] = new_route_line

    modified_original_content = '\n'.join(original_lines)

    with open(new_file_name, 'w') as modified_file:
        modified_file.write('\n'.join(lines_to_add) + '\n' + modified_original_content)

def remove_connectivity_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Regex patterns to match atomic coordinates and connectivity lines
    atomic_coord_pattern = re.compile(r'^\s*[A-Z][a-z]?\s+-?\d+\.\d+\s+-?\d+\.\d+\s+-?\d+\.\d+')
    connectivity_pattern = re.compile(r'^\s*\d+\s+\d+(\s+\d+\.\d+)+')

    cleaned_lines = []
    for line in lines:
        # Skip lines matching coordinates or connectivity
        if atomic_coord_pattern.match(line) or connectivity_pattern.match(line):
            continue
        cleaned_lines.append(line)

    # Remove trailing empty lines
    while len(cleaned_lines) > 0 and cleaned_lines[-1].strip() == '':
        cleaned_lines.pop()

    # Add exactly two blank lines at the end
    cleaned_lines.append('\n\n')

    with open(file_path, 'w') as file:
        file.writelines(cleaned_lines)

if __name__ == "__main__":
    # Check for -xx flag first
    use_xx_mode = '-xx' in sys.argv
    args = [arg for arg in sys.argv[1:] if arg != '-xx']

    input_files = []
    keywords = []
    
    # Determine input source (directory/file) and keywords
    if len(args) == 0:
        # Process all .chk files in current directory
        current_dir = os.getcwd()
        input_files = [os.path.join(current_dir, f) for f in os.listdir(current_dir) 
                       if f.endswith('.chk') and os.path.isfile(os.path.join(current_dir, f))]
    else:
        # Check if first argument is a directory/file
        first_arg = args[0]
        if os.path.isdir(first_arg):
            input_files = [os.path.join(first_arg, f) for f in os.listdir(first_arg) 
                           if f.endswith('.chk') and os.path.isfile(os.path.join(first_arg, f))]
            keywords = args[1:]  # Remaining args are keywords
        elif os.path.isfile(first_arg) and first_arg.endswith('.chk'):
            input_files = [first_arg]
            keywords = args[1:]
        else:
            # No valid input source; assume current directory and treat all args as keywords
            current_dir = os.getcwd()
            input_files = [os.path.join(current_dir, f) for f in os.listdir(current_dir) 
                           if f.endswith('.chk') and os.path.isfile(os.path.join(current_dir, f))]
            keywords = args  # Treat all args as keywords
    
    for input_path in input_files:
        filename = os.path.basename(input_path)
        directory = os.path.dirname(input_path)
        
        if use_xx_mode:
            match = re.match(r'^(.*?)_(\d{2})\.chk$', filename)
            if match:
                base_name = match.group(1)
                num = int(match.group(2)) + 1
                new_filename = f"{base_name}_{num:02d}.gjf"
            else:
                base_name = os.path.splitext(filename)[0]
                new_filename = f"{base_name}_01.gjf"
        else:
            match = re.match(r'^(.*)_of(\d+)\.chk$', filename)
            if match:
                base_name = match.group(1)
                num_str = match.group(2)
                num_length = len(num_str)
                new_num = int(num_str) + 1
                new_num_str = f"{new_num:0{num_length}d}"
                new_filename = f"{base_name}_of{new_num_str}.gjf"
            else:
                base_name = os.path.splitext(filename)[0]
                new_filename = f"{base_name}.gjf"
        
        output_path = os.path.join(directory, new_filename)
        
        if not execute_command(input_path, output_path):
            continue
        
        add_lines_to_gjf(input_path, output_path, keywords)
        remove_connectivity_data(output_path)
        print(f"Processed: {filename} → {new_filename}")