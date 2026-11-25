"""Exercise the workflows linked from the public portfolio."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(channel="chrome")
    page = browser.new_page()
    page.goto("https://taskflow-kycile24.onrender.com", timeout=90000)
    page.select_option("#language", "uk")
    expect(page.get_by_role("heading", name="Моя дошка")).to_be_visible()
    page.reload()
    page.get_by_role("button", name="Додати завдання").click()
    page.get_by_label("Назва завдання").fill("Перевірити каталог")
    page.get_by_role("button", name="Зберегти").click()
    page.get_by_role("button", name="Завершити", exact=True).click()
    expect(page.locator("#done")).to_contain_text("Перевірити каталог")
    page.select_option("#language", "en")
    expect(page.get_by_role("button", name="Reopen")).to_be_visible()
    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Delete").click()
    expect(page.locator("#doneCount")).to_have_text("0")

    page.goto("https://warehouse-kycile24.onrender.com", timeout=90000)
    expect(page.locator("#metrics strong").first).to_have_text("33", timeout=30000)
    page.fill("#catalogQuery", "AX55")
    expect(page.locator("#catalogRows tr")).to_have_count(2)
    page.get_by_role("button", name="Add to plan").first.click()
    page.locator("#planRows input").fill("17")
    page.locator("#planRows input").press("Tab")
    page.reload()
    expect(page.locator("#planRows input")).to_have_value("17")
    with page.expect_download() as export:
        page.click("#export")
    csv = Path(export.value.path()).read_text(encoding="utf-8-sig")
    assert 'AX55' in csv and '"17"' in csv
    page.select_option("#language", "uk")
    expect(page.get_by_role("heading", name="План поповнення")).to_be_visible()
    browser.close()
