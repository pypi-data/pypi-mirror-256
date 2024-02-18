import os
import subprocess
import json
from tkinter import COMMAND

from commands.const import COMMANDS, DATA_FILE, ID


def run_command(cmd_id: int, shell: bool = True, check: bool = True):

    if not os.path.isfile(DATA_FILE):
        raise ValueError(
            "Decrypted file does not exist. Run: 'commands -d -k the_key_to_decrypt'"
        )

    with open(DATA_FILE, "r") as f:
        data = json.load(f)
        commands = data[COMMANDS]

        found_command = None
        for cmd in commands:
            if cmd[ID] == cmd_id:
                found_command = cmd
                break

        if not found_command:
            raise ValueError(f"Command with ID: {cmd_id} was not found.")

        command_output = subprocess.run(cmd[COMMAND].split(" "), shell=shell, check=check)
        print(command_output)
