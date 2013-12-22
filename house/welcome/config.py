visits = 0
def chooser():
  global visits
  if visits < 1:
    visits += 1
    return 'map'
  elif visits == 1:
    visits = 0
    return 'map2'