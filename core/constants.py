"""Constantes centralizadas de la aplicación."""

# Nombres de clases del modelo (en inglés, ordenados)
CLASS_NAMES = [
    'Ant', 'Armadillo', 'Bat', 'Bear', 'Beatle', 'Bee', 'Butterfly', 'Cat',
    'Centipede', 'Cheetah', 'Crab', 'Crocodile', 'Deer', 'Dog', 'Dolphin',
    'Dragonfly', 'Duck', 'Eagle', 'Elephant', 'Falcon', 'Fox', 'Frog',
    'Giraffe', 'Goat', 'Goldfish', 'Harbor_seal', 'Hedgehog',
    'Hippopotamus', 'Horse', 'Jaguar', 'Jellyfish', 'Kangaroo', 'Koala',
    'Ladybug', 'Leopard', 'Lion', 'Lizard', 'Lobster', 'Mallard', 'Monkey',
    'Mouse', 'Otter', 'Owl', 'Oyster', 'Panda', 'Parrot', 'Pig',
    'Porcupine', 'Rabbit', 'Rhinoceros', 'Seahorse', 'Shark', 'Sheep',
    'Shrimp', 'Snake', 'Spider', 'Squid', 'Squirrel', 'Starfish', 'Swan',
    'Tick', 'Tiger', 'Turtle', 'Whale', 'Woodpecker', 'Worm', 'Zebra'
]

# Umbral de confianza para predicciones
CONFIDENCE_THRESHOLD = 0.90

# Tamaño de ventana principal
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 800

# Tamaño de imagen para el modelo
MODEL_IMAGE_SIZE = (224, 224)

