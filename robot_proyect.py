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

class Part: 
  def __init__ (self, name, attack_level, defense_level, energy_consump):
    self.name = name
    self.attack_level = attack_level
    self.defense_level = defense_level
    self.energy_consump = energy_consump

  def get_status_dict(self):
    formatted_name = self.name.replace(" ","_").lower()
    return{       
        "{}_name".format(formatted_name): self.name.lower(),
        "{}_status".format(formatted_name): self.is_available(),
        "{}_attack".format(formatted_name): self.attack_level,
        "{}_defense".format(formatted_name): self.defense_level,
        "{}_energy_consump".format(formatted_name): self.energy_consump,
    }
  def is_available(self):
    return not self.defense_level <= 0
  
colors = {
    "Black": '\x1b[90m',
    "Blue": '\x1b[94m',
    "Cyan": '\x1b[96m',
    "Green": '\x1b[92m',
    "Magenta": '\x1b[95m',
    "Red": '\x1b[91m',
    "White": '\x1b[97m',
    "Yellow": '\x1b[93m',
}

class Robot:
  def __init__(self, name, color_code): 
    self.name = name
    self.color_code = color_code
    self.energy = 100
    self.parts = [
        Part("HEAD", attack_level=50, defense_level=10, energy_consump=10),
        Part("WEAPON", attack_level=90, defense_level=80, energy_consump=30),
        Part("LEFT_ARM", attack_level=50, defense_level=10, energy_consump=10),
        Part("RIGHT_ARM", attack_level=50, defense_level=10, energy_consump=10),
        Part("LEFT_LEG", attack_level=40, defense_level=10, energy_consump=10),
        Part("RIGHT_LEG", attack_level=40, defense_level=10, energy_consump=10),
    ]

  def greet(self): 
    print("My name is: ", self.name.capitalize())

  def print_energy(self):
    print(f"My energy is: {self.energy} percent energy left")
  
  def print_color_code(self):
    print("My color code is: ", self.color_code.lower())

  def attack(self, enemy_robot, part_to_use, part_to_attack):
    enemy_robot.parts[part_to_attack].defense_level -= self.parts[part_to_use].attack_level
    self.energy -= self.parts[part_to_use].energy_consump

  def is_on(self):
    return self.energy >= 0
  
  def is_there_available_parts(self):
    for part in self.parts:
      if part.is_available():
        return True
    return False

  def print_status(self):
    print(self.color_code)
    print(self.get_part_status())
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
  print("Welcome to the game...")
  robot_one = Robot("Janeth", colors["Cyan"])
  robot_two = Robot("Robotina", colors["Red"])
  round = 0
  while playing:
    if round % 2 == 0:
      current_robot = robot_one
      enemy_robot = robot_two
    else:
      current_robot = robot_two
      enemy_robot = robot_one
    current_robot.print_status()
    print("What part should I use to attack?")
    part_to_use = int(input("Choose a number part: "))

    enemy_robot.print_status()
    print("What part of enemy shoud to attack?")
    part_to_attack = int(input("Choose a part enemy to attack: "))

    current_robot.attack(enemy_robot, part_to_use, part_to_attack)
    round += 1

    if not enemy_robot.is_on() or enemy_robot.is_there_available_parts() == False:
      playing = False
      print("Congratulations you won!")
      print(current_robot.name)
play()