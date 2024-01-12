from http import HTTPStatus
from bangsue_codename import *

def main(args):
  p = BangsueCodename.ThailandDistrict()
  codename = p.get_code_name()
  return p.convert_codename_to_string(codename, "all")
