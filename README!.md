# SeniorProject
Senior Project Files
Hi everyone, these are the files I used in the creation of my project. I chose to do a more time-lapse style of video instead of just a powerpoint to add creativity
to my overall project. I would have liked to slow it down more and to talk more about the project, but my designated time frame came faster then I anticipated. 
Once again, the headshots_picam.py file is basically the first step. Here you run it and hit the "Spacebar" 
to take photos of yourself at various angles/lighting etc. I chose to do 15 shots of myself for reference. You save these files to a folder with called "yourname". I didn't include
it in here since it only contains photos of myself, and no code.
The second step is to run the train_model.py file in a command prompt, which will then take the headshots taken earlier, and encode them into readable text. The data is then dumped
into the "encodings.pickle" file. Pickling is basically the use of converting of an object in Python into a character stream to be used in other files.
The last file to use is the face_lock.py file. This file is used to pull the encodings.pickle file, and using the "haarcascade_frontalface_default.xml",
will then detect faces preregistered. This file will also then use the GPIO outputs on the Raspberry Pi to send signals to the circuit I created, therefore locking/unlocking
the doorlock. I used a wide variety websites and code listings found online to create my project. I used OpenCV as the biggest contributer for the facial recognition, and imutils
for the majority of the image processing.
