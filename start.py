
import subprocess

command = ['python', './stabe_bot.py']

print("Starting the bot")
while True:
    try:
        result = subprocess.run(command, shell=True, check=True, text=True)
        print(result.stderr)
    except Exception as e:
        print(e)