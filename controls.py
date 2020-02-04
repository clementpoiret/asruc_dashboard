# Controls for webapp

# Timeframe
TIME_FRAME_VALUES = dict(SHORT=0, MEDIUM=7, LONG=31)
TIME_FRAME_NAMES = dict(SHORT="Dernier Entraînement",
                        MEDIUM="7 jours",
                        LONG="31 jours")

# POPULATION
POPULATION = dict(ALL="Tout", AV="Avants", AR="Arrières")

# DPZV
DPZV = dict(DPZV0e6="0-6km/h",
            DPZV6e14="6-14km/h",
            DPZV14e19="14-19km/h",
            DPZV19e24="19-24km/h",
            DPZV24e40="24-40km/h")

# TZFC
TZFC = dict(Tzfc0e70="0-70bpm",
            Tzfc70e110="70e110bpm",
            Tzfc110e150="110-150bpm",
            Tzfc150e180="150-180bpm",
            Tzfc180e250="180-250bpm")

# Pretty Column Names
COLNAMES = [
    "Nom", "Date", "LapTime", "Distance", "mmin", "Vmoy", "Vmax", "Fcmoy",
    "Fcmin", "Fcmax", "DPZV0e6", "DPZV6e14", "DPZV14e19", "DPZV19e24",
    "DPZV24e40", "Tzfc70e110", "Tzfc0e70", "Tzfc150e180", "Tzfc110e150",
    "Tzfc180e250", "Sprints", "RrHfMoy", "RrBfMoy", "HfBfMoy", "Power"
]

PRETTY_COLNAMES = [
    "Nom", "Date", "LapTime", "Distance", "m/min", "Vitesse Moyenne",
    "Vitesse Maximale", "MC Moyenne", "FC Minimale", "FC Maximale",
    "DPZV 0-6Kmh", "DPZV 6-14Kmh", "DPZV 14-19Kmh", "DPZV 19-24Kmh",
    "DPZV 24-40Kmh", "TZFC 70-110s", "TZFC 0-70s", "TZFC 150-180s",
    "TZFC 110-150s", "TZFC 180-250s", "Sprints", "Variabilité Haute Fréquence",
    "Variabilité Basse Fréquence", "Rapport Haute/Basse Fréquence", "Puissance"
]
