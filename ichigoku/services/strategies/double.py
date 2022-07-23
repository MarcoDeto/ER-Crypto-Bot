def get_double_top(list, filtered, tolerance=5):

   # CERCO IL PRIMO TOP E IL SUO INDICE
   top = max(list)
   filtered.remove(top)
   top_index = list.index(top)
   # CALCOLO IL RANGE DI VALORI PER IL SECONDO TOP
   min_range = top - top * tolerance / 100
   max_range = top + top * tolerance / 100
   # CERCO TUTTI I SECONDI TOP POSSIBILI E LI SALVO
   check_list = get_elemets_in_range(list, min_range, max_range, top_index)

   while len(check_list) > 0:
      second_top = max(check_list, key=lambda x: x['value'])

      # CONTROLLO CHE CI SIA ALMENO UNA VALORE TRA I DUE TOP
      if second_top['index'] > (top_index+1):
         between_list = list[top_index:second_top['index']]
         if (is_min_between(between_list) == True):
            return {'first_top': {'index': top_index, 'value': top}, 'second_top': second_top, }
         else:
            check_list.remove(second_top)

      elif second_top['index'] < (top_index-1):
         between_list = list[second_top['index']:top_index]
         if (is_min_between(between_list) == True):
            return {'first_top': {'index': top_index, 'value': top}, 'second_top': second_top, }
         else:
            check_list.remove(second_top)

      else:
         check_list.remove(second_top)

   return None


def get_double_bottom(list, filtered, tolerance=5):

   # CERCO IL PRIMO BOTTOM E IL SUO INDICE
   bottom = min(list)
   filtered.remove(bottom)
   bottom_index = list.index(bottom)
   # CALCOLO IL RANGE DI VALORI PER IL SECONDO TOP
   min_range = bottom - bottom * tolerance / 100
   max_range = bottom + bottom * tolerance / 100
   # CERCO TUTTI I SECONDI BOTTOM POSSIBILI E LI SALVO
   check_list = get_elemets_in_range(list, min_range, max_range, bottom_index)

   while len(check_list) > 0:
      second_bottom = min(check_list, key=lambda x: x['value'])

      # CONTROLLO CHE CI SIA ALMENO UNA VALORE TRA I DUE BOTTOM
      if second_bottom['index'] > (bottom_index+1):
         between_list = list[bottom_index:second_bottom['index']]
         if (is_max_between(between_list) == True):
            return {'first_bottom': {'index': bottom_index, 'value': bottom}, 'second_bottom': second_bottom, }
         else:
            check_list.remove(second_bottom)

      elif second_bottom['index'] < (bottom_index-1):
         between_list = list[second_bottom['index']:bottom_index]
         if (is_max_between(between_list) == True):
            return {'first_bottom': {'index': bottom_index, 'value': bottom}, 'second_bottom': second_bottom, }
         else:
            check_list.remove(second_bottom)

      else:
         check_list.remove(second_bottom)

   return None


def get_elemets_in_range(list, min_range, max_range, index):
   i = 0
   check_list = []
   for item in list:
      if ((item > min_range or item < max_range) and index != i):
         check_list.append({'index': i, 'value': item})
      i = i + 1
   return check_list


def is_min_between(list):

   min_check = min(list)
   min_check_index = list.index(min_check)
   # CONTROLLO CHE IL MINIMO SIA COMPRESO TRA INIZIO E FINE LISTA
   if (min_check_index != 0 and min_check_index != (len(list)-1)):
      return True

   return False


def is_max_between(list):

   max_check = max(list)
   max_check_index = list.index(max_check)
   # CONTROLLO CHE IL MINIMO SIA COMPRESO TRA INIZIO E FINE LISTA
   if (max_check_index != 0 and max_check_index != (len(list)-1)):
      return True

   return False


