from pprint import pprint
import csv
import re

def format_phone(phone):
    pattern = r'(\+7|8)?\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})\s*(\(доб\.\s*(\d+)\))?'
    match = re.match(pattern, phone)
    if match:
        groups = match.groups()
        phone_number = f'+7({groups[1]}){groups[2]}-{groups[3]}-{groups[4]}'
        if groups[6]:
            phone_number += f' доб.{groups[6]}'
        return phone_number
    return phone

def main():
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    pprint(contacts_list)

    contacts_dict = {}
    for contact in contacts_list[1:]:
        full_name = " ".join(contact[:3]).split(" ")
        lastname = full_name[0]
        firstname = full_name[1]
        surname = full_name[2] if len(full_name) > 2 else ''
        organization = contact[3]
        position = contact[4]
        phone = format_phone(contact[5])
        email = contact[6]

        key = (lastname, firstname)
        if key in contacts_dict:
            existing_contact = contacts_dict[key]
            if not existing_contact[2]:  # surname
                existing_contact[2] = surname
            if not existing_contact[3]:  # organization
                existing_contact[3] = organization
            if not existing_contact[4]:  # position
                existing_contact[4] = position
            if not existing_contact[5]:  # phone
                existing_contact[5] = phone
            if not existing_contact[6]:  # email
                existing_contact[6] = email
        else:
            contacts_dict[key] = [lastname, firstname, surname, organization, position, phone, email]

    new_contacts_list = [contacts_list[0]] + list(contacts_dict.values())

    pprint(new_contacts_list)

    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(new_contacts_list)


if __name__ == "__main__":
    main()
