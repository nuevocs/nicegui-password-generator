from dotenv import load_dotenv
import os

load_dotenv()

BETTERSTACK_TOKEN: str = os.environ["BETTERSTACK_TOKEN"]

MONGODB_HOST: str = os.environ["MONGODB_HOST"]
MONGODB_PORT: int = int(os.environ["MONGODB_PORT"])

HOW_TO_USE: str = """
#### How to use

- Tap the "GENERATE A PASSWORD" button to generate a random password.
- The generated password can be altered as you like from the input.
- Optionally, you can enable the "punctuation enabled" switch to include punctuation in the password.
- You can also change the length of the password by moving the slider.
- You can add a note of the password by changing the text in the "Your note:" input.
- Tap the "DOWNLOAD THE PASSWORD FILE" button to download a text file containing the password and the note.

"""