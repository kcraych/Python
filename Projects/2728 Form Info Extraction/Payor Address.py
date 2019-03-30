import pandas as pd
import xlwt

def findnth(haystack,needle,n):
      parts = haystack.split(needle,n)
      if len(parts) <= n:
         return -1
      return len(haystack)-len(parts[-1])-len(needle)

fn = '12-21-17 input.xlsx' # file saved on python anywhere
df = pd.read_excel(fn)

list1 = ['MPI']
list2 = ['Payor Name']
list3 = ['Street Address']
list4 = ['City State Zip']
recordMax = len(df.index)
for record in range(0,recordMax):
      recordForm = df['Form'][record]
      mpi = df['MPI'][record]
      payor = df['Payor'][record]
      find = "~NM1*PR*2"
      count = 0
      if type(recordForm) is unicode:
          count = recordForm.count(find)
      occurance = 0
      while occurance < count:
         occurance += 1
         start = findnth(recordForm,find,1)
         recordForm = recordForm[start+1:]
         N3 = findnth(recordForm,"~",1)
         N4 = findnth(recordForm,"~",2)
         end = findnth(recordForm,"~",3)
         if recordForm[N3+1:N3+3] == 'N3':
            N3 = recordForm[N3+4:N4]
         else:
            N3 = recordForm[N3+1:N3+4]
         if recordForm[N4+1:N4+3] == 'N4':
            N4 = recordForm[N4+4:end]
         else:
            N4 = recordForm[N4+1:N4+4]
         list1.append(mpi)
         list2.append(payor)
         list3.append(N3)
         list4.append(N4)

book = xlwt.Workbook()
sheet1 = book.add_sheet('sheet1')

for i,e in enumerate(list1):
    sheet1.write(i,0,e)
for i,e in enumerate(list2):
    sheet1.write(i,1,e)
for i,e in enumerate(list3):
    sheet1.write(i,2,e)
for i,e in enumerate(list4):
    sheet1.write(i,3,e)

name = "output.xls"
book.save(name)
book.save(TemporaryFile())