from types import SimpleNamespace

from scikit_package.cli.add import news_item
from scikit_package.utils import auth

TEMPLATE_CONTENT = """**Added:**

* <news item>

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


def _setup_news_test_env(tmp_path, template_content=TEMPLATE_CONTENT):
    """Set up a temporary news directory and template file for testing."""
    news_dir = tmp_path / "news"
    news_dir.mkdir()
    template_file = news_dir / "TEMPLATE.rst"
    template_file.write_text(template_content)
    # Override the default news directory and template path
    from scikit_package.cli import add

    add.NEWS_DIR = str(news_dir)
    add.TEMPLATE_PATH = str(template_file)
    branch_name = "test-branch"
    # Mock the auth.get_current_branch to return a specific branch name
    auth.get_current_branch = lambda: branch_name
    news_file = news_dir / f"{branch_name}.rst"
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
