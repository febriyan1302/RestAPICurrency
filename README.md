# RestAPICurrency

This Project using
- Python 3 With Django Rest Framework
- Mysql
- Docker (2 container -> app & mysql)

app run with port :8087, Ex : localhost:8087

To import database please run : "/bin/sh import_database.sh"

1. [x] User Input daily exchange data -> tanggal, from, to, rate

   => curl --header "Content-Type: application/json" --request POST --data '{"c_from":"IDR","c_to":"GBP","rate":15000,"tanggal":"2018-08-19"}' http://localhost:8087/price/


2. [x] User can see exchange rate
    - [x] with parameter -> date 
    - [x] Response Required “FROM, TO, Rate, 7-day avrage”
  
  => curl "http://127.0.0.1:8087/price/"
  
  => curl "http://127.0.0.1:8087/price/?date=2018-8-16"


3. [x] User want to add exchange list with parameter -> FROM & TO

  => curl --header "Content-Type: application/json" --request POST --data '{"c_from":"IDR","c_to":"MAY"}' http://localhost:8087/exchange/
  
  
4. [x] User can delete exchange list with parameter -> FROM & TO

  => curl -X "DELETE" http://127.0.0.1:8087/exchange/IDR/MAY
  

Thank You !
