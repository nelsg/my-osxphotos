from __future__ import annotations

import osxphotos
from osxphotos.cli import query_command, verbose
import json
import logging
import re
from datetime import datetime


DATE_REGS = [
    r"([0-9]{4})(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])_(2[0-3]|[01][0-9])([0-5][0-9])([0-5][0-9])",
    r"([0-9]{4})\-(0[1-9]|1[0-2])\-(0[1-9]|[1-2][0-9]|3[0-1]) (2[0-3]|[01][0-9])\.([0-5][0-9])\.([0-5][0-9])",
]


def load_photos():
    with open('./data/myphotos.json') as f:
        photos = json.load(f)
    for photo in photos:
        photo['created'] = datetime.fromisoformat(photo['created'])
        photo['modified'] = datetime.fromisoformat(photo['modified'])
    return photos


def save_photos(photos):
    with open('./data/myphotos.json', 'w') as f:
        f.write(json.dumps(photos, indent=4, sort_keys=True, default=str))


def compute_duplicates_names(photos):
    duplicates_name = {}
    for photo in photos:
        if photo['name'] in duplicates_name:
            duplicates_name[photo['name']] += 1
            photo['duplicated_name'] = True
        else:
            duplicates_name[photo['name']] = 1
    print(f"Nb unique names : " + str(len(list(filter(lambda v: v==1, duplicates_name.values())))))
    print(f"Nb duplicates names : " + str(len(list(filter(lambda v: v>1, duplicates_name.values())))))
    print(f"Nb duplicates photos : " + str(sum(filter(lambda v: v>1, duplicates_name.values()))))
    with open('./data/duplicates.json', 'w') as f:
        f.write(json.dumps(duplicates_name, indent=4))
    return duplicates_name


def compute_photo_names_datetime(photos):
    for photo in photos:
        name = photo['name']
        for datereg in DATE_REGS:
            m = re.match(datereg, name)
            if m:
                datetime_name = datetime.fromisoformat(f"{m.group(1)}-{m.group(2)}-{m.group(3)}T{m.group(4)}:{m.group(5)}:{m.group(6)}")
                photo['datetime_name'] = datetime_name
                if datetime_name != photo['created']:
                    photo['created_inconsistent'] = True
                if (datetime_name - photo['created']).days > 1:
                    print(f"High diff for {photo['name']}")
                break


def main():
    photos = load_photos()
    duplicates_name = compute_duplicates_names(photos)
    compute_photo_names_datetime(photos)
    save_photos(photos)
    for photo in photos:
        if  'created_inconsistent' in photo and \
            'duplicated_name' in photo and \
            photo['created_inconsistent'] and \
            photo['duplicated_name']:
            print(f"Duplicated and datename inconsistent for {photo['name']}")

if __name__ == "__main__":
    main()