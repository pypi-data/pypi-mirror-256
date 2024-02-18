import os
import subprocess
from rich.table import Table

def create_table(data_dict) -> Table:
    table = Table()

    # Adicionando cabeçalhos
    for header in data_dict.keys():
        table.add_column(header)

    # Encontrando o número de linhas (baseado no item mais longo)
    num_rows = max(len(values) for values in data_dict.values())

    # Adicionando linhas
    for i in range(num_rows):
        row = [
            f"{"[green]:heavy_check_mark:" if data_dict[key][i] == "Ok" else f"[red]{data_dict[key][i]}"}" if key == "status" else f"[bold blink dark_green]{data_dict[key][i]}" if i < len(data_dict[key]) else "" for key in data_dict
        ]
        table.add_row(*row)

    return table

def run_command(command, path=os.getcwd()):
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            cwd=path,
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error:")
        print(e.stderr)
