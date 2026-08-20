from playwright.sync_api import expect


def test_support_form_page_content(page, live_server_url):
    page.goto(live_server_url + "/support-form/")

    expect(page.get_by_role("heading", level=1)).to_have_text("Contact National Data Library")
    expect(page.locator("legend", has_text="What's it to do with?")).to_have_count(1)
    expect(page.locator("label", has_text="What are the details")).to_have_count(1)
    expect(page.locator("label", has_text="Your name")).to_have_count(1)
    expect(page.locator("label", has_text="Your email address")).to_have_count(1)


def test_support_form_choosing_what_is_it_to_do_with(page, live_server_url):
    page.goto(live_server_url + "/support-form/")

    expect(page.locator("legend", has_text="What's it to do with?")).to_have_count(1)

    choice = page.locator("label", has_text=" A specific page ")
    choice.click()
