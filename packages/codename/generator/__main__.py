from http import HTTPStatus
from bangsue_codename import *

def main(args):
  try:
    p = BangsueCodename.ThailandDistrict()
    codename = p.get_code_name()
    cname = p.convert_codename_to_string(codename, "all")

    if cname is not None:
        return {
        'statusCode': HTTPStatus.OK,
        'body': cname
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
