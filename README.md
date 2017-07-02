# FAQ (Frequently Asked Questions)

Q1. How to import initial data to MongoDB?
  
```shell
mongoimport -d dbName -c CollectionName --type csv --file path/to/csvFileName.csv --headerline
```