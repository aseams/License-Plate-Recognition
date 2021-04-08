import json

jason=r"""{"ParsedResults":[{"TextOverlay":{"Lines":[{"LineText":"New Jersey","Words":[{"WordText":"New","Left":188.0,"Top":48.0,"Height":56.0,"Width":216.0},{"WordText":"Jersey","Left":416.0,"Top":48.0,"Height":76.0,"Width":320.0}],"MaxHeight":76.0,"MinTop":48.0},{"LineText":"ZPT 958","Words":[{"WordText":"ZPT","Left":50.0,"Top":120.0,"Height":228.0,"Width":414.0},{"WordText":"958","Left":454.0,"Top":120.0,"Height":228.0,"Width":358.0}],"MaxHeight":228.0,"MinTop":120.0},{"LineText":"Garden State","Words":[{"WordText":"Garden","Left":210.0,"Top":354.0,"Height":74.0,"Width":244.0},{"WordText":"State","Left":478.0,"Top":354.0,"Height":74.0,"Width":188.0}],"MaxHeight":74.0,"MinTop":354.0}],"HasOverlay":true,"Message":"Total lines: 3"},"TextOrientation":"0","FileParseExitCode":1,"ParsedText":"New Jersey\nZPT 958\nGarden State","ErrorMessage":"","ErrorDetails":""}],"OCRExitCode":1,"IsErroredOnProcessing":false,"ProcessingTimeInMilliseconds":"421"}"""

json_dict = json.loads(jason)

print("Full Text:\n" + json_dict['ParsedResults'][0]['ParsedText'])
print("Top Line: " + json_dict['ParsedResults'][0]['TextOverlay']['Lines'][0]['LineText'])
print("Middle Line: " + json_dict['ParsedResults'][0]['TextOverlay']['Lines'][1]['LineText'])
print("Bottom Line: " + json_dict['ParsedResults'][0]['TextOverlay']['Lines'][2]['LineText'])