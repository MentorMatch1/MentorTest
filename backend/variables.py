compatibility_scores = {
    'Math': {
        'Math': 1.0,
        'Physics': 0.8,
        'Chemistry': 0.6,
        'Biology': 0.5,
        'Computer Science': 0.9,
        'Engineering': 0.7,
        'Psychology': 0.4,
        'Pharmacology': 0.4,
        'Kinesiology': 0.3,
        'Astrophysics': 0.8,
        'Neuroscience': 0.5
    },
    'Physics': {
        'Math': 0.8,
        'Physics': 1.0,
        'Chemistry': 0.7,
        'Biology': 0.5,
        'Computer Science': 0.7,
        'Engineering': 0.9,
        'Psychology': 0.3,
        'Pharmacology': 0.4,
        'Kinesiology': 0.2,
        'Astrophysics': 1.0,
        'Neuroscience': 0.5
    },
    'Chemistry': {
        'Math': 0.6,
        'Physics': 0.7,
        'Chemistry': 1.0,
        'Biology': 0.8,
        'Computer Science': 0.5,
        'Engineering': 0.7,
        'Psychology': 0.4,
        'Pharmacology': 0.9,
        'Kinesiology': 0.3,
        'Astrophysics': 0.6,
        'Neuroscience': 0.6
    },
    'Biology': {
        'Math': 0.5,
        'Physics': 0.5,
        'Chemistry': 0.8,
        'Biology': 1.0,
        'Computer Science': 0.4,
        'Engineering': 0.5,
        'Psychology': 0.7,
        'Pharmacology': 0.8,
        'Kinesiology': 0.6,
        'Astrophysics': 0.5,
        'Neuroscience': 0.9
    },
    'Computer Science': {
        'Math': 0.9,
        'Physics': 0.7,
        'Chemistry': 0.5,
        'Biology': 0.4,
        'Computer Science': 1.0,
        'Engineering': 0.8,
        'Psychology': 0.3,
        'Pharmacology': 0.3,
        'Kinesiology': 0.2,
        'Astrophysics': 0.7,
        'Neuroscience': 0.4
    },
    'Engineering': {
        'Math': 0.7,
        'Physics': 0.9,
        'Chemistry': 0.7,
        'Biology': 0.5,
        'Computer Science': 0.8,
        'Engineering': 1.0,
        'Psychology': 0.3,
        'Pharmacology': 0.5,
        'Kinesiology': 0.3,
        'Astrophysics': 0.8,
        'Neuroscience': 0.4
    },
    'Psychology': {
        'Math': 0.4,
        'Physics': 0.3,
        'Chemistry': 0.4,
        'Biology': 0.7,
        'Computer Science': 0.3,
        'Engineering': 0.3,
        'Psychology': 1.0,
        'Pharmacology': 0.5,
        'Kinesiology': 0.6,
        'Astrophysics': 0.2,
        'Neuroscience': 0.8
    },
    'Pharmacology': {
        'Math': 0.4,
        'Physics': 0.4,
        'Chemistry': 0.9,
        'Biology': 0.8,
        'Computer Science': 0.3,
        'Engineering': 0.5,
        'Psychology': 0.5,
        'Pharmacology': 1.0,
        'Kinesiology': 0.4,
        'Astrophysics': 0.3,
        'Neuroscience': 0.7
    },
    'Kinesiology': {
        'Math': 0.3,
        'Physics': 0.2,
        'Chemistry': 0.3,
        'Biology': 0.6,
        'Computer Science': 0.2,
        'Engineering': 0.3,
        'Psychology': 0.6,
        'Pharmacology': 0.4,
        'Kinesiology': 1.0,
        'Astrophysics': 0.1,
        'Neuroscience': 0.7
    },
    'Astrophysics': {
        'Math': 0.8,
        'Physics': 1.0,
        'Chemistry': 0.6,
        'Biology': 0.5,
        'Computer Science': 0.7,
        'Engineering': 0.8,
        'Psychology': 0.2,
        'Pharmacology': 0.3,
        'Kinesiology': 0.1,
        'Astrophysics': 1.0,
        'Neuroscience': 0.4
    },
    'Neuroscience': {
        'Math': 0.5,
        'Physics': 0.5,
        'Chemistry': 0.6,
        'Biology': 0.9,
        'Computer Science': 0.4,
        'Engineering': 0.4,
        'Psychology': 0.8,
        'Pharmacology': 0.7,
        'Kinesiology': 0.7,
        'Astrophysics': 0.4,
        'Neuroscience': 1.0
    }
}


matched_format = {
        'Mentee ID': [],
        'Mentee Firstname': [],
        'Mentee Lastname': [],
        'Mentee Email': [],
        'Mentee Program': [],
        'Mentee Interests': [],
        'Mentee Country': [],
        'Mentee City': [],
        'Mentee Residence': [],
        'Mentor ID': [],
        'Mentor Role': [],
        'Mentor Firstname': [],
        'Mentor Lastname': [],
        'Mentor Email': [],
        'Mentor Program': [],
        'Mentor Interests': [],
        'Mentor Country': [],
        'Mentor City': [],
        'Mentor Residence': [],
        'Score': []
    }

mentor_vars  = [
    'Mentor ID',
    'Mentor Role',
    'Mentor Firstname',
    'Mentor Lastname',
    'Mentor Email',
    'Mentor Program',
    'Mentor Interests',
    'Mentor Country',
    'Mentor City',
    'Mentor Residence',
]

mentee_vars  = [
    'Mentee ID',
    'Mentee Firstname',
    'Mentee Lastname',
    'Mentee Email',
    'Mentee Program',
    'Mentee Interests',
    'Mentee Country',
    'Mentee City',
    'Mentee Residence',
]

JUNIOR_MAX = 4
SENIOR_MAX = 6
