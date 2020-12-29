#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import re
import sys
import time


PAT_IFRAME = re.compile(r"^(\<iframe\n(?:\s+\S+\n)+\>\<\/iframe\>\n)", re.MULTILINE)
PAT_SOURCE = re.compile(r"\s+src\=\"(\S+)\"")


def render_screenshot (source_html, source_png):
    """use Selenium to render `source_png` from `source_html`"""
    chrome_path = os.getcwd() + "/chromedriver"
    chrome_options = Options()  
    browser = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)

    browser.get(source_html)
    time.sleep(1)

    browser.get_screenshot_as_file(source_png)
    browser.quit()


def replace_pyvis_iframe (text, parent, stem):
    output = []

    for chunk in PAT_IFRAME.split(text):
        m_iframe = PAT_IFRAME.match(chunk)

        if m_iframe:
            source_html = None
            iframe = m_iframe.group()

            m_source = PAT_SOURCE.search(iframe)

            if m_source:
                source_html = m_source.group(1)

            if source_html:
                source_png = source_html.replace(".html", ".png")

                try:
                    os.mkdir("{}/{}_files".format(parent, stem))
                except:
                    pass

                render_screenshot(
                    "file://{}/examples/{}".format(os.getcwd(), source_html),
                    "{}/{}_files/{}".format(parent, stem, source_png),
                    )

                output.append("![png]({}_files/{})".format(stem, source_png))
            else:
                output.append(chunk)
        else:
            output.append(chunk)

    return "\n".join(output)


if __name__ == "__main__":
    filename = Path(sys.argv[1])

    parent = filename.parent
    stem = filename.stem

    with open(filename, "r") as f:
        text = f.read()

    text = replace_pyvis_iframe(text, parent, stem)

    with open(filename, "w") as f:
        f.write(text)
