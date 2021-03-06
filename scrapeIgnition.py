import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ignitionScraperTools import performAntiBotCounterMeasures
from ignitionScraperTools import login
from ignitionScraperTools import downloadSong
from ignitionScraperTools import sortSongsByMostDownloads
from ignitionScraperTools import searchForTrack
from scrapeSpotifyPlaylist import get_songs_from_spotify
from selenium.webdriver import Chrome

# Chrome executable location. (Open task manager, right click Chrome and select "Open file location")
webdriver.ChromeOptions.binary_location = ur"C:\\Program Files (x86)\\Google\\Chrome Beta\\Application\\chrome.exe"

# The login URL for CustomsForge
loginUrl = "https://customsforge.com/index.php?app=core&module=global&section=login"

playlist_url = "https://open.spotify.com/playlist/3hr3kUFmiZqCRs149azvmu?si=EZosJvSoSFyF7evdj0-wYg"

# The spotify playlist URL
searches = get_songs_from_spotify(playlist_url)

def downloadSongs(searches):
    # Chrome Driver setup.
    driver = Chrome()
    driver.implicitly_wait(10)

    # Perform login. (function hidden in tools file)
    login(driver, loginUrl)

    driver.find_element_by_id('nav_menu_19_trigger').click()

    WebDriverWait(driver, 10).until(EC.title_contains('Ignition3'))

    # Close the popup window which appears. (function hidden in tools file)
    performAntiBotCounterMeasures(driver)

    # Click the downloads sorter twice. (function hidden in tools file)
    sortSongsByMostDownloads(driver)

    # Perform our search(es)
    for searchTerms in searches:
        searchForTrack(driver, searchTerms)

        songRows = driver.find_elements_by_css_selector('tr.odd, tr.even')
        
        empty = driver.find_elements_by_css_selector('td.dataTables_empty')
        if not empty:
            # Open the context menu and ctrl+click to download.
            downloadSong(driver, songRows[0])

    # It throws an exception here because then the browser will remain open for some time, allowing you to download the files.
    raise Exception('Finished. You\'ll have to manually download the files now and move them to the appropriate location.')

downloadSongs(searches)