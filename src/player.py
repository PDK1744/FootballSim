class Player:
  def __init__(self, name, position, skill_level):
      self.name = name
      self.position = position
      self.skill_level = skill_level

  def __str__(self):
      return f"{self.name} ({self.position}, Skill: {self.skill_level})"
