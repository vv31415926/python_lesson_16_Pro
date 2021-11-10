import requests
import pprint

class HeadHunter_vacancies:
    def __init__(self):
        self.baseURL = 'https://api.hh.ru'
        self.vacancyURL = f'{self.baseURL}/vacancies'
        self.country = 'Россия'

    def view_vacancies( self, city:str ):
        idCountry, idRegion, idCity = self.get_id( city ) # ID заданного города
        num = 0
        for ind_page in range(200):
            params = {
                'per_page': 50,
                'page': ind_page,
                'area': idCity
            }
            response = requests.get( self.vacancyURL, params=params).json()
            items = response['items']   # список словарей вакансий
            set_vac = set([])
            for v in items:     # по элементам словаря
                name = v['name']
                set_vac.add( name )
            break
        return set_vac

    def get_id( self, nameCity:str ):
        # [{'areas'Страна: [{'areas'j,область/край/республика : [{'areas'Город: [],
        url_area = f'{self.baseURL}/areas'
        response = requests.get(url_area).json()   # список [0] из словарей стран

        res = ''
        for dicCountrys in response: # по словарям стран
            if dicCountrys['name'] == self.country:
                # словарь областей нужной страны
                idCountry = dicCountrys['id']  # ID нужной страны
                lstRegions = dicCountrys['areas'] # список словарей областей
                for dicRegion in lstRegions:
                    # словарь области с городами
                    lstCitys = dicRegion['areas']   # список словарей городов
                    for dicCity in lstCitys:
                        # словарь города
                        if dicCity['name'] == nameCity:
                            # нужный город
                            idRegion = dicCity['parent_id']
                            idCity = dicCity['id']
                            res = (idCountry, idRegion, idCity )
                            break
                    if res:
                        break
                if res:
                    break
            if res:
                break

        return res

if __name__ == '__main__':
    hh = HeadHunter_vacancies()

    #r = hh.get_id_Region( 'Челябинск' )
    #print( r )

    r = hh.view_vacancies('Челябинск')
    print( len(r) )
    pprint.pprint( r )