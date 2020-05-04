

def get_lines_of_file(first_line, last_line, filename):
    target_file_lines = open(filename, "r").readlines()
    return target_file_lines[first_line:last_line]
