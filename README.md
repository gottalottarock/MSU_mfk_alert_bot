# MSU_mfk_alert_bot
Bot for tracking vacant positions on MSU mfk.

Telegram бот для отслеживания освободившихся мест в записи на межфакультетские курсы МГУ.


##/start:
Для единовременной проверки мест:
/check <номер или ссылка на мфк>

Например:
/check 969 
или 
/check https://lk.msu.ru/course/view?id=969
для курса "Мозг: как он устроен и работает"

Для уведомлений об освободившихся местах
/follow <номер или ссылка на мфк>
Будет периодически проверять курс и уведомлять,
если появилось место в списке.
Можно добавить несколько курсов,
каждый курс будет отслеживаться некоторое время,
в конце отслеживая придет уведомление.

Для отображения информации по отслеживаемым курсам:
/status

Для отписки используйте /unfollow