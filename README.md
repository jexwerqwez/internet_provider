# Описание предметной области

Интернет-провайдер предоставляет своим клиентам интернет-услуги. С каждым клиентом заключается договор на предоставление услуг. В договоре указываются паспортные данные клиента, дата заключения договора. При расторжении договорапроставляется дата прекращения оказания услуг. 

За каждую подключенную услугу с клиента ежедневно списывается с баланса стоимость услуги. При этом фиксируется дата и время изменения баланса. Если баланс после списания стоимости услуги становится отрицательным, то клиент блокируется. Активный клиент (с положительным балансом) имеет статус 1. Заблокированный - статус 2.

Стоимость услуг время от времени меняется. При изменении стоимости для истории сохраняется старое значение, новое значение и дата изменеия.

Каждый клиент может подключить/отключить любое количество услуг в любое время. Даты включения/отключения услуг у клиента сохраняются.

# Конечные пользователи системы
1. Клиент - внешний пользователь информационной системы:
	- личный кабинет;
	- просмотр услуг;
        - выполнение запросов по услугам;
        - конструктор тарифа.
2. Администратор  - внутренний пользователь информационной системы:
	- редактирование услуг.
3. Техническая поддержка клиентов - внутренний пользователь информационной системы:
	- просмотр данных клиентов;
        - выполнение запросов по клиентам;
        - составление отчётов, связанных с клиентами.
4. Финансовый отдел  "--- внутренний пользователь информационной системы
	- управление финансовыми операциями;
	- составление финансовых отчётов.
5. Директор  - внутренний пользователь информационной системы:
	- просмотр всех созданных отчётов.

# Основной бизнес-процесс в предметной области}
Подключение и отключение услуг клиентами/клиентам.