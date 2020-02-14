import requests, json, os

try:
   from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup 

def getTableFromWahlrechtSubPage(url:str):
    request = requests.get(url)
    parsed_html = BeautifulSoup(request.content, features="html.parser")
    table = parsed_html.body.find('table', attrs={'class':'wilko'})
    table_head = table.find('thead')
    table_body = table.find('tbody')
    
    #works
    parties_list = getPartiesFromTableHead(table_head)
    print(str(parties_list))

    parsed_table:map = {}
    for table_row in table_body.find_all('tr'):
        parsed_row:list = []
        for table_cell in table_row.find_all('td'):
            if len(table_cell.contents) != 0:
                content = table_cell.contents[0]

                if "%" in str(content) or "–" == str(content):
                    parsed_row.append(content)
        try:
            date_cell = table_row.find_all('td', attrs={'class':'s'})[0]
            parsed_table[str(date_cell.contents[0])] = parsed_row
        except IndexError:
            None

    return {'parties':parties_list, 'values':parsed_table}


def getPartiesFromTableHead(table_head:BeautifulSoup):
    parties_soup = table_head.find_all('th')
    parties:list = []
    for party_elem in parties_soup:
        party_string:str = ''
        if 'class' in party_elem.attrs:
            classes = party_elem.attrs['class']
            if len(classes) == 1 and classes[0] == 'part':
                for contained_element in party_elem.contents:
                    if hasattr(contained_element, 'contents'):
                        party_string += str(contained_element.contents[0])
                    else:
                        party_string += str(contained_element)
                parties.append(party_string)
        else:
            #Sonstige has no class
            if 'Sonstige' in str(party_elem):
                parties.append('Sonstige')
    return parties

def main():
    print("Executing main function:")
    # request = requests.get('https://www.wahlrecht.de/umfragen/forsa.htm')
    # print("######################################BEGIN########################################")
    # for line in request.iter_lines():
    #     print(line)
    # print("######################################END########################################")

    # parsed_html = BeautifulSoup(request.content)
    # print(parsed_html.body.find('table', attrs={'class':'wilko'}).text)
    data:map = {}
    data['forsa'] = getTableFromWahlrechtSubPage('https://www.wahlrecht.de/umfragen/forsa.htm')
    data['allensbach'] = getTableFromWahlrechtSubPage('https://www.wahlrecht.de/umfragen/allensbach.htm')
    data['emnid'] = getTableFromWahlrechtSubPage('https://www.wahlrecht.de/umfragen/emnid.htm')
    data['politbarometer'] = getTableFromWahlrechtSubPage('https://www.wahlrecht.de/umfragen/politbarometer.htm')
    data['gms'] = getTableFromWahlrechtSubPage('https://www.wahlrecht.de/umfragen/gms.htm')
    data['dimap'] = getTableFromWahlrechtSubPage('https://www.wahlrecht.de/umfragen/dimap.htm')
    data['insa'] = getTableFromWahlrechtSubPage('https://www.wahlrecht.de/umfragen/insa.htm')
    data['yougov'] = getTableFromWahlrechtSubPage('https://www.wahlrecht.de/umfragen/yougov.htm')
    
    dir:str = "C:\\Users\\Robin\\Google Drive\\Privat\\IONOS\\Sonntagsfrage-Website\\data\\"
    try:
        os.stat(dir)
    except:
        os.mkdir(dir) 
    for datum in data.items():
        fileName = dir + str(datum[0]) + '.json'
        with open(fileName, 'w') as fp:
            json.dump(datum[1], fp)
        print("stored " + fileName + ".")

def debug():
    #getTableFromWahlrechtSubPage('https://www.wahlrecht.de/umfragen/insa.htm')
    print(getTableFromWahlrechtSubPage('https://www.wahlrecht.de/umfragen/insa.htm'))


if __name__== "__main__":
    main()
    #debug()