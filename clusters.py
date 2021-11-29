from numpy.random import choice, normal, randint
import pandas as pd
from faker import Faker

Faker.seed(27)
fake = Faker('en_US')

#############################


#
focused_tech = dict(
    business_size={
        'value':40,
        'std':10,
    },
    spent_past_year={
        'value': 30_000,
        'std': 5_000,
    },
    state=None,
    industry=[
        ('technology',1)
    ],
    closest_convenience_store={
        'value':5,
        'std':0.5,
    },
    provides_lunch=[
        (False, 0.2),
        (True, 0.8),
    ],
    # Person
    age_median={
        'value':29,
        'std':3,
    },
    education_average=[
        ('High School', 0.1),
        ('College', 0.7),
        ('Grad School', 0.2),
    ],
    # Unnecessary
    phone_number=None,
)

isolated_office = dict(
    business_size={
        'value':50,
        'std':15,
    },
    spent_past_year={
        'value':20_000,
        'std':6_000,
    },
    state=None,
    industry=[
        ('technology',2/26),
        ('education',2/26),
        ('agriculture',1/26),
        ('construction',1/26),
        ('entertainment',1/26),
        ('real_estate',4/26),
        ('healthcare',4/26),
        ('administration',4/26),
        ('retail',4/26),
        ('manufacturing',1/26),
        ('transportation',1/26),
        ('warehousing',1/26),
    ],
    closest_convenience_store={
        'value':10,
        'std':1,
    },
    provides_lunch=[
        (False, 0.8),
        (True, 0.2)
    ],
    # Person
    age_median={
        'value':40,
        'std':6,
    },
    education_average=[
        ('High School', 0.1),
        ('College', 0.6),
        ('Grad School', 0.3),
    ],
    # Unnecessary
    phone_number=None,
)

blue_collars = dict(
    business_size={
        'value':150,
        'std':25,
    },
    spent_past_year={
        'value':15_000,
        'std':2_000,
    },
    state=None,
    industry=[
        ('education',1/25),
        ('agriculture',4/25),
        ('construction',4/25),
        ('entertainment',1/25),
        ('administration',1/25),
        ('retail',2/25),
        ('manufacturing',4/25),
        ('transportation',4/25),
        ('warehousing',4/25),
    ],
    closest_convenience_store={
        'value':5,
        'std':1,
    },
    provides_lunch=[
        (False, 0.9),
        (True, 0.1)
    ],
    # Person
    age_median={
        'value':35,
        'std':8,
    },
    education_average=[
        ('High School', 0.4),
        ('College', 0.5),
        ('Grad School', 0.1),
    ],
    # Unnecessary
    phone_number=None,
)

active_workers = dict(
    business_size={
        'value':20,
        'std':2,
    },
    spent_past_year={
        'value':8_000,
        'std':1_000,
    },
    state=None,
    industry=[
        ('education',1/19),
        ('agriculture',3/19),
        ('construction',1/19),
        ('entertainment',2/19),
        ('healthcare',4/19),
        ('retail',5/19),
        ('transportation',1/19),
        ('warehousing',2/19),
    ],
    closest_convenience_store={
        'value':3,
        'std':0.4,
    },
    provides_lunch=[
        (False, 0.6),
        (True, 0.4)
    ],
    # Person
    age_median={
        'value':32,
        'std':6,
    },
    education_average=[
        ('High School', 0.4),
        ('College', 0.5),
        ('Grad School', 0.1),
    ],
    # Unnecessary
    phone_number=None,
)



businesses = {
    'focused_tech': (focused_tech, 100),
    'isolated_office': (isolated_office, 250),
    'blue_collars': (blue_collars, 100),
    'active_workers': (active_workers, 250),
}

####


##### Business Details ######
# Generate fake phone number
def generate_fake_phone():
    first = str(randint(100,999))
    second = str(randint(1,888)).zfill(3)

    last = (str(randint(1,9998)).zfill(4))
    while last in ['1111','2222','3333','4444','5555','6666','7777','8888']:
        last = (str(randint(1,9998)).zfill(4))

    return '{}-{}-{}'.format(first,second, last)

def generate_data(centers, size=1):
    data_point = {}
    for key,data in centers.items():
        if data is None:
            # TODO: Random Choice
            if key == 'phone_number':
                data_point[key] = generate_fake_phone()
            elif key == 'state':
                data_point[key] = fake.state_abbr()
            else:
                data_point[key] = [None]*size
        elif type(data) is list:
            a, p = zip(*data)
            data_point[key] = choice(
                                a=a,
                                size=size,
                                p=p,
            )
        elif type(data) is dict:
            data_point[key] = normal(
                                loc=data['value'],
                                scale=data['std'],
                                size=size,
            )
    return data_point


####
dfs = []
for business_name, business in businesses.items():
    center, n_examples = business
    temp = generate_data(center, size=n_examples)
    df_temp = pd.DataFrame(temp)
    df_temp.to_csv(f'{business_name}.csv', index=False)
    dfs.append(df_temp)

df = pd.concat(dfs)

df.to_csv('final.csv', index=False)
