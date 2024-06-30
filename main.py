import streamlit as st
import pandas as pd
from PIL import Image
import random
import sqlite3

conn = sqlite3.connect("drug_data.db",check_same_thread=False)
c = conn.cursor()

#Customers

def cust_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Customers(
                    C_Name VARCHAR(50) NOT NULL,
                    C_Password VARCHAR(50) NOT NULL,
                    C_Email VARCHAR(50) PRIMARY KEY NOT NULL, 
                    C_State VARCHAR(50) NOT NULL,
                    C_Number VARCHAR(50) NOT NULL 
                    )''')
    print('Customer Table create Successfully')

def customer_add_data(Cname, Cpass, Cemail, Cstate, Cnumber):
    c.execute('''INSERT INTO Customers (C_Name,C_Password,C_Email, C_State, C_Number) VALUES(?,?,?,?,?)''', (Cname,Cpass,Cemail,Cstate,Cnumber))
    conn.commit()

def customer_view_all_data():
    c.execute('SELECT * FROM Customers')
    customer_data = c.fetchall()
    return customer_data

def customer_update(Cemail,Cnumber):
    c.execute(''' UPDATE Customers SET C_Number = ? WHERE C_Email = ?''', (Cnumber,Cemail,))
    conn.commit()
    print("Updating")

def customer_delete(Cemail):
    c.execute(''' DELETE FROM Customers WHERE C_Email = ?''', (Cemail,))
    conn.commit()

#Drugs

def drug_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Drugs(
                D_Name VARCHAR(50) NOT NULL,
                D_ExpDate DATE NOT NULL, 
                D_Use VARCHAR(50) NOT NULL,
                D_Qty INT NOT NULL, 
                D_id INT PRIMARY KEY NOT NULL,
                D_Price DECIMAL(10,2) NOT NULL)
                ''')
    print('DRUG Table create Successfully')

def drug_add_data(Dname, Dexpdate, Duse, Dqty, Did, Dprice):
    c.execute('''INSERT INTO Drugs (D_Name, D_Expdate, D_Use, D_Qty, D_id, D_Price) VALUES(?,?,?,?,?,?)''', (Dname, Dexpdate, Duse, Dqty, Did, Dprice))
    conn.commit()

def drug_view_all_data():
    c.execute('SELECT * FROM Drugs')
    drug_data = c.fetchall()
    return drug_data

def drug_update(Duse, Did, Dprice):
    c.execute('''UPDATE Drugs SET D_Use = ?, D_Price = ? WHERE D_id = ?''', (Duse,Dprice,Did))
    conn.commit()

def drug_delete(Did):
    c.execute('''DELETE FROM Drugs WHERE D_id = ?''', (Did,))
    conn.commit()

#Orders

def order_create_table():
    c.execute('''
                CREATE TABLE IF NOT EXISTS Orders(
                O_Name VARCHAR(100) NOT NULL,
                O_Items VARCHAR(100) NOT NULL,
                O_Qty VARCHAR(100) NOT NULL,
                O_id VARCHAR(100) PRIMARY KEY NOT NULL,
                O_price DECIMAL(10,2))
              ''')

def order_add_data(O_Name,O_Items,O_Qty,O_id,O_price):
    c.execute('''INSERT INTO Orders (O_Name, O_Items, O_Qty, O_id, O_price) VALUES(?,?,?,?,?)''',
              (O_Name,O_Items,O_Qty,O_id,O_price))
    conn.commit()

def order_view_data(customername):
    c.execute('SELECT * FROM Orders Where O_Name == ?',(customername,))
    order_data = c.fetchall()
    return order_data

def order_view_all_data():
    c.execute('SELECT * FROM Orders')
    order_all_data = c.fetchall()
    return order_all_data

#suppliers

def supplier_create_table():
    c.execute('''
                CREATE TABLE IF NOT EXISTS Suppliers(
                S_id INT PRIMARY KEY NOT NULL,
                S_Name VARCHAR(50) NOT NULL, 
                D_id INT NOT NULL,
                D_name VARCHAR(50) NOT NULL,
                D_Qty INT NOT NULL,
                D_Price DECIMAL(10,2) NOT NULL,
                FOREIGN KEY(D_id) REFERENCES Drugs(D_id),
                FOREIGN KEY(D_name) REFERENCES Drugs(D_Name),
                FOREIGN KEY(D_Qty) REFERENCES Drugs(D_Qty),
                FOREIGN KEY(D_Price) REFERENCES Drugs(D_Price))
            ''')
    print("Supplier table created successfully")
    
def supplier_add_data(S_id, S_name, D_id, D_name, D_Qty, D_Price):
    c.execute('''
              INSERT INTO Suppliers (S_id, S_Name, D_id, D_name, D_Qty, D_Price)
              VALUES (?,?,?,?,?,?)
              ''', (S_id, S_name, D_id, D_name, D_Qty, D_Price))
    conn.commit()
    
def supplier_view_data():
    c.execute('SELECT * FROM Suppliers')
    supplier_data = c.fetchall()
    return supplier_data

def supplier_update(s_name, s_id):
    c.execute(''' UPDATE Suppliers SET S_Name = ? where S_id = ?''',(s_name,s_id))
    conn.commit()

def supplier_delete(s_id):
    c.execute(''' DELETE FROM Suppliers WHERE S_id = ? ''',(s_id,))
    conn.commit()

###################################################################

def admin():

    st.title("Pharmacy Database Dashboard")
    menu = ["Customers", "Suppliers", "Drugs", "Orders", "Insights"]
    choice = st.sidebar.selectbox("Menu", menu)

    ## DRUGS
    if choice == "Drugs":

        menu = ["Add", "View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Add":

            st.subheader("Add Drugs")

            col1, col2 = st.columns(2)

            with col1:
                drug_name = st.text_input("Enter the Drug Name")
                drug_expiry = st.date_input("Expiry Date of Drug (YYYY-MM-DD)")
                drug_mainuse = st.text_input("When to Use")
            with col2:
                drug_quantity = st.text_input("Enter the quantity")
                drug_id = st.text_input("Enter the Drug ID (example:#D1)")
                drug_price = st.text_input("Enter the price")

            if st.button("Add Drug"):
                drug_add_data(drug_name,drug_expiry,drug_mainuse,drug_quantity,drug_id,drug_price)
                st.success("Successfully Added Data")

        if choice == "View":
            st.subheader("Drug Details")
            drug_result = drug_view_all_data()
            with st.expander("View All Drug Data"):
                drug_clean_df = pd.DataFrame(drug_result, columns=["Name", "Expiry Date", "Use", "Quantity", "ID", "Price"])
                st.dataframe(drug_clean_df)
        
        if choice == 'Update':
            st.subheader("Update Drug Details")
            d_id = st.text_input("Drug ID")
            d_use = st.text_input("Drug Use")
            d_price = st.text_input("Drug Price")
            if st.button(label='Update'):
                drug_update(d_use,d_id,d_price)
                st.success("Drug Info Updated")

        if choice == 'Delete':
            st.subheader("Delete Drugs")
            did = st.text_input("Drug ID")
            if st.button(label="Delete"):
                drug_delete(did)
                st.success("Drug Deleted")

    ## CUSTOMERS
    elif choice == "Customers":

        menu = ["View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "View":
            st.subheader("Customer Details")
            cust_result = customer_view_all_data()
            with st.expander("View All Customer Data"):
                cust_clean_df = pd.DataFrame(cust_result, columns=["Name", "Password","Email-ID" ,"Area", "Number"])
                st.dataframe(cust_clean_df)

        if choice == 'Update':
            st.subheader("Update Customer Details")
            cust_email = st.text_input("Email")
            cust_number = st.text_input("Phone Number")
            if st.button(label='Update'):
                customer_update(cust_email,cust_number)
                st.success("Customer Info Updated")

        if choice == 'Delete':
            st.subheader("Delete Customer")
            cust_email = st.text_input("Email")
            if st.button(label="Delete"):
                customer_delete(cust_email)
                st.success("Customer Deleted")

    #ORDERS
    elif choice == "Orders":

        menu = ["View"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "View":
            st.subheader("Order Details")
            order_result = order_view_all_data()
            with st.expander("View All Order Data"):
                order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items","Qty" ,"ID", "Price"])
                st.dataframe(order_clean_df)

    #SUPPLIERS
    elif choice == "Suppliers":

        menu = ["Add", "View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Add":

            st.subheader("Add Suppliers")

            col1, col2 = st.columns(2)

            with col1:
                s_id = st.text_input("Enter supplier ID")
                drug_id = st.text_input("Enter the Drug ID (example:#D1)")
                drug_quantity = st.text_input("Enter the quantity")
            with col2:
                s_name = st.text_input("Enter supplier name")
                drug_name = st.text_input("Enter the Drug Name")
                drug_price = st.text_input("Enter the price")

            if st.button("Add Supplier"):
                supplier_add_data(s_id,s_name,drug_id,drug_name,drug_quantity,drug_price)
                st.success("Successfully Added Data")

        if choice == "View":
            st.subheader("Drug Details")
            drug_result = supplier_view_data()
            with st.expander("View All Supplier Data"):
                drug_clean_df = pd.DataFrame(drug_result, columns=["Supplier ID", "Supplier Name", "Drug ID", "Drug Name", "Drug Quantity", "Drug Price"])
                st.dataframe(drug_clean_df)
        
        if choice == 'Update':
            st.subheader("Update Supplier Details")
            s_id = st.text_input("Supplier ID")
            s_name = st.text_input("Supplier Name")
            if st.button(label='Update'):
                supplier_update(s_name, s_id)
                st.success("Supplier Info Updated")

        if choice == 'Delete':
            st.subheader("Delete Supplier")
            s_id = st.text_input("Supplier ID")
            if st.button(label="Delete"):
                supplier_delete(s_id)
                st.success("Supplier Deleted")

    #INSIGHTS 
    elif choice == "Insights":
        st.subheader("DBMS Mini Project - Ananya N, Anirudh P S, Chandana B N")


###################################################################

def getauthenicate(username, password):
    c.execute('SELECT C_Password FROM Customers WHERE C_Name = ?', (username,))
    cust_password = c.fetchall()
    if cust_password[0][0] == password:
        return True
    else:
        return False

###################################################################

def customer(username, password):
    if getauthenicate(username, password):
        print("In Customer")
        st.title("Welcome to Pharmacy Store")
        st.subheader("Your Order Details")
        order_result = order_view_data(username)
        with st.expander("View All Order Data"):
            order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items", "Qty", "ID", "Price"])
            st.dataframe(order_clean_df)

        drug_result = drug_view_all_data()
        print(drug_result)

        # Dictionary to hold the quantity selected for each drug
        selected_quantities = {}

        for index, drug in enumerate(drug_result):
            drug_name = drug[0]
            drug_usage = drug[2]
            drug_image_path = f'images/{drug_name.lower().replace(" ", "")}.jpg'  # Assuming images are named like the drugs

            st.subheader(f"{drug_name}")

            try:
                img = Image.open(drug_image_path)
                st.image(img, width=200, caption=f"Expiry date: {drug[1]}")
            except FileNotFoundError:
                st.write(f"No image found for {drug_name}")

            st.write(f"When to use: {drug_usage}")
            st.subheader(f"₹ {drug[5]}")
            quantity = st.number_input(label=f"Quantity (Maximum 5):", min_value=0, max_value=5, key=index)
            st.markdown("---")
            selected_quantities[drug_name] = quantity

        print(selected_quantities)

        i = 0
        order_total = 0
        for value in selected_quantities.values():
            order_total += drug_result[i][5]*value
            i += 1
        print(order_total)

        if st.button(label="Order now"):
            st.subheader(f"Order Total: ₹ {order_total}")
            O_items = []
            O_Qty = []

            for drug_name, quantity in selected_quantities.items():
                if quantity > 0:
                    O_items.append(drug_name)
                    O_Qty.append(str(quantity))

            O_items_str = ",".join(O_items)
            O_Qty_str = ",".join(O_Qty)

            O_id = f"{username}#O{random.randint(0, 1000000)}"
            order_add_data(username, O_items_str, O_Qty_str, O_id, order_total)

###################################################################

if __name__ == '__main__':
    drug_create_table()
    cust_create_table()
    order_create_table()
    supplier_create_table()

    menu = ["Login", "Register", "Admin"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        username = st.sidebar.text_input("Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox(label="Login"):
            customer(username, password)

    elif choice == "Register":
        st.subheader("Create New Account")
        cust_name = st.text_input("Name")
        cust_password = st.text_input("Password", type='password', key=1000)
        cust_password1 = st.text_input("Confirm Password", type='password', key=1001)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            cust_email = st.text_input("Email ID")
        with col2:
            cust_area = st.text_input("State")
        with col3:
            cust_number = st.text_input("Phone Number")

        if st.button("Sign Up"):
            if (cust_password == cust_password1):
                customer_add_data(cust_name,cust_password,cust_email, cust_area, cust_number,)
                st.success("Account Created!")
                st.info("Go to Login Menu to login")
            else:
                st.warning('Passwords do not match')
                
    elif choice == "Admin":
        username = st.sidebar.text_input("Name")
        password = st.sidebar.text_input("Password", type='password')
        if username == 'admin' and password == 'admin':
            admin()