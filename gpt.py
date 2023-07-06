from lwe import ApiBackend
from livewhisper import StreamHandler
import os
bot = ApiBackend()
handler = StreamHandler()
import paramiko
pepper_address = "192.168.0.110"
pepper_username = "nao"
pepper_password = "nao"

def put_file(machinename, username, password, dirname, filename, data):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(machinename, username=username, password=password)
    sftp = ssh.open_sftp()
    try:
        sftp.mkdir(dirname)
    except IOError:
        pass
    f = sftp.open(dirname + '/' + filename, 'w')
    f.write(data)
    f.close()
    ssh.close()


def get_question():
	try:
		question = handler.listen()
	except (KeyboardInterrupt, SystemExit): pass
	finally:
		print("\n\033[93mQuitting..\033[0m")
		if os.path.exists('dictate.wav'): os.remove('dictate.wav')

	# import whisper
	# model = whisper.load_model("base")
	# result = model.transcribe("sound-question.mp3 or .wav")
	
	# with open("transcription.txt", "w") as file:
	# 	question = file.write(result["text"])
	#return "What is the capital of france?"
	return question 
	

def ask_question(question):
	success, response, message = bot.ask(question)
	if success:
		print(response)
	else:
		print("No response")
		raise RuntimeError(message)
	return response


def output_response(response):
	#response = "test"
	print("Sending to pepper")
	put_file(pepper_address, pepper_username, pepper_password, "/home/nao/", "stuff.txt", response)
	#with open("stuff.txt", "w") as file:
	#	file.write(response)
	print("Response sent")




#output_response("test")

try:
	while True:
		question = get_question()
		response = ask_question(question)
		output_response(response)
except (KeyboardInterrupt, SystemExit): pass
finally:
	print("\n\033[93mAsking ChatGPT...\033[0m")
	if os.path.exists('dictate.wav'): os.remove('dictate.wav')
