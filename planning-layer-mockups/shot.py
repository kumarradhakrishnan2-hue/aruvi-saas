from playwright.sync_api import sync_playwright
import os
f = "file://" + os.path.abspath("readiness-grid-flow.html")
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":390,"height":844})
    pg.goto(f); pg.wait_for_timeout(400)
    pg.eval_on_selector("text=Continue to the weekly grid", "el=>el.click()")
    pg.wait_for_timeout(400)
    sw = pg.evaluate("document.documentElement.scrollWidth"); cw = pg.evaluate("document.documentElement.clientWidth")
    print("mobile scrollW", sw, "clientW", cw, "=>", "OVERFLOW" if sw>cw+1 else "no-overflow")
    pg.screenshot(path="m_grid.png", full_page=True)
    pg2 = b.new_page(viewport={"width":900,"height":1100})
    pg2.goto(f); pg2.wait_for_timeout(300)
    pg2.eval_on_selector("text=Continue to the weekly grid", "el=>el.click()")
    pg2.wait_for_timeout(300)
    pg2.screenshot(path="d_grid.png", full_page=True)
    b.close()
print("done")
