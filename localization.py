import json
import os

default = "en"

def get(locale, text_id, *args):
    try:
        file = "./Locale/"+locale+".loc"
        if not os.path.exists(file):
            file = "./Locale/"+locale.split("_")[0]+".loc"
            if not os.path.exists(file):
                file = "./Locale/"+default+".loc"
    
        with open(file, "r", encoding="utf-8") as json_file:
            parsed_json = json.load(json_file)
            result = parsed_json["translation"].get(text_id, text_id)

            if result == text_id:
                file = "./Locale/"+default+".loc"
                 with open(file, "r", encoding="utf-8") as json_file:
                    parsed_json = json.load(json_file)
                    result = parsed_json["translation"].get(text_id, text_id)

            for i, ele in enumerate(args):
                result = result.replace("%$"+str(i), str(ele))

            return result
    except Exception as e:
        print(e)
        return text_id
