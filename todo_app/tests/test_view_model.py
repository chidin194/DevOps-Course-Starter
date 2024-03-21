from todo_app.view_models.ViewModel import ViewModel


def test_done_items():
  # Arrange
  view_model = ViewModel([{"title": "Walk the dog", "status": "To Do", "id": "139fhiwg"}, 
                          {"title": "Go shopping", "status": "Doing", "id": "12jf0wrjgp"}, 
                          {"title": "Book doctor's appointment", "status": "Done", "id": "2u039hfo"}])
  
  # Act
  result = view_model.done_items

  # Assert
  assert len(result) == 1
  assert result[0]['status'] == 'Done'
  assert result[0]['id'] == '2u039hfo'
  assert result[0]['title'] == "Book doctor's appointment"

def test_doing_items():
  # Arrange
  view_model = ViewModel([{"title": "Walk the dog", "status": "To Do", "id": "139fhiwg"}, 
                          {"title": "Go shopping", "status": "Doing", "id": "12jf0wrjgp"}, 
                          {"title": "Book doctor's appointment", "status": "Done", "id": "2u039hfo"}])
  
  # Act
  result = view_model.doing_items

  # Assert
  assert len(result) == 1
  assert result[0]['status'] == 'Doing'
  assert result[0]['id'] == '12jf0wrjgp'
  assert result[0]['title'] == 'Go shopping'

def test_to_do_items():
  # Arrange
  view_model = ViewModel([{"title": "Walk the dog", "status": "To Do", "id": "139fhiwg"}, 
                          {"title": "Go shopping", "status": "Doing", "id": "12jf0wrjgp"}, 
                          {"title": "Book doctor's appointment", "status": "Done", "id": "2u039hfo"}])
  
  # Act
  result = view_model.to_do_items

  # Assert
  assert len(result) == 1
  assert result[0]['status'] == 'To Do'
  assert result[0]['id'] == '139fhiwg'
  assert result[0]['title'] == 'Walk the dog'
