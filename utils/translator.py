from googletrans import Translator
translator = Translator()

async def detect_language(text:str):
    result = await translator.detect(text=text[:500])
    return result  


async def translate(text:list):
    result = await translator.translate(text=text,dest='en')
    x = []
    for items in result:
        x.append(items.text)

    content = "".join(x)
    return content


    



