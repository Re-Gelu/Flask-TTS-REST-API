from pathlib import Path
from chardet import UniversalDetector
from art import tprint
from PyPDF2 import PdfFileReader
import pyttsx3
import os


class TextToSpeech:
    __engine = pyttsx3.init()
    __voices = __engine.getProperty('voices')
    __voice_rate: int = 200
    __voice_id: int = 0
    text: str = ""
    __file_path: str = ""
    __save_path: str = ""
    
    def __init__(self, file_path=None, text: str = None, save_path: str = None, voice_rate: int = None, voice_id: int = None, autoconvert_file: bool = False):
        if file_path and text:
            raise Exception('Choose a file or a text string to pass in! Not both at the same time!')
        if file_path:
            self.file_path = file_path
        if text:
            self.text = text
        if save_path:
            self.save_path = save_path
        if voice_rate:
            self.voice_rate = voice_rate
        if voice_id:
            self.voice_id = voice_id
        if file_path and autoconvert_file:
            self.get_text_from_file()
        
    def get_text_from_file(self) -> str:
        """Get the text from the text file

        Raises:
            Exception: If file is not a PDF, TXT or RTF file
            Exception: If file path not found or not exsists

        Returns:
            str: text from the file
        """        
        if self.__file_path:
            
            match Path(self.__file_path).suffix:
                
                case ".txt" | ".rtf":
                    # Определение кодировки
                    detector = UniversalDetector()
                    with open(self.__file_path, 'rb') as fh:
                        for line in fh:
                            detector.feed(line)
                            if detector.done:
                                break
                        detector.close()

                    # Чтение файла
                    with open(self.__file_path, "r", encoding=detector.result['encoding']) as filehandle:
                        self.text = filehandle.read()
                    self.text = self.text.replace("\n", " ")

                    return self.text
                
                case ".pdf":
                    # Работа с PDF форматом

                    # Чтение файла
                    with open(self.__file_path, "rb") as filehandle:
                        pdf = PdfFileReader(filehandle)

                        self.pdf_document_info = pdf.getDocumentInfo()

                        self.text = ""

                        for page_number in range(pdf.numPages):
                            pdf_page = pdf.getPage(page_number)
                            self.text += pdf_page.extract_text()

                    self.text = self.text.replace("\n", " ")

                    return self.text
                
                case _:
                    raise Exception('File format not supported!')
            
        else:
            raise Exception('File path not found or not exsists! Try to change `file_path` variable.')
        
    def save(self) -> str:
        """Method to save the mp3 file from the text

        Raises:
            Exception: If no text string to save

        Returns:
            str: Path to the mp3 file
        """        
        if self.text: 
            final_filename = "voice.mp3"
            self.__save_path = self.__save_path + final_filename

            # Преобразование в голос
            self.__engine.setProperty("rate", self.__voice_rate)  # Установка скорости чтения
            self.__engine.setProperty('voice', self.__voices[self.__voice_id].id)  # Установка голоса
            self.__engine.save_to_file(self.text, self.__save_path)
            self.__engine.runAndWait()

            #print(f"[+] Done! Check - {os.path.abspath(final_filename)}")
            return os.path.abspath(final_filename)
        else:
            raise Exception('No text string to save! Try to change `text` variable or use file methods!')
    
    @property
    def file_path(self) -> str:
        """File path getter

        Returns:
            File path: Private class variable
        """        
        return self.__file_path
    
    @file_path.setter
    def file_path(self, path: str):
        """File path setter

        Args:
            path (str): Valid path to file

        Raises:
            Exception: If file path is not found or not exsists
        """        
        if path and Path(path).exists() and Path(path).is_file():
            self.__file_path = path
        else:
            raise Exception('Path to file not found or not exsists!')
    
    @property
    def save_path(self):
        """Save path getter

        Returns:
            Save path: Private class variable
        """
        return self.__save_path
    
    @save_path.setter
    def save_path(self, path: str):
        """Save path setter

        Args:
            path (str): Valid path to folder

        Raises:
            Exception: If path to save not found or not exsists!
        """        
        if path and Path(path).exists():
            self.__save_path = path
        else:
            raise Exception('Path to save not found or not exsists!')
    
    @property
    def voices(self):
        """Voices getter

        Returns:
            Voices: List of system tts voices
        """        
        return self.__voices
        
    @property
    def voice_id(self):
        """Voice id getter

        Returns:
            Voice_id: Private class variable
        """        
        return self.__voice_id

    @voice_id.setter
    def voice_id(self, id: int):
        """Voice id setter

        Args:
            id (int): Valid voice id in list of sytem voices

        Raises:
            Exception: If voice id is not in system voices list
        """        
        if 0 <= id <= len(self.__voices) - 1:
            self.__voice_id = id
        else:
            raise Exception('Voice id must be in system voices list! You can check it by calling `voices` variable.')
        
    @property
    def voice_rate(self):
        """Voice rate getter

        Returns:
            Voice_rate: Private class variable
        """        
        return self.__voice_rate
    
    @voice_rate.setter
    def voice_rate(self, value: int):
        """Voice rate setter

        Args:
            value (int): Valid voice rate

        Raises:
            Exception: If voice rate < 0 or > 1000
        """        
        if 0 <= value <= 1000:
            self.__voice_rate = value
        else:
            raise Exception('Voice rate must be >= 0 and <= 1000!')

if __name__ == "__main__":
    tprint("TEXT TO SPEECH by Re:Gelu", font="Slant")

    #file_path = input("Input file path: ")
    #print(" ")

    tts = TextToSpeech(
        file_path="text.txt",
        save_path=os.path.join("uploads/audios/"),
        autoconvert_file = True
    )
    #tts = TextToSpeech(text="Я ебал твой рот наоборот!")
    tts.save()
    print("[+] Success!")