import requests
import json
import csv


def main():

  file = open('your_file.csv', 'rU')
  reader = csv.DictReader(file, fieldnames = ("name", "phone", "company_name", "address_line1", "address_line2",
                                              "city_locality", "state_province", "postal_code", "country_code"))
  next(reader)
  data = json.dumps([row for row in reader])

  try:
      url = your_address_validation_api_provider

      headers = {
                  'Content-Type': 'application/json',
                  'api-key': 'your_api_key'
                  }
      r = requests.post(url,  headers=headers, data=data)
      json_data = json.loads(r.text)

      flattened_json = flatten(json_data)

      to_csv_writer(flattened_json)

  except Exception as e:
    print(e)


def flatten(old_data, new_data=None, parent_key='', sep='.', width=2):
    '''
    recursively flattens nested json data
    :param old_data: the original data
    :param new_data: the resulting dictionary
    :param parent_key: the prefix assigned to each key
    :param sep: the separator between the keys
    :param width: width of the field when converting list indexes
    :return: a flattened json that uses dot notation
    '''
    if new_data is None:
        new_data = {}
    # checks if the data is a dictionary
    if isinstance(old_data, dict):
        for k, v in old_data.items():
            new_key = parent_key + sep + k if parent_key else k
            flatten(v, new_data, new_key, sep, width)
    # checks if the data is a list
    elif isinstance(old_data, list):
        if len(old_data) == 1:
            flatten(old_data[0], new_data, parent_key, sep, width)
        else:
            for i, elem in enumerate(old_data):
                new_key = "{}{}{:0>{width}}".format(parent_key, sep if parent_key else '', i, width=width)
                flatten(elem, new_data, new_key, sep, width)
    else:
        if parent_key not in new_data:
            new_data[parent_key] = old_data
        else:
            raise AttributeError("key {} is already used".format(parent_key))

    return new_data


def to_csv_writer(json_dict):
    '''
    Takes in the flattened json and writes it to csv
    :param json_dict: the flattened data dictionary
    '''
    # used to hold the header row for the csv
    header = []
    # loop through the json dictionary to get all the keys we will
    # use in the header of the csv. Each key starts with an index
    # ex "01.parent_name.child_name", this loop strips the index,
    # and adds unique keys to the list.
    for k, v in json_dict.items():
        k = k.split('.',1)[1]
        if k not in header:
            header.append(k)
    output_file = open('output.csv', 'w')
    writer = csv.writer(output_file, lineterminator = '\n')
    # write the header fields to the output csv.
    writer.writerow(header)
    # holds the next row we need to write to the csv.
    next_row = []
    index = 0
    # Loop through the data, if the index in the key matches our current index,
    # add the data to the next_row list.

    for k,v in json_dict.items():
        if int(k.split('.',1)[0]) == index:
            next_row.append(v)
        # otherwise write out the list, clear the list, append the value
        # of the current key, and increase the index.
        else:
            writer.writerow(next_row)
            next_row.clear()
            next_row.append(v)
            index+=1
    if len(next_row) > 0:
        writer.writerow(next_row)
    output_file.close()

if __name__ == '__main__':
  main()