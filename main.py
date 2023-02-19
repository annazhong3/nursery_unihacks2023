# this file generates patient data and nurse availability, then matches nurses with patients based on this algorithm

# imports
import random
import names
import pandas as pd

# we will generate 100 rows of patient data
rows = 100

# name data

patient_names = []

for i in range(rows):
  name = names.get_full_name()
  patient_names.append(name)

# disease data

# our data (from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2815281/)
diseases_dict = {
  # "cause": "percent of hospitalizations"
  "Pneumonia": 20.96,
  "Asthma": 9.58,
  "Infectious diarrhea and gastroenteritis": 3.40,
  "Other hernias": 3.25,
  "Inguinal hernias": 3.19,
  "Phimosis": 2.86,
  "Infections of skin and subcutaneous tissues": 2.42,
  "Chronic diseases of the tonsils and adenoids": 2.20,
  "Congenital malformations of the circulatory system": 2.05,
  "Other diseases of the nervous system": 1.86
}
# these are the top ten main causes of child hospitalization in São Paulo, from 2002 to 2006

# separate into lists of disease names and weights (probabilities)
disease_names = diseases_dict.keys()
disease_names = list(disease_names)

disease_weights = diseases_dict.values()
disease_weights = list(disease_weights)

# based on this list of diseases and proability values, we will create a list of 100 diseases for our new dataset
diseases = random.choices(disease_names, weights=(disease_weights), k=rows)
# print(diseases)

# hospital room data

rooms = []  # store our new data here

wings = ["5L", "5R", "6L",
         "6R"]  # assume there are left and right wings on floor 5 and 6
for wing in wings:
  for i in range(1, 26):
    i = str(i)
    room = wing + i
    rooms.append(room)  # in each wing, there are 25 rooms

# patient schedule data
all_patient_schedules = []

# possible tasks
activities = [
  "medicine", "IV", "prepare for surgery", "feed meal", "fun activity",
  "casual check-in chat"
]

# creates a 24-hour empty schedule
for i in range(rows):
  schedule = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]  # 24 empty time slots

  #fills schedule with a random activity for each time slot
  for i in range(0, 2):
    rand_index = random.randint(0, len(schedule) - 1)
    if schedule[rand_index] == "":
      schedule[rand_index] = random.choice(activities)

  all_patient_schedules.append(schedule)

# using all data generated previously, combine into our new dataset

patient_data = pd.DataFrame({
  'Name': patient_names,
  'Condition': diseases,
  'Room': rooms,
  'Schedule': all_patient_schedules
})

# displaying the DataFrame
print(patient_data)


# create nurse data

# nurse name data
num_nurses = 8
nurse_names = []

for i in range(rows, rows+num_nurses): # every name up to rows = 100 was used for patients
  name = names.get_full_name()
  nurse_names.append(name)

# nurse station location data
# we will assume there is a nurse station at the center of each hall

nurse_stations = []

for i in range(num_nurses):
  if i in range(0, num_nurses//4):
    nurse_stations.append("Station 5L")
  elif i in range(num_nurses//4, num_nurses//2):
    nurse_stations.append("Station 5R")
  elif i in range(num_nurses//2, 3*num_nurses//4):
    nurse_stations.append("Station 6L")
  else:
    nurse_stations.append("Station 6R")

# creating nurse schedules
all_nurse_schedules = []
all_patient_schedules2 = all_patient_schedules.copy()
for i in range(num_nurses):
  schedule = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]  # 24 empty time slots
  for j in range(len(all_patient_schedules2)): # gets individual patient schedules
    nurse = nurse_stations[i]
    patient_schedule = all_patient_schedules2[j]
    
    room = rooms[j]
    if room[:2] in nurse: # if the patient is in the nurses area
      for w in range(len(patient_schedule)): 
        if (patient_schedule[w] != "") and (schedule[w] == ""): # if patient has an activity and nurse schedule is empty
          schedule[w] = f"{patient_schedule[w]} with patient {patient_names[j]}" 
          patient_schedule[w] = "" 


  all_nurse_schedules.append(schedule)


#prints nurse schedules
for i in range(len(all_nurse_schedules)):
  print(f"Nurse {i+1}: {all_nurse_schedules[i]}")
  print()
  
