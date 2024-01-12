from http import HTTPStatus
from bangsue_codename import *

def main():
  p = BangsueCodename.ThailandDistrict()
  codename = p.get_code_name()
  return {"body": p.convert_codename_to_string(codename, "all")} 
