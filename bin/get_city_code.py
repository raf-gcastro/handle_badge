#! -*- encoding: utf-8 -*-

from sys import argv, exit


THRESHOULD = 3

def read_file(city_file):
    import yaml

    with open(city_file,'r') as f:
        cities = yaml.load(f, Loader=yaml.FullLoader)
        f.close()

    return cities

def handle_city_name(city_name):
    from unidecode import unidecode

    handled_city_name = unidecode(city_name.lower().replace("'",''))
    handled_city_name = handled_city_name.replace('-',' ')
    handled_city_name = handled_city_name.replace('_',' ')

    return handled_city_name

def generate_hash_cities(cities, city_name):
    import Levenshtein

    city_name = handle_city_name(city_name)
    proximity = {}
    for i in range(THRESHOULD):
        proximity[i] = {}

    for key, value in cities.items():
        value_name = handle_city_name(value['nome_municipio'])
        dist = Levenshtein.distance(value_name, city_name)

        if (dist < THRESHOULD):
            proximity[dist][value['nome_municipio']] = {'codigo_municipio':value['codigo_municipio'], 'sigla_uf':value['sigla_uf']}

    return proximity

def get_city_code(hash_cities):
    print('Por favor, confirme o nome da cidade e a UF:')
    print('--------------------------------------------')
    count = 0
    answer = {}

    if (hash_cities[0] != {}):
        city = list(hash_cities[0].keys())[0]
        print(str(count)+':', city, '-', hash_cities[0][city]['sigla_uf'], '[Enter]')
        print()
        answer[count] = hash_cities[0][city]['codigo_municipio']
        count += 1
   
        cities = list(hash_cities[0].keys())[1:]
        for city in cities:
            print(str(count), '-', city, '-', hash_cities[0][city]['sigla_uf'])
            answer[count] = hash_cities[0][city]['codigo_municipio']
            count += 1

    city_proximity = list(hash_cities.keys())[1:]
    for key in city_proximity:
        for city in hash_cities[key].keys():
            print(str(count)+':', city, '-', hash_cities[key][city]['sigla_uf'])
            answer[count] = hash_cities[key][city]['codigo_municipio']
            count += 1
    print('--------------------------------------------')
    print('Insira o número correspondente à opção: ')
    idx_city = input()
    
    if (idx_city != '' and not idx_city.isdigit() and int(idx_city) not in range(count)):
        print('Opção inválida! Tente novamente.')

        return get_city_code(hash_cities)
    
    if (idx_city == ''):
        return answer[0]
    elif (idx_city.isdigit()):
        return answer[int(idx_city)]
    else:
        print('Um erro inesperado aconteceu.')
        print('Execução abortada.')
        exit(-1)

def save_in_file(city_code, tmp_file):
    with open(tmp_file,'w') as f:
        f.write(city_code)
        f.close()

def main():
    if (len(argv) != 4):
        print('Usage:', argv[0], '<path/to/municipios.yml>', '<tokenized_city_name>', '<tmp_file.txt>')
        exit(-1)

    city_file = argv[1]
    city_name = argv[2]
    tmp_file  = argv[3]

    cities = read_file(city_file)
    hash_cities = generate_hash_cities(cities, city_name)
    city_code = get_city_code(hash_cities)

    save_in_file(city_code, tmp_file)
    return 0

if (__name__ == '__main__'):
    main()
