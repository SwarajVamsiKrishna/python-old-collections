from faker import Faker

fake = Faker()

problem_description = fake.sentence(nb_words=10)

print(problem_description)


import random

print(random.choice(['Yes', 'No']))
