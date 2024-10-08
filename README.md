# RPChatBotVK
Чат-бот для ролевых игр в ВК

Разделы:
- [RPChatBotVK](#rpchatbotvk)
- [Установка и запуск](#установка-и-запуск)
  - [Ручная установка](#ручная-установка)
  - [Через Docker](#через-docker)
  - [Через docker-compose](#через-docker-compose)
- [Конфигурация](#конфигурация)
  - [Основная конфигурация (config.ini)](#основная-конфигурация-configini)
    - [Раздел DEFAULT](#раздел-default)
    - [Раздел API](#раздел-api)
    - [Раздел VK](#раздел-vk)

# Установка и запуск

Вы можете развернуть бота с помощью одного из этих способов: <br/>
[Ручная установка](#ручная-установка)<br/>
[Через Docker](#через-docker)<br/>
[Через docker-compose](#через-docker-compose)<br/>

## Ручная установка

Чтобы установить бота вы можете скачать данный репозиторий на свой компьютер командой:

```bash
git clone https://github.com/Misha00025/RPChatBotVK.git 
```

Перейти в папку RPChatBotVK:

```bash
cd RPChatBotVK
```

Создать виртуальное окружение:

```bash
python -m venv venv
```

Активировать его:

```bash
source venv/bin/activate
```

Установить необходимые пакеты:

```bash
pip install -r req.txt
```

Запуск бота выполняется командой:

```bash
python main.py
```

ВНИМАНИЕ: перед запуском программы убедитесь, что правильно настроили бота ([см. "Конфигурация"](#конфигурация))

## Через Docker

Установка бота через Docker начинается со скачивания образа:

```bash
docker pull ghcr.io/misha00025/rpchatbot:<version>
```

где `<version>` необходимо заменить на желаемую версию бота <br/>
ОСТОРОЖНО: все версии бота до `1.0.0` являются **_нестабильными_**, так что используйте их на свой страх и риск

Запуск бота через Docker требует первоначального запуска команды:

```bash
docker run -d \
  --name <name> \
  -v ./configs:/root/RPChatBotVK/configs:rw \
  -v ./logs:/root/RPChatBotVK/logs:rw \
  -v ./saves:/root/RPChatBotVK/saves:rw \
  ghcr.io/misha00025/rpchatbot:<version>
```

`<name>` -- это название контейнера, который будет создан. <br/>
Дальше остановите контейнер:

```bash
docker container stop <name>
```

После остановки контейнера перейдите к [настройке](#конфигурация) и запустите бота снова:

```bash
docker container start <name>
```

## Через docker-compose

Создайте папку, в которой будете содержать бота. В этой папке создайте файл `docker-compose.yaml` и заполните его следующим содержимым:

```docker
services:
  rpchatbot:
    container_name: <name>
    image: ghcr.io/misha00025/rpchatbot:<version> 
    volumes:
      - './configs:/root/RPChatBotVK/configs:rw'
      - './logs:/root/RPChatBotVK/logs:rw'
      - './saves:/root/RPChatBotVK/saves:rw'
```

Замените:
- `<name>` на название контейнера;
- `<version>` на номер желаемой версии бота.

Дальше запустите бота, используя:

```bash
docker-compose up -d
```

После того как создадутся папки `configs`, `logs` и `saves` остановите его:

```bash
docker-compose stop
```

И перейдите к настройке ([см. "Конфигурация"](#конфигурация))

# Конфигурация

Бот работает по принципу клиент-серверного приложения, где сам бот представляет сторону клиента. Бот принимает сообщения от пользователей ВК и после предварительной обработки передаёт их запросы на специальный `сервер обработки данных` (или `СОД`).

Для работы бота обязательно наличие `СОД`. Разверните его самостоятельно из репозитория [TheDungeonNotebook](https://github.com/Misha00025/TheDungeonNotebook) или воспользуйтесь услугами по его аренде. 

Вся настройка бота выполняется через папку `configs`. В этой папке необходимо создать 4 файла:
- config.ini - основной файл конфигурации;
- keyboard.txt - файл "клавиатуры";
- service_token.txt - файл токена для обращения к `СОД`;
- token.txt - файл токена VK 
 
## Основная конфигурация (config.ini)

В этом файле должна содержаться основная информация, необходимая для работы бота. Если вы только создали файл, скопируйте в него содержимое [default_conf.ini](https://github.com/Misha00025/RPChatBotVK/blob/master/default_config.ini). Он используется в качестве шаблона конфигурационного файла.

Конфигурационный файл разбит на несколько разделов:
- `DEFAULT` - общие настройки бота;
- `API` - настройки работы с сервером;
- `VK` - настройки работы с VK.

### Раздел DEFAULT

Этот раздел содержит в себе:
- `LogFile` - название файла логов;
- `Listener` - откуда слушать сообщения (не используется);
- `Sender` - куда отправлять сообщения (не используется);
- `SilencePrefix` - префикс, предотвращающий пересылку сообщений;
- `KeyboardFile` - название файла с "клавиатурой", Адрес указывается относительно папки `configs`.

### Раздел API

Этот раздел содержит в себе:
- `Version` - используемая версия API `СОД`;
- `Protocol` - протокол соединения (`http` или `https`);
- `Host` - имя (или IP-адрес) хоста, на котором содержится `СОД`;
- `Port` (необязательно) - порт подключения. Если не указан, то будет использован порт выбранного протокола.
- `ServiceTokenFile` - название файла, содержащего токен подключения к `СОД`

### Раздел VK

Этот раздел содержит:
- `TokenFile` - файл, содержащий ключ доступа к группе ВК;

Для получения ключа доступа к группе ВК [см. официальную документацию ВК](https://dev.vk.com/ru/api/access-token/getting-started)