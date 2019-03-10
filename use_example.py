import csv
import requests
import json
from io import StringIO
import  matplotlib.pyplot as plt


def get_datagovua_data(package_id):
    DATASET_URL = "https://data.gov.ua/api/3/action/package_show?"
    BASE_REQUEST_URL = "https://data.gov.ua/api/3/action/resource_show?"
    params_package = {'id': package_id}

    r = requests.get(url=DATASET_URL, params=params_package)

    req = json.loads(r.text)

    resource_id = req['result']['resources'][-1]['id']
    params_dataset = {'id': resource_id}

    r2 = requests.get(url=BASE_REQUEST_URL, params=params_dataset)

    req2 = json.loads(r2.text)

    dataset_link = req2['result']['url']
    r3 = requests.get(dataset_link)

    return r3.text


if __name__ == "__main__":
    package_id = "338a8ccf-8b77-476b-b138-9bb5b7550584"
    sdata = get_datagovua_data(package_id)

    data = []
    f = StringIO(sdata)
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        data.append(row)

    for row in data:
        print(row)
    increase_ind = [3 + (3 * i) for i in range(8)]
    print(increase_ind)
    ua_migration_increase = [int(data[2][i]) for i in increase_ind]
    print(ua_migration_increase)

    plt.plot(list(range(len(ua_migration_increase))), ua_migration_increase)
    plt.show()
