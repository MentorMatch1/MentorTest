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
        'Mentee Hobbies': [],
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
        'Mentor Hobbies': [],
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
    'Mentor Hobbies',
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
    'Mentee Hobbies',
    'Mentee Country',
    'Mentee City',
    'Mentee Residence',
]

cohorts = {
    '1st Year Computer Science Tips': 'This seminar provides first-year computer science students with practical advice on how to navigate their introductory courses, manage coding assignments, and utilize resources such as coding labs and online platforms effectively.',
    'Getting Started with Classes': 'A comprehensive guide for all first-year students on how to choose, enroll in, and manage their classes. Topics include understanding prerequisites, balancing course loads, and making the most of lectures and tutorials.',
    'Navigating through University': 'An essential seminar for new students covering campus navigation, understanding university services, accessing academic support, and tips for making a smooth transition from high school to university life.',
    'First Year Neuroscience Tips': 'Focused on first-year neuroscience students, this session offers insights into tackling challenging coursework, understanding complex concepts, and finding study groups and resources specific to neuroscience.',
    'Meeting New People 101': 'This seminar helps students overcome social anxiety, build meaningful connections, and engage in campus activities. Topics include joining clubs, participating in events, and networking with peers and faculty.',
    'First Year Biology Study Guide': 'Aimed at first-year biology students, this guide provides strategies for mastering biological concepts, tips for effective lab work, and advice on utilizing textbooks and online resources for better understanding.',
    'First Year Physics Study Guide': 'This seminar is designed to assist first-year physics students with study techniques for understanding fundamental principles, solving complex problems, and preparing for lab sessions and exams.',
    'First Year Chemistry Study Guide': 'Geared towards first-year chemistry students, this session offers advice on handling chemical equations, laboratory safety, report writing, and effective study methods for chemistry courses.',
    'How to Study in Uni 101': 'A general seminar for all students on developing effective study habits, creating study schedules, using different study techniques, and finding the best study environments to enhance learning.',
    'Mental Health Tips': 'This crucial seminar focuses on maintaining mental well-being during university. Topics include stress management, recognizing signs of mental health issues, seeking help, and utilizing campus mental health resources.',
    'Surviving Exam Season': 'Provides strategies for coping with the pressure of exams, including effective revision techniques, time management during exams, dealing with exam anxiety, and understanding the importance of self-care during exam periods.',
    'Learning Time Management': 'A seminar dedicated to teaching students how to prioritize tasks, manage their time efficiently, and balance academic responsibilities with personal life to ensure a productive and fulfilling university experience.',
}


JUNIOR_MAX = 5



