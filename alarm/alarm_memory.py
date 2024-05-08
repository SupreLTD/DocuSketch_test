import logging
import psutil
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MEMORY_THRESHOLD = 75
API_URL = "http://api-url.com/alarm"


def check_memory_usage(memory_threshold) -> None:
    memory_percent = psutil.virtual_memory().percent
    if memory_percent > memory_threshold:
        send_alarm()


#
def send_alarm():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            logger.info("Аларм отправлен успешно!")
        else:
            logger.error(f"Ошибка отправки аларма. Код ответа: {response.status_code}")
    except (requests.exceptions.RequestException, Exception) as e:
        logger.error(f"Ошибка отправки аларма: {e}")


while True:
    check_memory_usage(MEMORY_THRESHOLD)
