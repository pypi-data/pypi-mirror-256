"""Dependencies"""

import math

"""Damage Calc"""

def pokemon_Damage(Level, Power, Atk, Defense, STAB, Type, Random):
  global pokemon_Damage
  baseDamage = ((2*Level/5+2)*Atk*Power/Defense)/50+2
  pokemon_Damage = math.floor(((baseDamage * STAB * Type * Random)/255))-1
  return pokemon_Damage

# Example
    # pokemon_Damage(50, 85, 100, 100, 1.5, 1, 217)
    # print(pokemon_Damage)

"""Base Powers"""

def pokemon_Power(move):
  global pokemon_Power
  if move == "Body Slam":
    pokemon_Power = 85
  elif move == "Thunderbolt":
    pokemon_Power = 95
  elif move == "Psychic":
    pokemon_Power = 95
  elif move == "Double Edge":
    pokemon_Power = 100
  elif move == "Ice Beam":
    pokemon_Power = 95

# Example
    # pokemon_Power("Double Edge")
    # print(pokemon_Power)

"""Important Movesets"""

def pokemonMovesets(mon, number_Importance):
    if mon == "Tauros":
        if number_Importance == 1:
            return "Body Slam"
        elif number_Importance == 2:
            return "Hyper Beam"
        elif number_Importance == 3:
            return "Earthquake"
        elif number_Importance == 4:
            return "Blizzard"
    elif mon == "Snorlax":
        if number_Importance == 1:
            return "Body Slam"
        elif number_Importance == 2:
            return "Rest"
        elif number_Importance == 3:
            return "Reflect"
        elif number_Importance == 4:
            return "Earthquake"
    elif mon == "Chansey":
        if number_Importance == 1:
            return "Soft Boiled"
        elif number_Importance == 2:
            return "Thunder Wave"
        elif number_Importance == 3:
            return "Ice Beam"
        elif number_Importance == 4:
            return "Thunderbolt"

    



# Example
# pokemonMovesets("Chansey", 1)
# print(pokemon_Movesets)

# Example 2
    # pokemonMovesets("Chansey", 1)
    # print(pokemon_Movesets)
    # pokemon_Movesets = ''
    # pokemonMovesets("Chansey", 2)
    # print(pokemon_Movesets)
    # pokemonMovesets("Chansey", 3)
    # print(pokemon_Movesets)
    # pokemonMovesets("Chansey", 4)
    # print(pokemon_Movesets) # This predicts the moveset of a Chansey

"""Explanations"""

def pokemon_Explain(Thing):
  if Thing == "1/256":
    reuturn "The 1/256 miss is a glitch in Generation 1, that makes all moves have a 1/256 chance of missing. This is most important on 100% accuracy moves, as this makes them only 99.61% accurate"

# Example
    # pokemon_Explain("1/256")