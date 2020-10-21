# simple_http_server
**Пример решаемой задачи**

Сервис реализует HTTP API для загрузки (upload),
скачивания (download) и удаления файлов.

 **Последовательность настройки**
  
 Скачаем репозиторий
 ###### git clone https://github.com/dmitry-chvdr/simple_http_server.git
 
 Переходим в корневую папку проекта
 
 ###### cd /..../simple_http_server
 
 Развернём сервис

 ###### sh deploy.sh
 
 Запустим тесты 
 
 ###### pytest server_test.py
 
 **Работа с сервисом**
 
 Объекты и методы
 
    /file
    post:
      /{fileHash}
      get:   
      delete:

 Примеры запроса
 
 GET
 
 curl -X GET http://localhost:8000/file/c656130152ab5a59243bf313a74515b
 
 POST
 
 curl -F "image=@/home/user/Desktop/image.pdf"   http://locahost:8000/file/
 
 DELETE
 
 curl -X DELETE http://localhost:8000/file/c656130152ab5a59243bf313a745
 
 
