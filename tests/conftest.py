import os
import re
import warnings
from datetime import datetime
from pathlib import Path

import pytest
import allure
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption("--headed", action="store_true", help="Run Chrome with a visible browser window")


@pytest.fixture
def driver(request):
    options = Options()
    if not request.config.getoption("--headed"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    if os.getenv("CHROME_BINARY"):
        options.binary_location = os.environ["CHROME_BINARY"]

    browser = webdriver.Chrome(options=options)
    try:
        yield browser
    finally:
        test_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", request.node.name)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        screenshot_dir = Path(__file__).resolve().parents[1] / "evidence"
        screenshot_path = screenshot_dir / f"{timestamp}_{test_name}.png"
        try:
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            if browser.save_screenshot(str(screenshot_path)):
                allure.attach.file(
                    str(screenshot_path),
                    name=request.node.name,
                    attachment_type=allure.attachment_type.PNG,
                )
            else:
                warnings.warn(f"Could not save screenshot for {request.node.name}", RuntimeWarning)
        except (OSError, WebDriverException) as error:
            warnings.warn(f"Could not save screenshot for {request.node.name}: {error}", RuntimeWarning)
        finally:
            browser.quit()
