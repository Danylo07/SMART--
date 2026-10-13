# SmartHome OpenHAB
Навчальний пакет до практичної роботи. Орієнтовно для OpenHAB 4.1.x, Mosquitto 2.x, Python 3.

## Запуск
1. Запустіть Mosquitto з конфігурацією `mqtt/mosquitto.conf`.
2. Розмістіть каталог `conf` у `/openhab/conf` контейнера OpenHAB.
3. Установіть MQTT binding через Add-ons.
4. Встановіть залежність: `python -m pip install 'paho-mqtt>=2.0'`.
5. Запустіть: `python smart_home_simulator.py`.
6. Перевірте: `mosquitto_sub -h localhost -t 'smarthome/#' -v`.
7. Відкрийте `http://localhost:8080`.

Для Docker можна використати `docker run -d --name mqtt-broker -p 1883:1883 -v "$PWD/mqtt:/mosquitto/config" eclipse-mosquitto:2` та `docker run -d --name openhab -p 8080:8080 -v "$PWD/conf:/openhab/conf" -v openhab_userdata:/openhab/userdata -v openhab_addons:/openhab/addons -e EXTRA_JAVA_OPTS='-Duser.timezone=Europe/Warsaw' openhab/openhab:4.1.0`.

Увага: анонімний MQTT доступ призначений лише для ізольованого навчального стенда. Не відкривайте порт 1883 у публічний інтернет. Зробіть реальні скриншоти після запуску: головна сторінка, Things, Items, Sitemap, логи. Звіт не містить вигаданих скриншотів.
