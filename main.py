import pyperclip
import xml.dom.minidom
import json
from pynput import keyboard

## pyperclip
#region pyperclip
def takeFromClipboard():
    copiedString = pyperclip.paste()
    return copiedString

def pasteToClipboard(textToPaste):
    pyperclip.copy(textToPaste)
#endregion

## JSON
#region JSON
def prettify_json(json_string):
    json_obj = json.loads(json_string)
    pretty_json_string = json.dumps(json_obj, indent=4, sort_keys=False)
    return pretty_json_string


def takeJsonPart(jsonToExtract):
    # print(f'Complete string is: {jsonToExtract}')
    print(f'Extracting json...\n\n\n')
    try:
        jsonPart = jsonToExtract.split('{',1)
        dataPart = jsonPart[0]
        jsonPart = '{' + jsonPart[1]
        # print(f'Json is: {jsonPart}')
        return dataPart, jsonPart
    except:
        return -1

def jsonPrettyfier():
    dataPart,jsonToExtract = takeJsonPart(takeFromClipboard())
    if (jsonToExtract != -1):
        prettyJson = prettify_json(jsonToExtract)
        print(f'Prettyfied Json is: {prettyJson}')
        parsedJson = dataPart + "\n" + prettyJson
        pasteToClipboard(parsedJson)
    else:
        print(f'Error')
#endregion

## XML
#region XML
def xmlPrettyfier():
    xmlString = xml.dom.minidom.parseString(takeFromClipboard())
    xml_pretty_str = xmlString.toprettyxml()
    print(xml_pretty_str) 
    pasteToClipboard(xml_pretty_str)
#endregion

## Language Detection
#region LanguageDetection
def detectLanguage():
    clipboardText = takeFromClipboard()
    if ( (clipboardText.find("application/json") != -1) or (clipboardText.find("{\"") != -1)):
        print("Is JSON")
        return 1
    elif ((clipboardText.find("application/xml") != -1) or (clipboardText.find("<?xml") != -1)) :
        print("Is XML")
        return 2
#endregion

## Key combination listener
#region listener
COMBINATION = {keyboard.Key.ctrl, keyboard.KeyCode.from_char('c')}
current = set()

def on_activate():
    print('Global hotkey activated!')
    try:
        if (detectLanguage() == 1):
            jsonPrettyfier()
        else:
            xmlPrettyfier()
    except:
        print("Nothing to prettify here! ErrorCode: -1")

def for_canonical(f):
    return lambda k: f(l.canonical(k))
#endregion

if __name__ == '__main__':
    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse('<ctrl>+c'),
        on_activate)
    with keyboard.Listener(
            on_press=for_canonical(hotkey.press),
            on_release=for_canonical(hotkey.release)) as l:
        l.join()