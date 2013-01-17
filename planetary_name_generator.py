from random import randint


def generate_name():
    r = randint(1, 100)

    if(r <= 10):
        name = "%s %s" % (get_name(), get_number())

    elif(r > 10 and r <= 20):
        name = "%s %s" % (get_number(), get_name())

    elif(r > 20 and r <= 30):
        name = "%s-%s %s" % (get_name(), get_name(), get_number())

    elif(r > 30 and r <= 40):
        name = "%s %s-%s" % (get_number(), get_name(), get_name())

    elif(r > 40 and r <= 50):
        name = "%s %s %s" % (get_name(), get_letter(), get_number())

    elif(r > 50 and r <= 60):
        name = "%s %s %s" % (get_number(), get_name(), get_letter())

    elif(r > 60 and r <= 70):
        name = "%s-%s %s" % (get_number(), get_letter(), get_name())

    elif(r > 70 and r <= 80):
        name = "%s %s-%s" % (get_name(), get_letter(), get_number())

    elif(r > 80 and r <= 90):
        name = "%s-%s %s" % (get_name(), get_letter(), get_number())

    elif(r > 90 and r <= 100):
        name = "%s-%s %s" % (get_letter(), get_number(), get_name())

    return name


def get_number():
    return str(randint(5, 1000))


def get_name():
    return names[randint(0, (len(names) - 1))]

def get_letter():
    letters = "ABCDEFGXZ"
    letter = letters[randint(0, (len(letters) - 1))]

    if randint(0, 1):
        letter = letter.lower()

    return letter


names = [
    "Newton",
    "Harriot",
    "Galilei",
    "Napier",
    "Leibniz",
    "Boyle",
    "Raphson",
    "Servetus",
    "Galti",
    "al-Nafis",
    "Copernicus",
    "Macleod",
    "HD",
    "Gliese",
    "Cha",
    "NN",
    "Librae",
    "Andromedae",
    "Sextantis",
    "Herculis",
    "Leonis",
    "Virginis",
    "Cancri",
    "PLA",
]
