import requests
import json
import os
from datetime import datetime

URL = "https://akafoe.studylife.org/api/meal-plans/week"

MENSA_ID_DICT = {
    "RUB Mensa" : "a0f40678-5e86-4ae4-9ff1-ae1e9e25934b",
    "Q-West": "a0f40678-ac6b-4b31-a37b-7f0e4b5eb188",
    "Rote Bete": "a0f4067a-78d2-42c2-a3de-1006cf571dea"
}

def get_all_menus_next_week(name):
    week_num = ""
    try:
        # or "current"
        response = requests.get(f"{URL}/next?canteen_id={MENSA_ID_DICT.get(name)}")
        if (response.status_code == 200):
            data = response.json()
            week_num += str(data["week_number"])
            menu_by_days = data["days"]
            menu = { d["date"] : 
                        { m["title"] : {
                                "price_stud" : m["price_student"]
                                , "price_empl" : m["price_employee"]
                                , "price_gue" : m["price_guest"]  
                                , "alleg" : m["allergens"]} 
                            for m in d["meals"]}
                    for d in menu_by_days}
            # create if path does not exist, and write down menu locally
            os.makedirs(f"./menu/kw{week_num}", exist_ok=True)
            with open(f"./menu/kw{week_num}/{name}.json", "w", encoding="utf-8") as f:
                json.dump(menu, f, ensure_ascii=False)
            return menu
        elif (response.status_code == 401):
            raise Exception(f"No valid data for {name} of next week.")
    except Exception as e:
        print(e)
        
def pretty_printer(menu_dict):
    for (date, dishes) in menu_dict.items():
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        print(f"\n{date}")
        for (titel, dish_info) in dishes.items():
            print(titel)
            print(f"Price (student): {dish_info["price_stud"]}")


for name in MENSA_ID_DICT.keys():
    print(f"\n{name}")
    menu = get_all_menus_next_week(name)
    pretty_printer(menu)
