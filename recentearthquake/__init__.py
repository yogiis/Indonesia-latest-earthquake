import requests as requests
from bs4 import BeautifulSoup


def data_extract():
    try:
        content = requests.get('https://bmkg.go.id')
    except Exception:
        return None

    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')
        results = soup.find('span', {'class': 'waktu'})
        results = results.text.split(', ')
        date = results[0]

        results = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        results = results.findChildren('li')
        i = 0
        magnitude = None
        depth = None
        location = None
        condition = None

        for res in results:
            if i == 1:
                magnitude = res.text
            elif i == 2:
                depth = res.text
            elif i == 3:
                koordinat = res.text.split(' - ')
                ls = koordinat[0]
                bt = koordinat[1]
            elif i == 4:
                location = res.text
            elif i == 5:
                condition = res.text
            i = i + 1

        hasil = dict()
        hasil['tanggal'] = date
        hasil['magnitude'] = magnitude
        hasil['kedalaman'] = depth
        hasil['koordinat'] = {'ls': ls, 'bt': bt}
        hasil['lokasi'] = location
        hasil['dirasakan'] = condition
        return hasil
    else:
        return None


def data_view(result):
    if result is None:
        print("Tidak bisa menemukan data gempa terkini")
        return

    print('Gempa terkini berdasarkan BMKG')
    print(f"Tanggal {result['tanggal']}")
    print(f"Magnitude {result['magnitude']}")
    print(f"Koordinat LS: {result['koordinat']['ls']}, BT: {result['koordinat']['bt']}")
    print(f"Lokasi {result['lokasi']}")
    print(f"Kondisi {result['dirasakan']}")


if __name__ == '__main__':
    result = data_extract()
    data_view(result)
