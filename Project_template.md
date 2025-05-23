# Project_template

Тип: Материал
Родитель: Описание проекта для 11 когорты (https://www.notion.so/11-03abbbbc8bcb49ed9b85c9b6d1174056?pvs=21)

Это шаблон для решения проектной работы. Структура этого файла повторяет структуру заданий. Заполняйте его по мере работы над решением.

# Задание 1. Анализ и планирование

В задании уже описано, что существующее приложение является монолитом, написано на `Java`, использует `PosgreSQL`, предоставляет REST API для клиентов и позволяет удаленно управлять устройством контроля отопления и получать данные о температуре. Требуется детально определить цели и задачи бизнеса, провести анализ приложения, через призму DDD. В терминах DDD этот этап этап можно определить как стратегическое проектирование.

«Тёплый дом» — это небольшая компания, которая организует удалённое управление отоплением в доме. Недавно она выиграла тендер и получила заказ на создание экосистемы умных посёлков на территории нескольких регионов страны.

Чтобы выполнить заказ, компании необходимо расширить функционал своей системы и масштабировать её. Экосистема должна позволить пользователям управлять не только  отоплением, но и умными устройствами в доме. 

### 1. Описание функциональности монолитного приложения

**Управление отоплением:**

- Пользователи могут удалённо включать/выключать отопление в своих домах
- Пользователи могут выставить уставку по температуре на включение/отключение отопления

**Мониторинг температуры:**

- Пользователи могут получить информацию о температуре в помещении

### 2. Анализ архитектуры монолитного приложения

По этому пункту все описано в задании:

- **Язык программирования**: Java
- **База данных**: PostgreSQL
- **Архитектура**: Монолитная, все компоненты системы (обработка запросов, бизнес-логика, работа с данными) находятся в рамках одного приложения.
- **Взаимодействие**: Синхронное, запросы обрабатываются последовательно.
- **Масштабируемость**: Ограничена, так как монолит сложно масштабировать по частям.
- **Развёртывание**: Требует остановки всего приложения.

### 3. Определение доменов и границы контекстов

Далее описаны по уровням L1 - домены приложения, L2 - поддомены,  L3 - контексты

- Умный дом
  - Устройства
    - Регистрация
    - Управление
  - Телеметрия
    - Сбор и передача показаний
    - Видеонаблюдение
- Пользователи 
  - Управление аккаунтом
  - Уведомления

### **4. Проблемы монолитного решения**

Проще всего провести анализ проблем текущего решения, основываясь на целях бизнеса на ближайший год.

- *Экосистема доступна пользователю в режиме самообслуживания по модели SaaS.* 

Для работы по модели SaaS требуется обеспечить высокую доступность сервиса. Сейчас за взаимодействие с пользователем отвечает одно монолитное приложение - сервер синхронно обрабатывающий запросы от конечных устройств с единой базой данных, это может влиять на доступность функционала. Кроме того - в момент обновления монолитного приложения клиент теряет связь с сервером до окончания обновления. 

Также стоит отметить сложность масштабирования такого варианта приложения.

- *Система позволяет управлять отоплением, включать и выключать свет, запирать и отпирать автоматические ворота, удалённо наблюдать за домом. Также в будущем могут появиться запросы на добавление новой функциональности. Решение должно быть легко расширяемым.*  

Требуется разработать много нового функционала. В рамках единого монолитного приложения это может быть сопряжено с рядом рисков для бизнеса: увеличение числа ошибок, усложнение тестирования, увеличение сроков разработки. 

- *Пользователь самостоятельно выбирает необходимые ему модули умного дома (устройства), сам их подключает, настраивает сценарии работы и просматривает телеметрию. Компания не занимается производством устройств, но поддерживает подключение к экосистеме устройств партнёров по стандартным протоколам.*
  - *Модули управления приборами и сами приборы (устройства) должны быть максимально готовы к использованию и продаваться в отдельных комплектах для удобной покупки и подключения.*
  - *Устройства должны быть доступны через интернет (для удалённого наблюдения и доступа). Предполагается, что пользователь будет иметь интернет-канал, к которому их можно подключить.*
  - *Покупатели могут программировать систему для управления различными модулями в соответствии со своими потребностями.*

В нынешней модели мастер на месте подключает модули к системе отопления. Для того, чтобы переложить эти функции на пользователя потребуется упростить механизм подключения модулей к системе. Если это будут стандартные модули, подключаемые по стандартизированным протоколам коммуникации, то требуется обеспечить поддержку различных стандартных протоколов, автоматическую аутентификацию и регистрацию IoT устройств в системе. Потребуется обеспечить интеграцию "Теплого дома" с множеством устройств, которые уже присутствуют или только выходят на рынок. Чтобы быстро реагировать на запросы клиентов, потребуется поддерживать короткий цикла разработки и высокую частоту релизов. Переход на микросервисы поможет этого добиться при условии, что API сервисов будут строго контролироваться.

- *Недавно компания выиграла тендер и получила заказ на создание экосистемы умных посёлков на территории нескольких регионов страны. У приложения 100 веб-клиентов, к системе подключены 100 модулей управления отоплением*

Оценим текущую и предполагаемую нагрузку на систему. Нунешняя нагрузка определяется главным образом IoT устройствами. Нагрузка постоянная, предсказуемая. Учитывая планы компании подключить к системе сеть поселков и расширить ассортимент умных устройств, можно говорить о увеличении числа устройств в 100 или даже 1000 раз, как и нагрузки на систему.

Отдельно следует учитывать стриминг видео с камер видеонаблюдения. 

Монолитное приложение скорее всего не сможет обеспечить высокий SLA, при увеличении нагрузок.

#### Вывод

Таким образом в контексте поставленных бизнесом задач микросервисная архитектура обеспечит:

- высокую доступность сервиса (шанс, что одновременно откажут несколько экземпляров одного приложения меньше, чем шанс отказа одного, функционал распределен по разным приложениям, поэтому пользователям всегда будет доступна по крайней мере часть функционала)
- удобство обновления и развертывания нового функционала 
- возможность масштабирования при росте нагрузки
- возможность настроить требуемый набор функций для отдельных пользователей
- ускорит разработку и вывод на рынок нового функционала

### 5. Визуализация контекста системы — диаграмма С4

**Важно**: В задании не было описания UI для пользователя (в 9 когорте было упоминание, что есть веб приложение с пользовательским интерфейсом, которое разрабатывается на аутсорсе), поэтому я в диаграмме отразил, что пользователь пользуется напрямую API сервиса. 

[Диаграмма контекста в модели C4.](./doc/Context.puml)

# Задание 2. Проектирование микросервисной архитектуры

При разделении приложения на микросервисы (МС) будем учитывать **14 принципов проектирования микросервисов**:

1. *Границы сервисов*. При разделении функционала приложения на МС будем руководствоваться DDD для определения границ МС, отвечающих за бизнес логику и SRP для определения МС выполняющих вспомогательные функции.
2. *Методы взаимодействия*. Так как речь идет о SaaS, требуется обеспечить низкие задержки, масштабируемость и отказоустойчивость, согласованность не является высоким приоритетом в данном случае, поэтому подойдет асинхронное взаимодействие через брокер сообщений.
3. *Управление данными*. Не страшно, если фактическая температура и температура в веб приложении будут немного отличаться. Этот фактор не является критически важным для сервиса, поэтому подойдет согласованность в конечном итоге.
4. *Стратегии развертывания*. Потребуются частые обновления и высокая доступность, т.е. в моменты обновления сервис должен будет оставаться доступным, поэтому развертывание нужно будет автоматизировать, поэтому хорошо подойдут контейниризация  и оркестрация развертывания.
5. *Балансировка нагрузки*. На этапе планирования сложно понять какой подход даст наилучший результат. Так как нагрузка на запись/чтение обусловлена главным образом умными устройствам, а следовательно постоянна и предсказуема, то, если предположить, что IP адреса устройств распределены равномерно, то хорошо должна подойти балансировка по IP-хэш сумме.
6. *Устойчивость к сбоям*. Пользователи не должны терять контроль над своим домом, для достижения этого может потребоваться избыточность МС. Что касается повторов (Retry), то важно, чтобы пользователю не пришлось повторять команды, потеря некоторого количества данных телеметрии может быть допустима. Выключатели (Circuit Breaker) могут потребоваться, чтобы разгрузить систему в случае  возникновения сбоев, чтобы предотвратить каскадный отказ системы.
7. *Масштабируемость*. Профиль нагрузки ожидается статический и предсказуемый, так как основной трафик генерируется умными устройствами, однако объем трафика должен постоянно расти, что требует обеспечить возможность горизонтального масштабирования системы, поэтому требуется обеспечить `stateless` сервисы.
8. *Безопасность*. Пользователи и умные устройства должны проходить аутентификацию и авторизацию. 
9. *Мониторинг и наблюдение*. Для подержания системы в устойчивом состоянии требуется обеспечить ее наблюдаемость. Нужно будет централизованно собирать логи (Log Aggregation), генерировать уведомления об аварии при отказе отдельных экземпляров МС (Health Check API), а также обирать метрики (Application metrics), чтобы своевременно выявлять бутылочные горлышки разрабатываемой системы.
10. *Хранение данных*. Предполагается использовать по одной базе данных на сервис (Database per Service) что обеспечит низкую связность сервисов, возможность независимого шардирования и репликации отдельных баз данных, а также разделить технологии. Так как данные структурированы, то в нашем случае может быть предпочтительнее использовать SQL. Для распределенных транзакций предлагается использовать паттерн SAGA.
11. *Управление API*. Так как речь идет о SaaS, то, чтобы обеспечить динамичное развитие функционала потребуется поддерживать версионирование API с обеспечением обратной совместимости.
12. *Тестирование и валидация*. Для обеспечения качества разрабатываемого ПО и уменьшения длительности релизного цикла потребуются автоматизированные модульные тесты на уровне приложений, интеграционные тесты МС. E2e тесты можно проводить в ручную, автоматизировав только несколько базовых сценариев.
13. *DevOps-практики*. Для поддержания динамики разработки потребуется использовать CI-пайплайны, чтобы упростить интеграцию кода разработчиков,CD практики позволят регулярно обновлять сервис, а поход IaC позволит ускорить процесс и уменьшить число ошибок при развертывании приложений.
14. *Версионирование и совместимость*. Так как сервисы будут обновляться независимо, для обеспечения большей гибкости, то для обеспечения контроля развертывания потребуется использовать семантическое версионирование, а также обратную совместимость на уровне API по крайней мере в пределах смежных мажорных версии.

#### Итоговая декомпозиция приложения на микросервисы

**Диаграмма контейнеров (Containers)**

[Container.puml](./doc/Container.puml)

**Диаграмма компонентов (Components)**

- [Devices Registry Service](./doc/Components/DeviceRegistrySeviceComponent.puml)
- [Devices Control Service](./doc/Components/DeviceControlServiceComponent.puml)
- [Telemetry Service](./doc/Components/TelemetryServiceComponent.puml)
- [CCTV Service](./doc/Components/CctvServiceComponent.puml)
- [User Account Service](./doc/Components/UserAccountServiceComponent.puml)
- [User Notification Service](./doc/Components/UserNotificationServiceComponent.puml)

**Диаграмма кода (Code)**

[Code.md](./doc/Code.puml)

# Задание 3. Разработка ER-диаграммы

[Entity-Relation.puml](./doc/Entity-Relation.puml)

# ❌ Задание 4. Создание и документирование API

### 1. Тип API

Укажите, какой тип API вы будете использовать для взаимодействия микросервисов. Объясните своё решение.

### 2. Документация API

Здесь приложите ссылки на документацию API для микросервисов, которые вы спроектировали в первой части проектной работы. Для документирования используйте Swagger/OpenAPI или AsyncAPI.