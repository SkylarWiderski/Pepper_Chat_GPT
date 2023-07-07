from lwe import ApiBackend
from livewhisper import StreamHandler
import os
bot = ApiBackend()
handler = StreamHandler()
import paramiko

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

#get the question in text 
def get_question():
	try:
		question = handler.listen()
	except (KeyboardInterrupt, SystemExit): pass
	finally:
		print("\n\033[93mLoading response...\033[0m")
		if os.path.exists('dictate.wav'): os.remove('dictate.wav')

	# import whisper
	# model = whisper.load_model("base")
	# result = model.transcribe("sound-question.mp3 or .wav")
	
	# with open("transcription.txt", "w") as file:
	# 	question = file.write(result["text"])
	#return "What is the capital of france?"
	return question 
	
#send the question to chat gpt and get the answer
def ask_question(question):
	success, response, message = bot.ask(question)
	if success:
		print(response)
	else:
		print("No response")
		raise RuntimeError(message)
	return response

#send answer to pepeper
def output_response(response):
	print("\n\033[93mSending to Pepper..\033[0m")
	put_file("192.168.0.110", "nao", "cogvis", "/home/nao/", "stuff.txt", response)
	#with open("stuff.txt", "w") as file:
	#	file.write(response)
	print("\n\033[93mResponse Sent..\033[0m")




old_response = "hi"

try:
	while True:
		question = get_question() #always get question in text
		response = ask_question(question) #store chat gpts answer
		if response != old_response:
			old_response = response
			output_response(response) #send response
except (KeyboardInterrupt, SystemExit): pass
finally:
	print("\n\033[93mQuitting...\033[0m")
	if os.path.exists('dictate.wav'): os.remove('dictate.wav')
	output_response("Goodbye")