#import libraries

import moviepy.editor as mpe
import whisper
import os

#Function to name new transcript file

def append_file(filename):
    """
    Add "_transcript.txt" to your new file name.

    This function takes the name of the video file that you are looking to transcribe and will append the
    file name with "_transcript.txt" in order to name the file for saving in the destination folder you select.

    Parameters
    ----------
    filename : file path
        Your file's location.

    Returns
    -------
    file_transcript.txt : file name
        The transcribed file name.
    """
    parts = filename.split('.')
    return "".join(parts[:-1])+ '_transcript.txt'



#Function to iterate over files and transcribe them

def video_to_txt(path, test_type, dest_folder):
    """
    Extracts video files from folder, extracts audio from video files, transcribes audio, and saves to designated
    folder.

    Pulls video files from given in first argument, extracts audio from the video files specified in second function
    argument by test type (Grandfather, Picnic, etc), transcribes the audio files, and then uses the append_file
    function to write a new file name for the transcript before saving to destination
    folder specified in third function argument.

    Parameters
    ----------
    path : file path
        Your file's location.

    test_type : str
        The type of test you wish to transcribe. The video can be called by the test name written in the file name.
        For example: Any files that recorded the Grandfather reading, will have '_Grandfather' and so can be called
        when you give that specific string to specify your test type. To call all videos, simply write 'mp4' or your
        chosen video file extension type.

    dest_folder : file path
        The path of the destination folder where you wish to save the transcriptions.

    Returns
    -------
    .txt file
        The transcribed file name.
    """

    #call the transcription model
    model = whisper.load_model('base')

    #iterate over files in sub-directory
    for root, dirs, files in os.walk(path):
        for file in files:
            fullPath = os.path.join(root, file)
            print(fullPath)

            #check if filename contains the string to match/type of test
            if test_type in file:
                print('Processing...')

                #write file to video var
                video = mpe.VideoFileClip(fullPath)

                #extract the audio
                video.audio.write_audiofile(r"transcript_audio.wav")

                #transcribe the audio
                result = model.transcribe(r"transcript_audio.wav", fp16=False)
                text = result["text"]

                #save to new folder
                outputPath = os.path.join(dest_folder, append_file(file))
                print(f'Saving output to {outputPath}')

                with open(outputPath, mode = 'w', encoding="utf-8") as file:
                    file.write("\n")
                    file.write(text)
                    print('File Saved')

