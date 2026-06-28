from playwright.sync_api import sync_playwright
import os
f="file://"+os.path.abspath("readiness-grid-flow.html")
with sync_playwright() as p:
    b=p.chromium.launch(args=["--no-sandbox"])
    pg=b.new_page(viewport={"width":390,"height":844})
    pg.goto(f); pg.wait_for_timeout(400)
    def ov(tag):
        sw=pg.evaluate("document.documentElement.scrollWidth"); cw=pg.evaluate("document.documentElement.clientWidth")
        print(tag, "scrollW", sw, "clientW", cw, "=> OVERFLOW" if sw>cw+1 else "=> ok")
    # durations screen
    ov("dur")
    pg.eval_on_selector("text=Continue to the weekly grid","e=>e.click()"); pg.wait_for_timeout(300)
    ov("grid-VI")
    # add a 60-min duration path? skip. go to next grade then to budget
    pg.eval_on_selector("#gridNext","e=>e.click()"); pg.wait_for_timeout(200)  # to grade VII dur
    # we're on dur for VII now; continue to its grid
    pg.eval_on_selector("text=Continue to the weekly grid","e=>e.click()"); pg.wait_for_timeout(200)
    ov("grid-VII")
    pg.eval_on_selector("#gridNext","e=>e.click()"); pg.wait_for_timeout(300)  # enter budget
    ov("budget-VI")
    pg.screenshot(path="m_budget.png", full_page=True)
    # open the working-days tab (longest summary line)
    pg.eval_on_selector("text=I know my working days","e=>e.click()"); pg.wait_for_timeout(300)
    ov("budget-days")
    pg.screenshot(path="m_budget_days.png", full_page=True)
    b.close()
print("DONE")
