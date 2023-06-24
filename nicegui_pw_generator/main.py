from nicegui import ui, app
from src import ui_elements


@ui.page('/')
async def main_content():
    main = ui_elements.MainUIElements()



ui.run()
