from http import HTTPStatus
from bangsue_codename import *

def main():
  try:
    p = BangsueCodename.MRTATrain()
    codename = p.get_code_name()
    return {"body": p.convert_codename_to_string(codename, "station_with_number"),"status": HTTPStatus.OK}
  except Exception as e:
    return {"body": e,"status": HTTPStatus.INTERNAL_SERVER_ERROR}
