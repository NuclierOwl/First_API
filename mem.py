import requests

url = "https://api.hh.ru/vacancies"
params = {
    "currency": "RUR",
    "min_salary": 1,
    "only_with_salary": True,
    "max_salary": 20000000,
    "page": 0,
    "per_page": 100
}

def get_vacancies(url, params):
    response = requests.get(url, params=params)
    data = response.json()
    return data['items']

def get_region_salaries(vacancies):
    region_salaries = {}
    for vacancy in vacancies:
        region = vacancy['area']['name']
        salary = vacancy['salary']
        if salary:
            if region not in region_salaries:
                region_salaries[region] = []
            region_salaries[region].append(salary['from'])
            region_salaries[region].append(salary['to'])
    return region_salaries

def calculate_average_salary(salaries):
    average_salaries = {}
    for region, values in salaries.items():
        average_salaries[region] = sum(values) / len(values)
    return average_salaries

def calculate_max_salary(salaries):
    max_salaries = {}
    for region, values in salaries.items():
        max_salaries[region] = max(values)
    return max_salaries

def calculate_min_salary(salaries):
    min_salaries = {}
    for region, values in salaries.items():
        min_salaries[region] = min(values)
    return min_salaries

vacancies = get_vacancies(url, params)
region_salaries = get_region_salaries(vacancies)
average_salaries = calculate_average_salary(region_salaries)
max_salaries = calculate_max_salary(region_salaries)
min_salaries = calculate_min_salary(region_salaries)

for region in average_salaries:
    print(f"Region: {region}")
    print(f"Average Salary: {average_salaries[region]}")
    print(f"Max Salary: {max_salaries[region]}")
    print(f"Min Salary: {min_salaries[region]}")
    print()