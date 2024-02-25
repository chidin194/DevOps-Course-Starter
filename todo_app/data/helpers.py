import os


def map_list_id_to_status(list_id):
  if list_id == os.getenv('TO_DO_LIST_ID'):
      return 'To Do'
  elif list_id == os.getenv('DOING_LIST_ID'):
      return 'Doing'
  elif list_id == os.getenv('DONE_LIST_ID'):
      return 'Done'