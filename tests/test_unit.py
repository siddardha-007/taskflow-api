# tests/test_unit.py
import pytest
from unittest.mock import MagicMock
from app.services.task import TaskService
from app.schemas.task import TaskCreate, TaskUpdate

# ==========================================
# Schema Validation Unit Tests
# ==========================================

def test_task_create_schema_valid():
    task = TaskCreate(title="Build Service", description="Write tests", priority=2)
    assert task.title == "Build Service"
    assert task.priority == 2

def test_task_create_schema_short_title():
    with pytest.raises(ValueError):
        TaskCreate(title="AB")

def test_task_update_schema_empty():
    with pytest.raises(ValueError, match="Provide at least one field to update"):
        TaskUpdate()

# ==========================================
# TaskService Unit Tests
# ==========================================

@pytest.fixture
def mock_db():
    return MagicMock()

def test_create_task_project_not_found(mock_db):
    service = TaskService(mock_db)
    # Mock the repository on the service instance
    service.projects = MagicMock()
    service.projects.get_by_id.return_value = None

    data = TaskCreate(title="Test Task")
    with pytest.raises(LookupError, match="Project not found"):
        service.create_task(project_id=1, data=data)

def test_create_task_success(mock_db):
    service = TaskService(mock_db)
    service.projects = MagicMock()
    service.tasks = MagicMock()

    service.projects.get_by_id.return_value = MagicMock(id=1)
    
    mock_task = MagicMock(id=10, title="Test Task")
    service.tasks.create.return_value = mock_task

    data = TaskCreate(title="Test Task")
    result = service.create_task(project_id=1, data=data)

    assert result.title == "Test Task"
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_task)

def test_update_task_none_value_error(mock_db):
    service = TaskService(mock_db)
    service.tasks = MagicMock()
    
    existing_task = MagicMock(project_id=1)
    service.tasks.get_by_id.return_value = existing_task

    data = TaskUpdate(title="Valid Title")
    # Manually inject None into fields dict to test service validation logic
    object.__setattr__(data, '__pydantic_fields_set__', {'title'})
    data.__dict__['title'] = None

    with pytest.raises(ValueError, match="Updated fields cannot be null"):
        service.update_task(project_id=1, task_id=10, data=data)