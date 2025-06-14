import shutil
from pathlib import Path
from types import SimpleNamespace

from scikit_package.cli import add
from scikit_package.cli.add import news_item


def _setup_news_test_env(tmp_path):
    """Set up a temporary news directory and template file for testing."""
    test_news_dir = tmp_path / "news"
    test_news_dir.mkdir()
    # Locate the real TEMPLATE.rst file in the project root
    project_root = Path(__file__).resolve().parents[1]
    real_template_path = project_root / "news" / "TEMPLATE.rst"
    test_template_file = test_news_dir / "TEMPLATE.rst"
    # Copy the real template to the test directory
    shutil.copy(real_template_path, test_template_file)
    # Override paths for testing
    add.NEWS_DIR = str(test_news_dir)
    add.TEMPLATE_PATH = str(test_template_file)
    # Mock branch setup
    branch_name = "test-branch"
    import scikit_package.utils.auth as auth

    auth.get_current_branch = lambda: branch_name
    news_file = test_news_dir / f"{branch_name}.rst"
    return news_file


def test_add_news_item(tmp_path):
    """Test adding a news item to the news file."""
    news_file = _setup_news_test_env(tmp_path)
    # Mimic `package add --add -m "Add first news."`
    args1 = SimpleNamespace(
        add=True,
        change=False,
        deprecate=False,
        remove=False,
        fix=False,
        security=False,
        message="Add first news.",
    )
    news_item(args1)
    expected_content_1 = """**Added:**

* Add first news.

**Changed:**

* <news item>

**Deprecated:**

* <news item>

**Removed:**

* <news item>

**Fixed:**

* <news item>

**Security:**

* <news item>
"""
    content_1 = news_file.read_text()
    assert content_1.strip() == expected_content_1.strip()
    # Mimic `package add --add -m "Add second news."`
    args2 = SimpleNamespace(
        add=True,
        change=False,
        deprecate=False,
        remove=False,
        fix=False,
        security=False,
        message="Add second news.",
    )
    news_item(args2)
    expected_content_2 = """**Added:**

* Add second news.
* Add first news.

**Changed:**

* <news item>

**Deprecated:**

* <news item>

**Removed:**

* <news item>

**Fixed:**

* <news item>

**Security:**

* <news item>
"""
    content_2 = news_file.read_text()
    assert content_2.strip() == expected_content_2.strip()


def test_no_news_item(tmp_path):
    """Test adding "no news" item to the news file."""
    news_file = _setup_news_test_env(tmp_path)
    # Mimic `package add --no-news -m "Fix small typo."`
    args = SimpleNamespace(
        add=False,
        change=False,
        deprecate=False,
        remove=False,
        fix=False,
        security=False,
        message="Fix small typo.",
    )
    news_item(args)
    expected_content = """**Added:**

* No news added: Fix small typo.

**Changed:**

* <news item>

**Deprecated:**

* <news item>

**Removed:**

* <news item>

**Fixed:**

* <news item>

**Security:**

* <news item>
"""
    content = news_file.read_text()
    assert content.strip() == expected_content.strip()
