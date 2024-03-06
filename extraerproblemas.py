import re

def bloque_postulante(file_path):
    postulantes = {}
    line_number = 0
    pattern = "# Postulante: "

    with open(file_path, 'r', encoding='utf-8-sig') as file:
        for line in file:
            match = re.search(pattern, line)
            line_number += 1
            if match:
                start_index = match.end()
                if postulantes:  # If postulantes dictionary is not empty
                    # Update the end point of the previous postulante
                    last_postulante = next(reversed(postulantes))
                    postulantes[last_postulante] = (postulantes[last_postulante][0], line_number - 1)
                postulante_num = line[start_index:start_index + 7]
                # Add the current postulante with its starting point
                postulantes[postulante_num] = (line_number, None)

    # Update the end point of the last postulante
    if postulantes:
        last_postulante = next(reversed(postulantes))
        postulantes[last_postulante] = (postulantes[last_postulante][0], line_number)

    return postulantes

def errores_por_postulantes(postulantes, file_path, output_file):
    postulantes_err_lines = {}

    with open(file_path, 'r', encoding='utf-8-sig') as file:
        for postulante, (start_line, end_line) in postulantes.items():
            err_lines = []
            # Seek to the beginning of the file
            file.seek(0)
            # Skip lines until reaching the starting line of the current postulante
            for _ in range(start_line - 1):
                next(file)
            # Read lines until reaching the ending line of the current postulante
            for line_number, line in enumerate(file, start=start_line):
                if line_number > end_line:
                    break
                match_err = re.search("ERR", line)
                if match_err:
                    err_lines.append(line.strip())
            postulantes_err_lines[postulante] = err_lines

    with open(output_file, 'w', encoding='utf-8') as output:
        for postulante, err_lines in postulantes_err_lines.items():
            output.write(f"Postulante: {postulante}\n")
            for line in err_lines:
                output.write(f"{line}\n")
            output.write("\n")

    return postulantes_err_lines

# Example usage:
file_path = "Consistencia"
postulantes = bloque_postulante(file_path)
output_file = "errores_por_postulantes.txt"
err_lines_by_postulante = errores_por_postulantes(postulantes, file_path, output_file)

for postulante, err_lines in err_lines_by_postulante.items():
    print("Postulante:", postulante)
    print("Error lines:", err_lines)
    print()
