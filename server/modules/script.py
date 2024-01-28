import re

def group_words(text, n=5):
    words = re.findall(r'\b\w+\b', text)
    return [' '.join(words[i:i+n]) for i in range(0, len(words), n)]



def convertMillisToTc(millis: int) -> str:
    #utility function to convert miliseconds to timeCode hh:mm:ss,mmm
    miliseconds,seconds=divmod(int(millis/1000),60)
    minutes=int(millis/(1000*60))%60
    hours=int(millis/(1000*60*60))%24
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{miliseconds:03d}"

def main():
    #define globals
    text = '''An application programming interface (API) is a way for two or more computer programs or components to communicate with each other. It is a type of software interface, offering a service to other pieces of software.[1] A document or standard that describes how to build or use such a connection or interface is called an API specification. A computer system that meets this standard is said to implement or expose an API. The term API may refer either to the specification or to the implementation. Whereas a system's user interface dictates how its end-users interact with the system in question, its API dictates how to write code that takes advantage of that system's capabilities.'''
    RAW_TEXT_LIST = []   # you should assing to RAW_TEXT_LIST each section of the text
    NAME_OF_FILE = str = "script" #change this

    currentSection = 0

    def makeSubRipStr(rawText : str, initialTimeCode: str, durationInMiliseconds : int ) -> str: 
        nonlocal currentSection
        
        currentSection+=1 # we add 1 to the currentSection counter, starting in 1.
        
        print(initialTimeCode.split(":"))
        print(len(initialTimeCode.split(":")))
        hours,minutes,seconds,miliseconds = initialTimeCode.split(":")
        initialTimeCodeInMilis : int = sum((3600000 * int(hours), 60000 * int(minutes),1000 * int(seconds), int(miliseconds)) )
        finalTimeCode : str = convertMillisToTc(initialTimeCodeInMilis + durationInMiliseconds);
        formatedText : str = f'{currentSection}\n{initialTimeCode} --> {finalTimeCode}\n{rawText}\n\n'
        return formatedText

    #Create the file and do nothing with it


    #open the file in "append mode and add each entry formated"
    with open(file=f"./{NAME_OF_FILE}.srt",mode="a+",encoding="utf-8") as subFile: pass
    


    grouped_words = group_words(text)

    for i, x in enumerate(grouped_words):
        RAW_TEXT_LIST.append([x, convertMillisToTc(5000 * i), 5])

    with open(file=f"./{NAME_OF_FILE}.srt",mode="w",encoding="utf-8") as subFile:
        for sourceTuple in RAW_TEXT_LIST:
            text, initialTC, duration = sourceTuple
            subFile.write(makeSubRipStr(text,initialTC,duration)) 


if __name__ == '__main__':
    main()
