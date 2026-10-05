from machine import ADC, Pin, PWM
from utime import sleep_ms


# Grove Shield pour Raspberry Pi Pico:
# A0 = ADC(0) = GP26
# A1 = GP27
potentiometre = ADC(0)
buzzer = PWM(Pin(27))

# Pour un buzzer passif, le son est le plus propre avec un duty-cycle
# qui reste entre 0 % et environ 50 %.
DUTY_MAX = 32768
VOLUME_MIN = 800
LECTURE_VOLUME_MS = 20
PAUSE_ENTRE_NOTES_MS = 30


def volume():
    valeur = potentiometre.read_u16()

    # Petite zone morte pour pouvoir couper le son quand le potentiometre
    # est tourne presque au minimum.
    if valeur < VOLUME_MIN:
        return 0

    return int(valeur * DUTY_MAX / 65535)


def attendre_en_actualisant_volume(duree_ms):
    temps_restant = duree_ms

    while temps_restant > 0:
        buzzer.duty_u16(volume())
        attente = min(LECTURE_VOLUME_MS, temps_restant)
        sleep_ms(attente)
        temps_restant -= attente


def jouer_note(frequence, duree_ms):
    if frequence == 0:
        buzzer.duty_u16(0)
        sleep_ms(duree_ms)
        return

    buzzer.freq(frequence)
    attendre_en_actualisant_volume(duree_ms)
    buzzer.duty_u16(0)
    sleep_ms(PAUSE_ENTRE_NOTES_MS)


# Melodie: Frere Jacques / Two Tigers.
DO = 262
RE = 294
MI = 330
FA = 349
SOL = 392
LA = 440
SILENCE = 0

melodie = [
    (DO, 350), (RE, 350), (MI, 350), (DO, 350),
    (DO, 350), (RE, 350), (MI, 350), (DO, 350),
    (MI, 350), (FA, 350), (SOL, 700),
    (MI, 350), (FA, 350), (SOL, 700),
    (SOL, 250), (LA, 250), (SOL, 250), (FA, 250), (MI, 350), (DO, 350),
    (SOL, 250), (LA, 250), (SOL, 250), (FA, 250), (MI, 350), (DO, 350),
    (DO, 350), (SOL, 350), (DO, 700),
    (DO, 350), (SOL, 350), (DO, 700),
    (SILENCE, 500),
]


try:
    while True:
        for frequence, duree in melodie:
            jouer_note(frequence, duree)
finally:
    buzzer.duty_u16(0)
    buzzer.deinit()
