import subprocess

# Define the command
command = 'yt-dlp --cookies ./cookies.txt https://www.youtube.com/watch?v=4w9iDLuvSOQ -vU'

# Execute the command
try:
    result = subprocess.run(command, shell=True, check=True, text=True)
    print("Command executed successfully!")
    print("Output:", result.stdout)
except subprocess.CalledProcessError as e:
    print(f"Error executing command: {e}")
    print("Error Output:", e.stderr)
