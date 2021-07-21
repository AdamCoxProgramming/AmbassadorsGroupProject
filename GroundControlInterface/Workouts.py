"""
    Astronauts on the station work out six out of seven days a week for 2.5 hours each day. "
    The International Space Station is equipped with three machines designed to give astronauts that full-body workout:
    a bicycle, a treadmill, and a weightlifting machine called ARED, for Advanced Resistive Exercise Device
"""
options = ["5X Weeks", "6X Weeks", "Everyday"]
specificOptions = ["Cardio workout", "Muscular workout", "none"]
execises = {
    "Exercice 1": ["Bycycle", "Time: 60 minutes"],
    "Exercice 2": ["Treadmill", "Time: 30 minutes"],
    "Exercice 3": ["ARED", "Time: 60 minutes"],
}

exs = [
 {"title": "Bycycle", "time": 360},
{"title": "Treadmill", "time": 30},
{"title": "ARED", "time": 60}
]

currentWorkout = options[0]

ex1 = {"title": "Bycycle", "time": 60}
ex2 = {"title": "Treadmill", "time": 30}
ex3 = {"title": "ARED", "time": 60}