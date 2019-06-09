from faker import Faker
from faker.providers import BaseProvider

import random, string

fake = Faker()

class CustomFaker(BaseProvider):

    def alphanumeric(self, length=20):
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))

    def industry(self):
        industries = ['automobile', 'education', 'health', 'information technology', 'banking', 'agriculture']
        return industries[random.randint(0,len(industries) - 1)]

fake.add_provider(CustomFaker)