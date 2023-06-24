from nicegui import ui, app
from src.password_generator_func import generating_random_password
from src import logging_func
from src.retrieve_datetime import current_date_jst
import logging
import os
import asyncio

logger: logging.Logger = logging_func.logging_better_stack(10)  # DEBUG=10


class MainUIElements:
    def __init__(self):
        self.label: ui.label = ui.label('Password Generator')
        self.inp_password_input: ui.input = ui.input('Your generated password:', placeholder="e.g. "
                                                                                             "1a2b3c4d5e6f7g8h9i0j")
        self.btn_generate_password: ui.button = ui.button('Generate Password', on_click=self.generate_password)
        self.password_punctuation_switch: ui.switch = ui.switch('punctuation enabled')
        self.password_length: ui.slider = ui.slider(min=6, max=64, value=16, step=1).props('label-always')
        self.password_note: ui.input = ui.input('Your generated password note:', placeholder="e.g. Facebook",
                                                validation={'Input too short': lambda value: len(value) > 0},
                                                value="My Password")
        self.create_file_button: ui.button = ui.button("Download Password", on_click=self.create_file)
        self.static_path: app = app.add_static_files('/file', 'nicegui_pw_generator/file')

    def generate_password(self):
        self.inp_password_input.value = generating_random_password(
            punctuation_flag=self.password_punctuation_switch.value,
            password_length=self.password_length.value)

        logger.info(f"Password generated: {self.label.text}")

    async def create_file(self):
        today = current_date_jst()
        file_directory = r"nicegui_pw_generator/file/"
        file_name = f"{self.password_note.value}_{today}.txt"
        file_path = f"{file_directory}{file_name}"
        with open(file_path, "w") as f:
            f.write(f"Note: {self.password_note.value}\n")
            f.write(f"Password: {self.inp_password_input.value}\n")
        ui.download(f"/file/{file_name}")
        ui.notify("You have downloaded a text file.", type="positive")

        logger.info(f"File created: {file_name}")
        await asyncio.sleep(0.5)

        if os.path.exists(file_path):
            with open(file_path, 'w'):
                os.remove(file_path)
                logger.info(f"File deleted.")
        else:
            logger.info(f"File not found.")
