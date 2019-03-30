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
list2 = ['Payor']
list3 = ['GrpPolNum']
recordMax = len(df.index)
for record in range(0,recordMax):
      recordForm = df['Form'][record]
      mpi = df['MPI'][record]
      payor = df['Payor'][record]
      find = "~REF*6P"
      count = 0
      if type(recordForm) is unicode:
          count = recordForm.count(find)
      occurance = 0
      while occurance < count:
         occurance += 1
         start = findnth(recordForm,find,1)
         recordForm = recordForm[start+8:]
         end = min(findnth(recordForm,"*",1),findnth(recordForm,"~",1))
         NUM = recordForm[:end]
         list1.append(mpi)
         list2.append(payor)
         list3.append(NUM)

book = xlwt.Workbook()
sheet1 = book.add_sheet('sheet1')

for i,e in enumerate(list1):
    sheet1.write(i,0,e)
for i,e in enumerate(list2):
    sheet1.write(i,1,e)
for i,e in enumerate(list3):
    sheet1.write(i,2,e)

name = "output6P.xls"
book.save(name)