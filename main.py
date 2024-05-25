from selenium import webdriver
import random
import time
import pygame
import datetime
def play_sound():
    pygame.mixer.init()
    pygame.mixer.music.load("/home/user/Music/8 Graves_-_Bury me low.mp3")  # Replace with the path to your sound file
    pygame.mixer.music.play()


def is_within_time_range(start_hour, end_hour):
    current_time = datetime.datetime.now().time()
    start_time = datetime.time(start_hour, 0)
    end_time = datetime.time(end_hour, 0)

    return start_time <= current_time <= end_time

def refresh_page_if_text_present(driver, text_to_check):
    now = datetime.datetime.now()

    try:
        # Open the website
        driver.get("https://service.berlin.de/terminvereinbarung/termin/taken/#&termin=1&dienstleister=327437&anliegen[]=120691")  # Replace with your website URL

        # Check if the text is present on the page
        if text_to_check in driver.page_source:
            # Refresh the page
            driver.refresh()

            # Wait for the page to load after refresh
            time_sleep = random.randint(61, 180) + random.randint(1, 1000) * 0.001
            time.sleep(time_sleep)  # Adjust the sleep duration based on your website's loading time
            global i

            print(f"{i}, {now.time()} slept {time_sleep}, no luck, spent {now- start}")
            i += 1
            # Recursive call to check again
            refresh_page_if_text_present(driver, text_to_check)
        elif "Bitte probieren Sie es zu einem späteren Zeitpunkt erneut." in driver.page_source:
            print("Maintenance window")
            time.sleep(random.randint(1800, 3600))
            print(f"{now} retrying")
            refresh_page_if_text_present(driver, text_to_check)
        else:
            # Text is no longer present, stop refreshing
            print("Bingo! Act now!")
            play_sound()
            a = input()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    driver = webdriver.Chrome()

    # Text to check on the page
    text_to_check = "Leider sind aktuell keine Termine für ihre Auswahl verfügbar."

    try:
        i=0
        start = datetime.datetime.now()
        refresh_page_if_text_present(driver, text_to_check)
    finally:
        # Close the browser window
        driver.quit()
