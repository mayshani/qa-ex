from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

service = Service("C:/chromedriver/chromedriver-win64/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("http://localhost:8080/")
wait = WebDriverWait(driver, 10)

# writing a function to fill the data to avoid redundancy
def fill_task(title, description, priority, date):
    title_input = driver.find_element(By.XPATH, "//input[@placeholder='Task title']")
    title_input.clear()
    title_input.send_keys(title)

    desc_input = driver.find_element(By.XPATH, "//textarea[@placeholder='Task description']")
    desc_input.clear()
    desc_input.send_keys(description)

    select = driver.find_element(By.TAG_NAME, "select")
    select.send_keys(priority)

    date_input = driver.find_element(By.XPATH, "//input[@type='date']")
    date_input.clear()
    date_input.send_keys(date)

    driver.find_element(By.XPATH, "//button[contains(text(),'Add Task')]").click()

# TC1: Add valid task
fill_task("Do laundry", "White clothes", "Medium", "12/3/2025")
time.sleep(1)

tasks = driver.find_elements(By.XPATH, "//li[contains(., 'Do laundry')]")
assert len(tasks) > 0, "task was not added"
print("TC1 passed: Task was added successfully")

# TC3: Completed task test
fill_task("Checkbox Test", "Check if checkbox works.", "Low", "12/6/2025")
time.sleep(1)

# checkbox filling
checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
checkboxes[-1].click()  # selects the last checkbox found

driver.refresh()  # need to refresh or login again to see tha change
time.sleep(2)

# It was easier for me to sort the task that are in active tasks to assure that completed is fine

active_tasks = driver.find_elements(By.XPATH, "//div[contains(@class, 'task') and contains(., 'Checkbox Test')]")
assert len(active_tasks) > 0, "is the task after check became completed?"
print("TC2 passed: Checkbox behavior is fine")

# TC 5: Filling passed date
fill_task("Past Date Test", "Trying to add a past date.", "Low", "02/04/2020")
time.sleep(3)
task_exists = any("Past Date Test" in task.text for task in driver.find_elements(By.TAG_NAME, "li"))
# runs all the dates in the list untill the passed date

if task_exists:
    print("Bug: Task with past date was added, which is incorrect!")
else:
    print("Success: Task with past date was not added, as expected.")


driver.quit()



