from gtts import gTTS
text =input("Enter the text you want to convert to speech: ")   

# Create a gTTS object  
tts = gTTS(text=text, lang='en')
# Save the audio file   
tts.save("output.mp3")
print("Audio file saved as output.mp3")
