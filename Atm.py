import random
import uuid
import mysql.connector as sql
from datetime import datetime
dtime=datetime.now()
database=sql.connect(
     host="localhost",
     user="root",
     password="Sahilscg9",
     database="atm_management")

cursor=database.cursor()

print(" !!!!!!!!!!!    W E L C O M E   TO    H E L L O    A T M       !!!!!!!!!!!!!!!!")
print("\n")
print("NOTE: If You Are New Here Please Register First..  !!!!!!!!!!!")
print("\n")
print("NOTE: If You Have Already Account Please Login  !!!!!!!!!!!")
print("\n")
print("1. Login ")
print("2.Register")
def choices():
    choose=int(input("Enter : "))
    if(choose==1):
        Accountnum=Login()
        main(Accountnum)

    elif(choose==2):
        Register()
    else:
        print("Wrong Choice!!!!! \n ")
        print(" Please Enter Right Option....... ")
        choices()

def num(Accountnum):
     print("1.Back ")
     back=int(input("Enter :"))
     if(back==1):
        main(Accountnum)
     else:
        print( "!!!!! Invalid !!!!!")
        num()
          

def pinchange(Accountnum):
       pin=int(input("Enter New Pin :"))
       while(pin<1000 or pin>9999):
            print("!!! Please Enter 4 digit PIN !!!")
            pin=int(input("Enter Four Digit Pin :"))  
       else:
            cursor.execute("update details set pin=%s where Accountno=%s",(pin,Accountnum))
            database.commit() 
            print("Pin Entered Succesfully") 
            num(Accountnum)


def deposit(Accountnum):
     value="Deposit"
     depositt=float(input("Enter The Money :"))
     query3="update details set Balance=Balance+%s where Accountno=%s"
     cursor.execute(query3,(depositt,Accountnum))
     database.commit()
     print("\n")
     print("      Balance is Deposited.........")
     print("\n")
     cursor.execute("select Balance from details where Accountno=%s",(Accountnum,))
     res=cursor.fetchone()
     print(" Your New Balance Is :",res[0])
     #For Transaction Id :
     cursor.execute("select Name from details where Accountno=%s",(Accountnum,))
     data2=cursor.fetchone()
     tran=str(uuid.uuid4())
     cursor.execute("insert into statement (Transaction_id, Name, Accountno, Balance, Type, transaction_date)values(%s,%s,%s,%s,%s,%s)",(tran,data2[0],Accountnum,res[0],value,datetime.now()))
     database.commit()
     print("           T H A N K  Y O U          ")
     print("\n")
     main(Accountnum)

def transfer(Accountnum):
    value="Transfer"
    tranAccountnum=int(input("Enter The Account Number :"))
    ifsccode=(input("Enter The IFSC Code :"))
    cursor.execute("select Accountno from details where Accountno=%s",(Accountnum,))
    data1=cursor.fetchone()
    cursor.execute("select Balance from details where Accountno=%s",(Accountnum,))
    data2=cursor.fetchone()
    if data1[0]==Accountnum:
        bal=float(input("Enter The Money For Transfer :"))
        if data2[0]>=bal:
            cursor.execute("update details set Balance=Balance+%s where Accountno=%s and ifsc=%s",(bal,tranAccountnum,ifsccode))
            cursor.execute("update details set Balance=Balance-%s where Accountno=%s",(bal,Accountnum))
            database.commit()
            print("     Money Tranfer Sussessfully.......")
            print("\n")
            cursor.execute("select Balance from details where Accountno=%s",(Accountnum,))
            data=cursor.fetchone()
            print(" Your Remaining Balance Is :",data[0])
            cursor.execute("select Name from details where Accountno=%s",(Accountnum,))
            data2=cursor.fetchone()
            tran=str(uuid.uuid4())
            cursor.execute("insert into statement(Transaction_id, Name, Accountno, Balance, Type, transaction_date) values(%s,%s,%s,%s,%s,%s)",(tran,data2[0],Accountnum,data[0],value,datetime.now()))
            database.commit()
            print("\n")
            main(Accountnum)
        else:
            print("  !!!!!!!!!! Insufficint Balance !!!!!!!!!!")
            print("\n")
            main(Accountnum)

def withdrawl(Accountnum):
     value="WITHDRAWL"
     bal=float(input("Enter The Amount : "))
     cursor.execute("select Balance from details where Accountno=%s",(Accountnum,))
     data=cursor.fetchone()
     if data[0]<bal:
          print("  !!!!!!!!!! Insufficint Balance !!!!!!!!!!")
          print("\n")
          main(Accountnum)
     else:
        cursor.execute("update details set Balance=Balance-%s where Accountno=%s",(bal,Accountnum))
        database.commit()
        cursor.execute("select Balance from details where Accountno=%s",(Accountnum,))
        data1=cursor.fetchone()
        cursor.execute("select Name from details where Accountno=%s",(Accountnum,))
        data2=cursor.fetchone()
        tran=str(uuid.uuid4())
        cursor.execute("insert into statement(Transaction_id, Name, Accountno, Balance, Type, transaction_date) values(%s,%s,%s,%s,%s,%s)",(tran,data2[0],Accountnum,data1[0],value,datetime.now()))
        database.commit()
        print("   W I T H D R A W L   S U CC E SS F U LL Y ")
        print(" Your Remaining Balance Is :",data1[0])
        print("            .........T H A N K   Y O U   F O R    V I S I T I N G............")
        print("\n")
        main(Accountnum)


          
def balinquary(Accountnum):
     cursor.execute("Select Balance from details where Accountno=%s",(Accountnum,))
     data=cursor.fetchone()
     for i in data:
          print("Your Balance is : ",i)
     print("   ...........  T H A N K   Y O U   ........")
     print("\n")
     main(Accountnum)

def statement(Accountnum):
     cursor.execute("select Transaction_id,Name,Accountno,Balance,Type from statement where Accountno=%s ORDER BY id DESC LIMIT 5",(Accountnum,))
     data=cursor.fetchall()
     for i in data:
          print(i)
          print("\n")
     print("   ...........  T H A N K   Y O U   ........")
     print("\n")
     main(Accountnum)
     
     

 
def choices1(Accountnum):
     choose1=int(input("Enter :"))
     if(choose1==1):
          deposit(Accountnum)
     elif(choose1==2):
          transfer(Accountnum)
     elif(choose1==3):
          pinchange(Accountnum)
     elif(choose1==4):
          withdrawl(Accountnum)
     elif(choose1==5):
          balinquary(Accountnum)
     elif(choose1==6):
          statement(Accountnum)
     elif(choose1==7):
          print("\n")
          print("                  THANK YOU FOR VISITING OUR ATM :)")
          print("\n")
          print("                     PLEASE COLLECT YOU CARD :) ")
          print("\n")
          print("                        HAVE A NICE DAY :)")
          print("\n")
          exit()
     else:
          print(" Wrong Choose.....")
          choices1()
          
     


def main(Accountnum):
     print("                            ........ H E L L O   A T M  .........")
     print("                                    Select Transaction            ")
     print("            Accountno=",Accountnum)
     print("\n")
     print("                         1. DEPOSIT                       2. TRANSFER       ")
     print("                        3. PIN CAHNGE                   4. CASH WITHDRAWAL ")
     print("                         5. BALANCE INQUARY               6. MINI STATEMENT")
     print("\n")
     print("                                       7.EXIT                                                 ")

     print("\n")
     choices1(Accountnum)
     print("                  .........T H A N K   Y O U   F O R    V I S I T I N G............")

def Register():
    print("Please Enter V A L I D details.....")
    Name=str(input("Enter Your Name :"))
    Bank_Name=str(input("Enter Your Bank :"))
    Accountnum=int(input("Enter Your Account Number :"))
    ifsc=(input("Enter IFSC Code :"))
    pin=pinn()
    Balance=0
    query="insert into details values(%s,%s,%s,%s,%s,%s)"
    values=(Name,Bank_Name,Accountnum,ifsc,pin,Balance)
    cursor.execute(query,values)
    database.commit()
    print("Thanks You For Register.............")
    print("\n")
    print("Please Login ...........")
    display()
    return Balance

def Login():
    Accountnum=(input("Enter Your Account Number :"))
    pin=int(input("Enter Your Four Digit Pin :"))
    print("\n")
    query1="select Accountno,Pin from details where Accountno=%s And pin=%s"
    cursor.execute(query1,(Accountnum,pin))
    data1=cursor.fetchone()
    if data1:
            print("Login Susscessfully .......")
            print("\n")
            main(Accountnum)
            return Accountnum
            
    else:
        print("No Data Found Please Check Account Number or Pin ......")
        print("Login.....")
        return Login()
    
def display():
     
     print("Please Enter Details For Login..........")
     Login()
          

def pinn():
    h=int(input("Enter Four Digit Pin :"))
    while(h<1000 or h>9999):
        print("!!! Please Enter 4 digit PIN !!!")
        h=int(input("Enter Four Digit Pin :"))     
    else:
            print("Pin Entered Succesfully") 
            return h
    return h      
            
                 

choices()
    
    



