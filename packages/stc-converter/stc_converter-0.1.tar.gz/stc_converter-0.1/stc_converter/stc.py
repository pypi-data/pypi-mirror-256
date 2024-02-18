from listenner import recognizer
import time
from unicodedata import normalize
from difflib import SequenceMatcher
import nltk
nltk.download('punkt')
nltk.download('stopwords')

class STC:
    """
    Speech to Command class

    This class is responsible for listening to the microphone and execute the commands

    :param start_word: str: The word that triggers the listenner
    :param lang: str: The language of the speech
    :param context_definer: str: The word that defines the context of the command
    """
    def __init__(self,start_command:str, context_definer: str = "using context", lang: str = "en-US", ):
        self.start_command = start_command.lower()
        self.lang = lang
        self.verbose_langs = {"en-US":"english", "pt-BR":"portuguese"}
        self.commands = []
        self.context_definer = context_definer

    def add_command(self, function: callable,commands: list,context:str="",) -> None:
        """
        Add a command to the list of commands
        :param context: str: The context of the function. It is the class where the function is defined
        :param function: callable: The function to be called
        :param commands: list: The list of commands that trigger the function
        :return: None
        """
        for command in commands:
            self.commands.append({"context":context,"command":command, "function":function,})

    def clean_text(self,text:str) -> str:
        """
        Remove the start command from the text
        :param text: str: The text to be cleaned
        :return: str: The cleaned text
        """
        text = text.lower().strip()
        # text = re.sub("[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]", "", text)
        # text = normalize("NFKD", text).encode("ASCII", "ignore").decode("ASCII")

        #removing stop words
        text = text.replace(self.start_command, "").strip()
        # stop_words = nltk.corpus.stopwords.words(self.verbose_langs[self.lang])
        # words = nltk.tokenize.word_tokenize(text)
        # words = [word for word in words if word not in stop_words]
        # text = " ".join(words)

        return text

    def get_context(self,text:str) -> list:
        """
        Get the context of the command
        :param text: str: The text to be analyzed
        :return: str: The context of the command and the text without the context
        """
        context = ""
        if self.context_definer in text:
            context = text.split(self.context_definer)[1].strip().split(" ")[0].strip()
            text = text.replace(self.context_definer+" " + context, "").strip()
        return [context, text]

    def get_command(self,text:str, context: str) -> callable:
        """
        Get the command from the text
        :param text: str: The text to be analyzed
        :param possible_commands: list: The list of possible commands
        :return: callable: The command to be executed
        """
        possible_commands = self.commands
        if context:
            possible_commands = [command for command in self.commands if SequenceMatcher(None, context, command["context"]).ratio() > 0.8]
        
        command = None
        words = text.split(" ")
        for possible_command in possible_commands:
            for word in words:
                if SequenceMatcher(None, word, possible_command["command"]).ratio() > 0.8:
                    command = possible_command["function"]
                    text = text.split(word)[1].strip()
                    break
        
        return command, text

    def run(self) -> None:
        """
        Run a infinite loop that listens to the microphone and execute the commands
        :return: None
        """
        while True:
            text = recognizer(self.lang)
            print("Text: ", text)
            if text and text.lower().startswith(self.start_command):
                cleanned_text = self.clean_text(text)
                context, cleanned_text = self.get_context(cleanned_text)
                command, text = self.get_command(cleanned_text, context)
                result = None
                if command:
                    result = command(text)

                if type(result) == str:
                    print(result)
            time.sleep(1)
        
         


    