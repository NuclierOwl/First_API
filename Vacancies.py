import json
import requests
import os
import constants


def get_data_from_hh():
    vacancies = []
    params = constants.params
    result = requests.get(constants.url, params).json()
    pages = result["pages"]
    vacancies.extend(result["items"])
    for i in range(1, pages):
        params["page"] += 1
        result = requests.get(constants.url,
                              params).json()
        if "items" in result.keys():
            vacancies.extend(result["items"])
    return vacancies


class Vacancies:
    def __init__(self):
        self._vacancies = []
        self._vacancies = self.__read_json()
        if not self._vacancies:
            self._vacancies = get_data_from_hh()
            print("get from hh")
            self.__save_to_json()
            print("saving")

    def __save_to_json(self):
        if self._vacancies:
            file = open("vacancies.json", "+w", encoding="utf-8")
            vacancies = "\n".join([json.dumps(vacancy) for vacancy in self._vacancies])
            file.write(vacancies)
            file.close()

    def __read_json(self):
        vacancies = []
        print("try read")
        if os.path.getsize("vacancies.json") > 0:
            with open("vacancies.json", "+r", encoding="utf-8") as file:
                vacancies_prep = file.read().split('\n')
                vacancies = [json.loads(item) for item in vacancies_prep]
        return vacancies

    def get_vacancies(self):
        return self._vacancies