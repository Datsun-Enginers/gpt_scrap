import undetected_chromedriver as uc

def iniciar_webdriver(headless=False, pos="maximizada"):
    options = uc.ChromeOptions()
    options.headless = headless 
    options.add_argument("--password-store=basic")
    options.add_experimental_option(
        "prefs",
        {
            "credential_enable_service": False,
            "profile.password_manager_enabled": False,
        },
    )

    if headless:
        options.add_argument("--headless")

    driver = uc.Chrome(
        options=options,
        log_level=3,
    )

    if not headless:
        driver.maximize_window()
        if pos != "maximizada":
            ancho, alto = driver.get_window_size().values()
            if pos == "izquierda":
                driver.set_window_rect(x=0,y=0,width=ancho//2, height=alto)
            elif pos == "derecha":
                driver.set_window_rect(x=ancho//2,y=0,width=ancho//2, height=alto)
    return driver