from datetime import datetime
import csv
def read(name):
  now = datetime.now()
  dtString  = now.strftime("%m/%d/%Y, %H:%M:%S")
  with open('Record.csv','r+') as csv_file:
    csv_writer=csv.writer(csv_file,delimiter=',')
    csv_reader=csv.reader(csv_file, delimiter=',')
    data=list(csv_reader)
    reversedList = reversed(data)
    # print(list(reversedList))
    for i,j in enumerate(reversedList):
      if(isinstance(j,list) and len(j)==2):
          print(j)
          if(j[0] == name):
            print('found')
            print(type(j[1]))
            dateDif= (datetime.now()-datetime.strptime(j[1],'%m/%d/%Y, %H:%M:%S')).total_seconds()
            print(dateDif)
            if(dateDif>28800):
              csv_writer.writerow([name,dtString])
            csv_writer.writerow([name,dtString])

    

read('ADS SDS CC')


