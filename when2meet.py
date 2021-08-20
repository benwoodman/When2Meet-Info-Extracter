import datetime

def setup():
    """Load info from files into script"""

    names_and_ids_input = open('./input/names.txt', 'r').read()
    names_and_ids = names_and_ids_input.split(';')
    ids_dict = {}

    for i in range(0, len(names_and_ids), 2):
        name = names_and_ids[i][names_and_ids[i].find("'") + 1:-1]
        id = names_and_ids[i + 1][names_and_ids[i + 1].find('=') + 2:]
        ids_dict[id] = name

    times_input = open('./input/times.txt', 'r').read().split('\n')
    times = {}

    for i in range(0, len(times_input), 2):
        id = times_input[i][times_input[i].find('[') + 1:times_input[i].find(']')]
        t = datetime.datetime.fromtimestamp(int(times_input[i][times_input[i].find('=') + 1:-1])).strftime('%A %H:%M')
        times[id] = t

    availability = {str(k): [] for k in range(420)}
    availability_arr = open('./input/availability.txt', 'r').read().split('\n')

    for a in availability_arr:
        slot = a[a.find('[') + 1:a.find(']')]
        user = a[a.find('(') + 1:a.find(')')]
        availability[slot].append(user)

    return ids_dict, times, availability

def get_counts(availability, times):
    """Get counts of available students per time"""
    counts = {times[k]: len(availability[k]) for k in availability.keys()}
    return counts

def dict_to_csv(d, file):
    """Convert from Python dict to csv file and save"""
    f = open(file, 'w')
    out = ''
    for k, v in d.items():
        out += str(k) + ';' + str(v) + '\n'
    f.write(out)

def test_times(using_times, ids_dict, times, availability):
    """Returns a list of students that are not satisfied by the current time"""
    all_ids = [id for id in ids_dict.keys()]
    for t in using_times:
        students_avail = availability[t]
        for s in students_avail:
            if str(s) in all_ids:
                all_ids.remove(str(s))
    
    return [ids_dict[s] for s in all_ids]

def person_with_avail(availability, ids_dict, times):
    """Gets indv availability for indv person"""
    students = {s: [] for s in ids_dict.keys()}
    for k, v in availability.items():
        for s in v:
            students[s].append(k)
    students_w_names = {ids_dict[k]: [times[t] for t in v] for k, v in students.items()}
    return students_w_names

# Setup
ids_dict, times, availability = setup()

# Save to csv
dict_to_csv(ids_dict, './output/ids.csv')
dict_to_csv(get_counts(availability, times), './output/time_counts.csv')
dict_to_csv({k: [ids_dict[s] for s in v] for k, v in availability.items()}, './output/avail_per_time.csv')
dict_to_csv(person_with_avail(availability, ids_dict, times), './output/student_avail.csv')
dict_to_csv(times, './output/times_table.csv')

# Time times here, you can view the times_table for a key value
using_times = ['7', '8', '9']
print(test_times(using_times, ids_dict, times, availability))

