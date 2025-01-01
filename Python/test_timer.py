import pytest
from unittest.mock import Mock
from timer import Fancy_buttons

@pytest.fixture
def mock_screen():
    """Fixture to create a mock screen object with a default size."""
    screen = Mock()
    screen.get_size = Mock(return_value=(800, 600))
    return screen

@pytest.fixture
def fancy_button(mock_screen):
    """Fixture to create a Fancy_buttons instance with mock screen."""
    return Fancy_buttons(mock_screen, 0.1, 0.1, 0.5, 0.3)

def test_initial_dimensions(fancy_button):
    """Test the initial dimensions based on fractions."""
    assert fancy_button.x == pytest.approx(80)  # 0.1 * 800
    assert fancy_button.y == pytest.approx(60)  # 0.1 * 600
    assert fancy_button.width == pytest.approx(400)  # 0.5 * 800
    assert fancy_button.height == pytest.approx(180)  # 0.3 * 600

def test_recalculate_dimensions(fancy_button, mock_screen):
    """Test recalculation of dimensions after resizing."""
    # Change screen size
    mock_screen.get_size.return_value = (1024, 768)
    fancy_button.recalculate_dimensions()

    # Check recalculated dimensions
    assert fancy_button.x == pytest.approx(102.4)  # 0.1 * 1024
    assert fancy_button.y == pytest.approx(76.8)  # 0.1 * 768
    assert fancy_button.width == pytest.approx(512)  # 0.5 * 1024
    assert fancy_button.height == pytest.approx(230.4)  # 0.3 * 768

def test_fraction_attributes(fancy_button):
    """Test that fraction attributes are stored correctly."""
    assert fancy_button.fraction_of_x == 0.1
    assert fancy_button.fraction_of_y == 0.1
    assert fancy_button.fraction_of_width == 0.5
    assert fancy_button.fraction_of_height == 0.3


if __name__ == "__main__":
    pytest.main(["-v", __file__])
