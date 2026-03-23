# import json
import requests
# from functools import reduce
from typing import cast
from string import Template
from pyrsistent import v, pmap, PMap, PVector
from ..database import SessionLocal
from ..models import Breed


# new_breed_member = Breed(id="ha", umbrella_id="ha", readable_name="ha", img_link="hahaha")
session = SessionLocal()
# with SessionLocal() as session:
#   try:
#     session.add(new_breed_member)
#     session.commit()
#     print(f"Saved item with id: {new_breed_member.id}")
#   except Exception as e:
#     session.rollback()
#     print(f"Error: {e}")


random_image_template_url = Template("https://dog.ceo/api/breed/$breed/images/random")
def get_image(breed: str) -> str:
  url = random_image_template_url.safe_substitute(breed=breed)
  resp = requests.get(url)
  return resp.json().get("message")

listing_response = requests.get("https://dog.ceo/api/breeds/list/all")
listing_as_mapping: dict[str, list] = listing_response.json().get("message", {})

def _get_data():
  listing_response = requests.get("https://dog.ceo/api/breeds/list/all")
  mapping: PMap[str, list[str]] = pmap(listing_response.json().get("message", {}))
  keys = sorted(mapping.keys())
  def _create_breed_record(id: str, umbrella_id, readable_name: str) -> Breed:
    img_link = get_image(id)
    print("Got one image")
    return Breed(id=id, umbrella_id=umbrella_id, readable_name=readable_name, img_link=img_link)
  def work_on_inner_list(umbrella_id):
    inner_list: list[str] = cast(list[str], mapping.get(umbrella_id))
    if len(inner_list) == 0:
      new_breed_member = _create_breed_record(id=umbrella_id, umbrella_id=umbrella_id, readable_name=umbrella_id.title())
      session.add(new_breed_member)
      print("added a breed")
    else:
      sub_list: PVector[Breed] = v()
      for specifier in inner_list:
        id = f"{umbrella_id}/{specifier}"
        readable_name = f"{umbrella_id} ({specifier.title()})".title()
        sub_list.append(_create_breed_record(id=id, umbrella_id=umbrella_id, readable_name=readable_name))
        img_link = get_image(id)
        new_breed_member = Breed(id=id, umbrella_id=umbrella_id, readable_name=readable_name, img_link=img_link)
        session.add(new_breed_member)
        print("added a breed (sub)")

  for id in keys:
    work_on_inner_list(id)
  
  session.commit()

_get_data()
session.close()

