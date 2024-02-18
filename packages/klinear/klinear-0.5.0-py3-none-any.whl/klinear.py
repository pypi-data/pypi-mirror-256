# nailplot.py
import requests

# this will help retrieve the content of the file
def dag(qn, line=None):
    content = requests.get(
        "https://raw.githubusercontent.com/vinodhugat/qqqqq/main/"+qn)

    if line is not None:
        modcontent = content.text.split("\n")
        return modcontent[line]
    else:
        return content.text
