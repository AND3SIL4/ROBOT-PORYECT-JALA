robot_art = r"""
      0: {head_name}
      Is available: {head_status}
      Attack: {head_attack}                              
      Defense: {head_defense}
      Energy consumption: {head_energy_consump}
              ^
              |                  |1: {weapon_name}
              |                  |Is available: {weapon_status}
     ____     |    ____          |Attack: {weapon_attack}
    |oooo|  ____  |oooo| ------> |Defense: {weapon_defense}
    |oooo| '    ' |oooo|         |Energy consumption: {weapon_energy_consump}
    |oooo|/\_||_/\|oooo|          
    `----' / __ \  `----'           |2: {left_arm_name}
   '/  |#|/\/__\/\|#|  \'           |Is available: {left_arm_status}
   /  \|#|| |/\| ||#|/  \           |Attack: {left_arm_attack}
  / \_/|_|| |/\| ||_|\_/ \          |Defense: {left_arm_defense}
 |_\/    O\=----=/O    \/_|         |Energy consumption: {left_arm_energy_consump}
 <_>      |=\__/=|      <_> ------> |
 <_>      |------|      <_>         |3: {right_arm_name}
 | |   ___|======|___   | |         |Is available: {right_arm_status}
// \\ / |O|======|O| \  //\\        |Attack: {right_arm_attack}
|  |  | |O+------+O| |  |  |        |Defense: {right_arm_defense}
|\/|  \_+/        \+_/  |\/|        |Energy consumption: {right_arm_energy_consump}
\__/  _|||        |||_  \__/        
      | ||        || |          |4: {left_leg_name} 
     [==|]        [|==]         |Is available: {left_leg_status}
     [===]        [===]         |Attack: {left_leg_attack}
      >_<          >_<          |Defense: {left_leg_defense}
     || ||        || ||         |Energy consumption: {left_leg_energy_consump}
     || ||        || || ------> |
     || ||        || ||         |5: {right_leg_name}
   __|\_/|__    __|\_/|__       |Is available: {right_leg_status}
  /___n_n___\  /___n_n___\      |Attack: {right_leg_attack}
                                |Defense: {right_leg_defense}
                                |Energy consumption: {right_leg_energy_consump}
                                
"""

# print(robot_art)

class Part():
  def __init__(self, name: str, attack_level=0, defense_level=0, energy_consumption=0):
    self.name = name
    self.attack_level = attack_level
    self.defense_level = defense_level
    self.energy_consumption = energy_consumption

  def get_status_dict(self):
      formatted_name = self.name.replace(" ", "_").lower()
      return {
        "{}_name".format(formatted_name): self.name.upper(),
        "{}_status".format(formatted_name): self.is_available(),
        "{}_attack".format(formatted_name): self.attack_level,
        "{}_defense".format(formatted_name): self.defense_level,
        "{}_energy_consump".format(formatted_name): self.energy_consumption
      }
  def is_available(self):
    return not self.defense_level <= 0

import random
class Cartas:
  def __init__(self):
    self.listaCartas =  []
    self.cartas = {
        "Aumentar ataque": {"ataque": 10, "defensa": 0, "envenenar": False, "usos": 2},
        "Aumentar defensa": {"ataque": 0, "defensa": 10, "envenenar": False, "usos": 2},
        "Saltar turno": {"ataque": 0, "defensa": 10, "envenenar": False, "usos": 2},
        "Envenenar": {"ataque": -10, "defensa": -5, "envenenar": True, "usos": 2},
        "Invencible": {"ataque": 0, "defensa": 0, "envenenar": False, "usos": 2}
    }
  def eleccionCartas(self):
    return random.choice(list(self.cartas.items()))

  def repartirCartas(self):
    self.carta1 = self.eleccionCartas()
    self.carta2 = self.eleccionCartas()
    while self.carta1[0] == self.carta2[0]:
      self.carta2 = self.eleccionCartas()
    self.listaCartas.append(self.carta1)
    self.listaCartas.append(self.carta2)
    return dict(self.listaCartas)

cartas = Cartas()
carta = cartas.repartirCartas()
print(carta)


colors = {
    "Black": "\x1b[90m",
    "Cyan": "\x1b[94m",
    "Red": "\x1b[91m",
    "White": "\x1b[97m"
}

class Robot:
  def __init__(self, name, color_code, cartas):
    self.name = name
    self.color_code = color_code
    self.energy = 100
    self.parts= [
        Part("Head", attack_level=5, defense_level=10, energy_consumption=5),
        Part("Weapon", attack_level=15, defense_level=0, energy_consumption=10),
        Part("Left arm", attack_level=3, defense_level=20, energy_consumption=10),
        Part("Right arm", attack_level=6, defense_level=20, energy_consumption=10),
        Part("Left leg", attack_level=4, defense_level=20, energy_consumption=15),
        Part("Right leg", attack_level=8, defense_level=20, energy_consumption=15),
    ]
    self.cartas = cartas
    self.card_temp = ""
    
  def greet(self):
    print("Hello, my name is", self.name)

  def print_energy(self):
    print("We have",self.energy,"porcent energy left")

  def attack(self, enemy_robot, part_to_use, part_to_attack, card):
    if card == "Aumentar ataque":
      self.parts[part_to_use].attack_level += self.cartas["Aumentar ataque"]["ataque"]

    elif card == "Envenenar":
      self.parts[part_to_use].attack_level += self.cartas["Envenenar"]["ataque"]
      enemy_robot.parts[part_to_attack].defense_level -= self.cartas["Envenenar"]["defensa"]

    enemy_robot.parts[part_to_attack].defense_level -= self.parts[part_to_use].attack_level

    if card == "Aumentar ataque":
      self.parts[part_to_use].attack_level -= self.cartas["Aumentar ataque"]["ataque"]
      self.cartas["Aumentar ataque"]["usos"] -= 1
      if self.cartas["Aumentar ataque"]["usos"] == 0:
        self.cartas.pop(card)
    elif card == "Envenenar":
      self.parts[part_to_use].attack_level -= self.cartas["Envenenar"]["ataque"]
      enemy_robot.parts[part_to_attack].defense_level += self.cartas["Envenenar"]["defensa"]
      self.cartas[card]["usos"] -= 1
      if self.cartas["Envenenar"]["usos"] == 0:
        self.cartas.pop(card)
    elif card == "Invencible":
      self.card_temp = card
    if self.card_temp == "Invencible":
      enemy_robot.parts[part_to_attack].defense_level += self.parts[part_to_use].attack_level
    
    self.energy -= self.parts[part_to_use].energy_consumption

  def is_on(self):
    return self.energy >= 0

  def is_there_available_parts(self):
    for part in self.parts:
      if part.is_available():
        return True
    return False
  def print_status(self):
    print(self.color_code)
    str_robot = robot_art.format(**self.get_part_status())
    self.greet()
    self.print_energy()
    print(str_robot)
    print(colors["Black"])

  def get_part_status(self):
    part_status = {}
    for part in self.parts:
      status_dict = part.get_status_dict()
      part_status.update(status_dict)
    return part_status

def play():
  playing = True
  print("Welcome to the game")
  cartas1 = Cartas()
  cartas2 = Cartas()
  robot_one = Robot("Jarvis", colors["Cyan"], cartas1.repartirCartas())
  robot_two = Robot("Optimus", colors["Black"], cartas2.repartirCartas())
  round = 0
  card = ""
  while playing:
    if round % 2 == 0:
      current_robot = robot_one
      enemy_robot = robot_two
    else:
      current_robot = robot_two
      enemy_robot = robot_one
    current_robot.print_status()
    print(f"Turno del jugador {round % 2}") 
    use_card = input("Do you want to use one of your cards?: (yes/no) ")
    if bool(current_robot.cartas):
      if use_card == "yes":
        print(current_robot.cartas) 
        card = input("What card do you want to use?: ")
        # print(current_robot.cartas["Saltar turno"]["usos"])
      else:
        pass
    else:
      print("You dont have cards available!")
      pass

    if card == "Saltar turno":
      if "Saltar turno" in current_robot.cartas:
        if current_robot.cartas["Saltar turno"]["usos"] == 1:
          print("La carta Saltar turno ya no esta disponible")
          current_robot.cartas.pop(card)
          round += 1
        else:
          print("Usaste saltar turno")
          current_robot.cartas[card]["usos"] -= 1
          round += 2

    elif card == "Invencible":
      print("Se anula el daño del siguiente ataque")
      round += 1

    elif card == "Envenenar":
      print("Robot enemigo envenenado")
      round += 1
    
    elif card == "Aumentar ataque":
      print("Ataque incementado con exito...")
      round += 1

    elif card == "Aumentar defensa":
      print("Desfensa aumentada ! ")
      round += 1
    
    print("What part should I use to attack?")
    part_to_use = int(input("Chooise a number part: "))

    enemy_robot.print_status()
    print("Which part of the enemy should we attack?") 
    part_to_attack = int(input("Chooise a number part: "))
    print(round)


    current_robot.attack(enemy_robot, part_to_use, part_to_attack, card)
    if card == card:
      print(f"Jugador {round % 2} usaste exitosamente la carta de: {card}")
    

    if not enemy_robot.is_on() or enemy_robot.is_there_available_parts() == False:
      playing = False
      print("Congratulation; you won")
      print(current_robot.name)
play()

