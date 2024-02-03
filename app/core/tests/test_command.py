import time
import pytest

from unittest.mock import patch

from django.core.management import call_command


@pytest.mark.django_db
def test_wait_for_db_command(capsys):
    """Test wait_for_db management command."""

    with patch("time.sleep", return_value=None):
        call_command("wait_for_db", sleep=3)

    captured = capsys.readouterr()

    assert "Waiting for the database..." in captured.out
    assert "Database available!" in captured.out
