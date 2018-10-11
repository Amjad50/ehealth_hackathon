data = {

    'all': {
        # what do i do when someone is having seizure
        'what do seizure': '1. stay calm with the person until the seizure is over \n'
                           '2. remove any nearby sharp object and steer the person to a safe place \n'
                           '3. make the person as comfortable as possible \n'
                           '4. alert us if the seizure last for more than 5 minutes.',
        # can i die from epilepsy
        'can die epilepsy': 'it’s rare but unfortunately people can die from epilepsy.',
        # can someone swallow their tongue during a seizure?
        'can swallow tongue seizure': 'no, it’s physically impossible to swallow your tongue.',
        # can i give water during seizure
        'can give water seizure': 'never, it is dangerous and has high risk of choking',

        # i need to travel overseas
        'travel overseas': 'ensure that you take your medication regularly, adequate sleep and avoid exhaustion',
    },
    'any': {
        # are seizures painful or dangerous?
        'painful dangerous': 'seizures usually aren’t painful; however, there are some people who could feel pain when one happens.',

        # i have side effect (vomit etc) after taking new medication what should i do?
        'what side effect vomit after new medication': 'you may reduce your medication to previous dose and observe. inform us if problem persist. if u develop allergy and rashes please stop medication and consult ur doctor',

        # emotional support
        # anxiety
        'worried worry panic': 'emotional support 1',
        # depression
        'sad suicide die life tired living': 'emotional support 2',
    },
    'depression': [
        'sad suicide die life tired living'
    ],

    'qa': {

        # my seizure frequency has increased in the past one week
        'seizure frequency increased': ('do u have any trigger (inadequate sleep ,fever etc)?', {
            1: 'it may be caused by the trigger continue same dose of medication and observe',
            0: 'it indicate that seizure is not controlled and might need higher dose of medication. please consult the doctor',
        }),

        # i have cluster (many) of seizures in one day.
        'cluster many seizure one 1 day': ('did you miss your medication?', {
            1: 'please resume your medication at the same dose or consult the doctor if seizure persist',
            0: 'if you have more than 2 seizure in a day please go to emergency',

        }),
    }
}

extra_data = ['it may be caused by the trigger continue same dose of medication and observe',
              'it indicate that seizure is not controlled and might need higher dose of medication. please consult the doctor',
              'please resume your medication at the same dose or consult the doctor if seizure persist',
              'if you have more than 2 seizure in a day please go to emergency']
