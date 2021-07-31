import csv
import requests as requests
import json


def write_csv(file="diem2021.csv", start=1000000, end=64999999):
    with open(file, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL, lineterminator='\n')
        writer.writerow(['SBD', 'Toan', 'Van', 'Ly', 'Hoa', 'Sinh', 'Su', 'Dia', 'GDCD', 'Anh'])

        countError = 0
        try:
            while start <= end:
                sbd = '0' + str(start) if (start <= 9999999) else str(start)
                URL = "https://diemthi.tuoitre.vn/search-thpt-score"
                data = {"data": sbd, "code": ""}
                content = requests.post(URL, json=data)

                if (content.status_code != 200):
                    print("Status code =/= 200")
                    f.close()
                    print("End at sbd: " + sbd)

                json_data = content.json()
                if len(json_data.get('data')) == 0:
                    countError += 1
                    print("Failure")

                else:
                    countError = 0
                    source = json_data.get('data')[0].get('_source')
                    diem = source.get('score')[:-1]

                    diem = diem.split(";")

                    list = [sbd]
                    for mon in diem:
                        list.append(mon.split(":")[-1])
                    writer.writerow(list)

                    print("Done: " + str(list))
                start += 1
                if countError >= 50:
                    start = ((start // 1000000) + 1) * 1000000
                    countError = 0

        except Exception as e:
            print(e)
            f.close()
            print("End at sbd: " + sbd)


write_csv()
