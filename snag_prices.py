import urllib.request
from dataclasses import dataclass


@dataclass
class House:
    price: str
    bed: str
    bath: str
    sqft: str


def fetch_data(link):
    """
    This function fetches all of the real estate listings in Rochester from the given realtor.com link
    """
    with open(link) as file:
        mystr = file.readlines()[0]
    
    index1 = mystr.find("/header><ul")
    index2 = mystr.find("</ul><script>")

    # Isolate the list of houses, split it into a list with an entry for each house
    mystr = mystr[index1:index2]
    entries = mystr.split("<li id")

    results = []
    for entry in entries:
        data = []

        edit_entry = entry
        # first, slice so the string to get to the correct piece of info
        dataidx = entry.find('"pc-price"')
        edit_entry = edit_entry[dataidx:]
        # next, slice so the data is first in the string
        dataidx = edit_entry.find(">")
        edit_entry = edit_entry[dataidx+2:]
        # finally, slice out the rest of the tag
        dataidx = edit_entry.find("<")
        edit_entry = edit_entry[:dataidx]
        edit_entry = edit_entry.replace(',', '')
        data.append(edit_entry)

        for datatype in ['beds"', 'baths"', 'sqft"']:
            edit_entry = entry
            # first, slice so the string to get to the correct piece of info
            dataidx = edit_entry.find('"pc-meta-'+datatype)
            edit_entry = edit_entry[dataidx:]
            # Now, slice so we're right in front of the data
            dataidx = edit_entry.find("meta-value")
            edit_entry = edit_entry[dataidx:]
            # Next, cut so the data is first in the string
            dataidx = edit_entry.find(">")
            edit_entry = edit_entry[dataidx+1:]
            # finally, slice out the rest of the tag
            dataidx = edit_entry.find("<")
            edit_entry = edit_entry[:dataidx]
            edit_entry = edit_entry.replace(',', '')
            edit_entry = edit_entry.replace('+', '')
            data.append(edit_entry)

        skip = False
        for i in range(4):
            skip = data[i] == '' or skip
        if not skip:
            results.append(House(data[0], data[1], data[2], data[3]))
    
    return results


def add_houses(houses, filename):
    with open(filename, 'a') as file:
        for house in houses:
            add_str = house.price + ';'
            add_str += house.bed + ';'
            add_str += house.bath + ';'
            add_str += house.sqft + '\n'
            file.write(add_str)


def main():
    total = 0
    for filename in ['website.html', 'website2.txt', 'website3.txt', 'website4.txt', 'website5.txt']:
        house_list = fetch_data(filename)
        print(house_list)
        print(len(house_list))
        total += len(house_list)
        add_houses(house_list, "realestate.txt")
    print("total: " + str(total))


if __name__ == "__main__":
    main()
