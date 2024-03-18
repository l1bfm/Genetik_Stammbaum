#!/usr/bin/python3
"""
Ein Programm, das den Stammbaum für eine genetisch veranlagte Krankheit ermittelt.

(c) 2020 - 2024 by l1bfm
"""
import sqlite3, pprint
krankheit = {'Name': '', 'Dominant-Rezessiv': True, 'Dominant': False, 'Autosomal': True}
connection = sqlite3.connect('db')
cursor = connection.cursor()
cursor.execute("SELECT * FROM krankheiten")
print(cursor.fetchall())
krankheit['Name'] = input("Bitte geben Sie den Namen der Krankheit ein.")
cursor.execute("SELECT * FROM krankheiten WHERE Name=?", [(krankheit['Name'])])
krankheit_raw = cursor.fetchall()
krankheit['Dominant-Rezessiv'] = krankheit_raw[0][1]
krankheit['Dominant'] = krankheit_raw[0][2]
krankheit['Autosomal'] = krankheit_raw[0][3]
print(krankheit)



# krankheit['Name'] = input('Name der Krankheit: ')
# krankheit['Dominant-Rezessiv'] = input('Dominant-Rezessiver Erbgang? (Wenn falsch: Enter drücken): ')
# krankheit['Dominant'] = input('Dominant? (Wenn falsch: Enter drücken): ')
# krankheit['Autosomal'] = input('Autosomal? (Wenn falsch: Enter drücken): ')

class Mensch:
    """
    Klasse für den Menschen.
    """

    def __init__(self, name, symptome, eltern, geschwister, kinder, maennlich: bool, anfang):
        self.name = name
        self.maennlich = maennlich
        self.symptome = symptome
        self.chromosomen = [0.0,0.0]
        # 1: erkrankt, bei nicht autosomalen Erbgängen beim Mann wird bei nur das erste Chromosom betrachtet
        self.p_erkranken = float()
        self.eltern_names = eltern
        self.eltern = []
        self.geschwister_names = geschwister
        self.geschwister = []
        self.kinder_names = kinder
        self.kinder = []
        self.anfang = anfang

    def __repr__(self):
        return self.name

    def replace_names_with_objects(self):
        for name in self.eltern_names:
            for person in personen:
                if name == person.name:
                    self.eltern.append(person)
        for name in self.geschwister_names:
            for person in personen:
                if name == person.name:
                    self.geschwister.append(person)
        for name in self.kinder_names:
            for person in personen:
                if name == person.name:
                    self.kinder.append(person)

    def find_lost_relatives(self):
        for person in personen:
            if person in self.kinder or person in self.eltern or person in self.geschwister:
                continue
            if self.name in person.eltern_names:
                self.kinder.append(person)
            if self.name in person.geschwister_names:
                self.geschwister.append(person)
            if self.name in person.kinder_names:
                self.eltern.append(person)

    def find_out_chromosomes_by_illness(self):
        if krankheit['Dominant-Rezessiv'] == 1:
            if krankheit['Dominant'] == 1:
                if self.symptome == 1:
                    self.chromosomen[0] = 1.0
                    # Unklar, ob das zweite Chromosom auch erkrankt ist

            else:
                if self.symptome == 1:
                    self.chromosomen = [1.0,1.0]
        else:
            print('Noch nicht implementiert: nicht dominant-rezessive Erbgänge')
            if krankheit['Autosomal'] is True:
                pass
            else:
                pass

    def find_out_chromosomes_by_relatives(self):
        if krankheit['Dominant-Rezessiv'] and not krankheit['Dominant'] and krankheit['Autosomal']:
            if self.symptome:
                return
            for kind in self.kinder:
                if 1.0 in kind.chromosomen and not self.symptome and not kind.symptome:
                    anderes_elternteil = kind.eltern
                    # print(self.name, 'ae', len(anderes_elternteil), anderes_elternteil)
                    if 1.0 in anderes_elternteil[0].chromosomen:
                        continue
                    self.chromosomen = [1.0,0.0]
                elif kind.symptome and self.symptome:
                    self.chromosomen = [1.0,1.0]
                elif kind.symptome and not self.symptome:
                    self.chromosomen = [1.0,0.0]
            # print(self.name, self.eltern)
            if self.eltern != []:
                for i in range(2):
                    if self.eltern[i].symptome:
                        self.chromosomen[i] = 1.0
                    elif 1.0 in self.eltern[i].chromosomen:
                        self.chromosomen[i] = 0.5

    def calc_probability(self):
        if krankheit['Dominant-Rezessiv'] and not krankheit['Dominant'] and krankheit['Autosomal']:
            self.p_erkranken = self.chromosomen[0] * self.chromosomen[1]
        elif krankheit['Dominant-Rezessiv'] and krankheit['Dominant'] and krankheit['Autosomal']:
            self.p_erkranken = self.chromosomen[0]
            if self.chromosomen[1] > self.p_erkranken:
                self.p_erkranken = self.chromosomen[1]


cursor.execute("SELECT * FROM stammbaum_1 ORDER BY Anfang")
personen_raw = cursor.fetchall()
personen = []
for person_data_raw in personen_raw:
    person_data = []
    for i in person_data_raw:
        if i is None:
            i = ""
        person_data.append(i)
    person = Mensch(person_data[0], person_data[2], person_data[3].split(','), person_data[5].split(','), person_data[4].split(','), person_data[1], person_data[6])
    personen.append(person)
    # print(person.name, person.symptome)
for person in personen:
    person.replace_names_with_objects()
for person in personen:
    person.find_lost_relatives()
for person in personen:
    person.find_out_chromosomes_by_illness()
#     print('Person '+person.name+' hat folgende Wahrscheinlichkeiten zu erkranken: '+str(person.p_erkranken)+' bei folgenden Wahrscheinlichkeiten für die einzelnen Chromosomen: '+str(person.chromosomen))
# print("\n\n------------------------------\n\n")
for person in personen:
    person.find_out_chromosomes_by_relatives()
    person.calc_probability()
    print('Person '+person.name+': \t'+str(person.p_erkranken)+'\t'+str(person.chromosomen))
