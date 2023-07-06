# Pepper_Chat_GPT
A repo that allows users to ask questions to Pepper, which are interpretted by Whisper, answered by ChatGPT, and the reply is spoken by Pepper

# Set up
Download the repository and install the python dependencies (whisper, chatgpt, sounddevice, Paramiko).

Note that to set up ChatGPT you must export your API key.

Edit gpt.py to add the IP address, username and password of your Pepper robot.

# Usage
Run the included choregraphe project on your pepper robot.

Next execute the gpt.py script in the terminal.

Once the whisper model has downloaded, wait for the "listening..." message then ask your question followed by silence.

Note that if you use a free API key, you will be limited to three questions per minute.


