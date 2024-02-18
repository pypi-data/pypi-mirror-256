import speech_recognition as sr

def recognizer(lang: str = "en-US") -> str:
    """
    Recognize the speech and return the text
    :param lang: str: The language of the speech
    :return: str: The recognized text or an empty string
    """ 
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say Something: ")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language=lang)
        return text
    except sr.UnknownValueError:
        return ""

if __name__ == "__main__":
    recognizer()