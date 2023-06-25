from nicegui import ui, app
from src.password_generator_func import generating_random_password
from src import logging_func
from src.retrieve_datetime import current_date_jst
from src import mongodb_func
import logging
import os
import asyncio
from src.constants import HOW_TO_USE, MONGODB_HOST, MONGODB_PORT

logger: logging.Logger = logging_func.logging_better_stack(10)  # DEBUG=10
logger_mongodb: logging.Logger = logging_func.logging_mongodb(20, host=MONGODB_HOST,
                                                              port=MONGODB_PORT,
                                                              database="logs",
                                                              collection="nicegui_pw_generator"
                                                              )  # DEBUG=10


class MainUIElements:
    def __init__(self):
        with ui.header(elevated=False).style('background-color: #333333').classes('items-center justify-between'):
            ui.label("PASSWORD GENERATOR").classes("text-xl text-center")
        with ui.card().props('autofocus item-aligned input-class="ml-3"').classes('w-10/12 mt-40 self-center '
                                                                                  'transition-all'):
            with ui.column().classes('w-full self-center transition-all'):
                with ui.tabs().classes('w-full') as tabs:
                    function = ui.tab('PASSWORD GENERATOR')
                    description = ui.tab('HOW TO USE')
                with ui.tab_panels(tabs, value=function).classes('w-full'):
                    with ui.tab_panel(function):
                        with ui.column().classes('w-full self-center transition-all'):
                            self.inp_password_input: ui.input = ui.input('Your generated password:', placeholder="e.g. "
                                                                                                                 "1a2b3c4d5e6f7g8h9i0j") \
                                .classes('w-10/12')
                            self.btn_generate_password: ui.button = ui.button('Generate a Password',
                                                                              on_click=self.generate_password,
                                                                              icon="autorenew")
                            self.password_punctuation_switch: ui.switch = ui.switch('Punctuation Disabled',
                                                                                    value=False,
                                                                                    on_change=self.punctuation_switch).classes(
                                'mb-5')
                            self.password_length: ui.slider = ui.slider(min=6, max=64, value=16, step=1).props(
                                'label-always') \
                                .classes('w-10/12')
                            self.password_note: ui.input = ui.input('Your note:', placeholder="e.g. Facebook",
                                                                    validation={
                                                                        'Input too short': lambda value: len(
                                                                            value) > 0},
                                                                    value="My Password").classes('w-10/12')
                            self.create_file_button: ui.button = ui.button("Download the Password file",
                                                                           on_click=self.create_file,
                                                                           color="secondary", icon="download")
                            self.static_path: app = app.add_static_files('/file', 'nicegui_pw_generator/file')
                    with ui.tab_panel(description):
                        with ui.column().classes('w-full self-center transition-all'):
                            # self.lbl_app_title: ui.label = ui.label('Password Generator').classes("text-xl self-center")
                            self.app_explanation: ui.markdown = ui.markdown(HOW_TO_USE)

    def punctuation_switch(self):
        if self.password_punctuation_switch.value is True:
            self.password_punctuation_switch.text = "Punctuation Enabled"
        else:
            self.password_punctuation_switch.text = "Punctuation Disabled"

    def generate_password(self):
        self.inp_password_input.value = generating_random_password(
            punctuation_flag=self.password_punctuation_switch.value,
            password_length=self.password_length.value)

        logger_mongodb.info(f"Password generated: {self.inp_password_input.value}")

    async def create_file(self):
        today = current_date_jst()
        file_directory = r"nicegui_pw_generator/file/"
        file_name = f"{self.password_note.value}_{today}.txt"
        file_path = f"{file_directory}{file_name}"
        with open(file_path, "w") as f:
            f.write(f"Note: {self.password_note.value}\n")
            f.write(f"Password: {self.inp_password_input.value}\n")
            f.write(f"Password Length: {self.password_length.value}\n")
            f.write(f"Punctuation Flag: {self.password_punctuation_switch.value}\n")
            f.write(f"Published Date: {today}\n")
        ui.download(f"/file/{file_name}")
        ui.notify("You have downloaded a text file.", type="positive")

        logger_mongodb.info(f"File created: {file_name}")

        await asyncio.sleep(0.5)

        if os.path.exists(file_path):
            with open(file_path, 'w'):
                os.remove(file_path)
                logger.info(f"File deleted.")
        else:
            logger.info(f"File not found.")
