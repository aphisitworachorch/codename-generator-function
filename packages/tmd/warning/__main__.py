from bs4 import BeautifulSoup
import requests
from pythainlp.util import thai_strptime
import urllib.parse
import re
from http import HTTPStatus

def create_plaintext_from_html(soup):
    plaintext = ""

    # Loop through the HTML elements and extract text
    for element in soup.recursiveChildGenerator():
        if hasattr(element, "text"):
            plaintext += element.text + " "

    return plaintext.strip()


def get_tmd_weather(get_latest: bool):
  get_tmd_alert = requests.get("https://www.tmd.go.th/warning-and-events/warning-storm", params={
      "show": 1 if get_latest else 10,
  })
  parsedata = BeautifulSoup(get_tmd_alert.content,"html.parser")
  find_listcontent = parsedata.find_all(class_="list-content")

  warning = list()

  for data in find_listcontent:
    formatter = {
        "alert_at":"",
        "alert_no":"",
        "alert_affected_to":"",
        "details":"",
        "alert_title":"",
        "alert_details":"",
        "contents":[],
        "format":""
    }
    alerted_date = thai_strptime(data.find("div",attrs={"class":None}).get_text(),"%d %B %Y")
    alert_source = data.find(class_="link-list-title").find("a")
    details = alert_source.get_text()
    inner_details = data.find(class_="link-list-title").find("a",href=True)
    get_details = requests.get(f"https://www.tmd.go.th{inner_details['href']}")
    parsing_details = BeautifulSoup(get_details.content,"html.parser")
    head_title = parsing_details.find("h1",class_="text-dark1").get_text()
    head_details = parsing_details.find("div",class_="font-small text-dark2").get_text()
    images = parsing_details.find("section",class_="subpage-paragraph").find("div",class_="ps-3")
    classify_content = images.find_all("p")

    formatter['alert_at'] = alerted_date.isoformat()
    formatter['details'] = details.replace("  "," ")
    formatter['alert_title'] = head_title
    formatter['alert_details'] = head_details
    formatter['alert_affected_to'] = thai_strptime(' '.join(re.findall(r'\([^)]*\)', formatter['details'])[-1].split(" ")[1:]).replace(")",""),"%d %B %Y").isoformat()
    formatter['alert_no'] = re.findall(r'ฉบับที่\s+[0-9]+', formatter['details'])[-1].replace("ฉบับที่ ",'')
    for content in classify_content:
      if (content.find("img")):
        formatter['format'] = "images"
        for images in content.find_all("img",src=True):
          sources = f"https://www.tmd.go.th{images['src']}"
          formatter['contents'].append(sources)
      else:
        formatter['format'] = "text"
        sources = create_plaintext_from_html(content)
        formatter['contents'].append(sources.replace("\xa0",""))
    
    if (formatter['format'] != "images"):
      formatter['contents'].append(' '.join(formatter['contents']))

    warning.append(formatter)

  return warning


def main(args):
  try:
    pretty_data = get_tmd_weather(bool(args.get("get_latest")))
    
    if pretty_data is not None:
        return {
        'statusCode': HTTPStatus.OK,
        'body': pretty_data
        }
    else:
       return {
          'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
          'body':[]
       }
  except Exception as e:
     print(e)
     return {
          'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
          'body':e
       }
