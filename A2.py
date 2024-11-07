from enum import Enum
from datetime import date
from collections import defaultdict

class Genre(Enum):
    FICTION= 0
    ROMANCE= 1
    MYSTERY= 2
    FANTASY= 3
    BIOGRAPHY= 4
    HISTORY= 5
    SELF_HELP= 6

class EBook:
    def __init__(self, title, author, publication_date, genre, price):
        self.__title= title
        self.__author= author
        self.__publication_date = publication_date
        self.__genre= genre
        self.__price= price
    #getters
    def get_title(self):
        return self.__title
    def get_author(self):
        return self.__author
    def get_publication_date(self):
        return self.__publication_date
    def get_genre(self):
        return self.__genre
    def get_price(self):
        return self.__price
    #setters
    def set_title(self, title):
        self.__title= title
    def set_author(self, author):
        self.__author = author
    def set_publication_date(self, publication_date):
        self.__publication_date= publication_date
    def set_genre(self, genre):
        self.__genre= genre
    def set_price(self, price):
        self.__price= price
    def __str__(self): #format ebook details into a readable string
        return f"EBook(title: {self.get_title()}, author: {self.get_author()}, genre: {self.get_genre().name}, price: {self.get_price()})"

class Customer:
    def __init__(self, name, email, mobile, is_loyalty_member):
        self.__name= name
        self.__email= email
        self.__mobile= mobile
        self.__is_loyalty_member= is_loyalty_member
    #getters
    def get_name(self):
        return self.__name
    def get_email(self):
        return self.__email
    def get_mobile(self):
        return self.__mobile
    def get_is_loyalty_member(self):
        return self.__is_loyalty_member
    #setters
    def set_name(self, name):
        self.__name= name
    def set_email(self, email):
        self.__email= email
    def set_mobile(self, mobile):
        self.__mobile= mobile
    def set_is_loyalty_member(self, is_loyalty_member):
        self.__is_loyalty_member= is_loyalty_member
    def update_account(self, name=None, email=None, mobile=None): #update the infromation, if the custmoer wants to change them
        if name:
            self.set_name(name)
        if email:
            self.set_email(email)
        if mobile:
            self.set_mobile(mobile)
    def delete_account(self): #set all attributes to none and false if the user want
        self.__name= None
        self.__email= None
        self.__mobile= None
        self.__is_loyalty_member= False
    def __str__(self):
        return f"Customer(name: {self.get_name()}, email: {self.get_email()}, loyalty_member: {self.get_is_loyalty_member()})"
class ShoppingCart:  #define shopping cart class for cart management
    def __init__(self, cart_items={}):
        self.__cart_items = defaultdict(int)  #using defaultdict to handle new keys automatically
    #getters & settrs
    def get_cart_items(self):
        return self.__cart_items
    def set_cart_items(self, cart_items):
        self.__cart_items= cart_items
    #add ebook to cart with quantity
    def add_to_cart(self, ebook, quantity=1):
        self.__cart_items[ebook] += quantity
    def remove_from_cart(self, ebook):  #remove book from cart
        cart_items= self.get_cart_items()  #get current cart items
        if ebook in cart_items:  #check if ebook is in cart
            del cart_items[ebook]  #delet ebook from cart
        self.set_cart_items(cart_items)  #update cart without deleted item
    def update_quantity(self, ebook, quantity):  #update qunatity of an ebook
        cart_items= self.get_cart_items()  #get current cart items
        if ebook in cart_items:  #check if book is in cart
            cart_items[ebook] = quantity  #update quantity for ebook
        self.set_cart_items(cart_items)  #update cart with new quantity
    def calculate_total(self): #total wihtou discount
        return sum(map(lambda item: item[0].get_price() * item[1], self.__cart_items.items()))
    def __str__(self):
        cart= "Shopping Cart:\nItems:\n" #initialize a string to hold cart items
        for ebook, quantity in self.get_cart_items().items(): #loop through each item in the cart ebook as key and quantity as value
            cart += (f"EBook(title: {ebook.get_title()}, "f"author: {ebook.get_author()}, "f"genre: {ebook.get_genre().name}, "f"price: {ebook.get_price()}, "f"quantity: {quantity})\n") #format each ebook's details and add it to cart
        return cart #return the complete cart representation
class Order:
    def __init__(self, order_id, customer, cart, order_date=date.today(), total_amount=0):
        self.__order_id= order_id
        self.__customer= customer
        self.__cart= cart
        self.__order_date= order_date
        self.__total_amount= total_amount
    #getters
    def get_order_id(self):
        return self.__order_id
    def get_customer(self):
        return self.__customer
    def get_cart(self):
        return self.__cart
    def get_order_date(self):
        return self.__order_date
    def get_total_amount(self):
        return self.__total_amount
    #setters
    def set_order_id(self, order_id):
        self.__order_id= order_id
    def set_customer(self, customer):
        self.__customer= customer
    def set_cart(self, cart):
        self.__cart= cart
    def set_order_date(self, order_date):
        self.__order_date= order_date
    def set_total_amount(self, amount):
        self.__total_amount= amount
    def calculate_total(self):  #calculate total for order with discounts
        total= self.get_cart().calculate_total()  # Start with the cart's total (wihtou discount)
        if self.get_customer().get_is_loyalty_member():  #check if customer is loyalty member
            total *= 0.90  #apply 10% discount
        total_items =sum(self.get_cart().get_cart_items().values())  #get total items
        if total_items >= 5:  #check if total items meet bulk discount criteria
            total *= 0.80  #apply 20% discount
        self.set_total_amount(total)  #set final total amount
        return total  #return calculated total
    def __str__(self):
        # Use ShoppingCart's __str__ method directly for displaying items
        return (f"Order Summary:\n"
                f"Order ID: {self.get_order_id()}\n"
                f"Customer: {self.get_customer().get_name()}\n"
                f"Order Date: {self.get_order_date()}\n"
                f"{self.get_cart()}"  # Uses ShoppingCart's __str__ method for items
                f"Total Amount (before VAT): {self.get_total_amount()}\n")

class Invoice:
    def __init__(self, order, vat_rate=0.08, vat_amount=0, total=0):
        self.__order = order
        self.__vat_rate = vat_rate
        self.__vat_amount = vat_amount
        self.__total = total
    def get_order(self):
        return self.__order
    def get_vat_rate(self):
        return self.__vat_rate
    def get_vat_amount(self):
        return self.__vat_amount
    def get_total(self):
        return self.__total
    #setters
    def set_order(self, order):
        self.__order= order
    def set_vat_rate(self, vat_rate):
        self.__vat_rate= vat_rate
    def set_vat_amount(self, vat_amount):
        self.__vat_amount= vat_amount
    def set_total(self, total):
        self.__total= total
    def calculate_invoice(self):  # calculate total and VAT for invoice
        order_total= self.get_order().calculate_total()  # get order total
        vat_amount= order_total * self.get_vat_rate()  # calculate VAT amount
        self.set_vat_amount(vat_amount)  # set VAT amount
        final_total= order_total + self.get_vat_amount()  # final total
        self.set_total(final_total)  # set the final
    def __str__(self):
        return (f"Invoice for Order ID: {self.get_order().get_order_id()}\n" f"Customer: {self.get_order().get_customer().get_name()}\n" f"Order Total (before VAT): {self.get_order().get_total_amount()}\n" f"VAT Rate: {self.get_vat_rate() * 100}%\n" f"VAT Amount: {self.get_vat_amount()}\n" f"Total (with VAT): {self.get_total()}\n")

class EBookStore:
    def __init__(self, name, customers=None, orders=None):
        self.__name = name
        self.__catalog = self.default_catalog()  # call method to set default catalog
        self.__customers = self.assign_customers(customers)  # assign customers
        self.__orders = self.assign_orders(orders)  # Assign orders
    def get_name(self):
        return self.__name
    def get_catalog(self):
        return self.__catalog
    def get_customers(self):
        return self.__customers
    def get_orders(self):
        return self.__orders
    #setter
    def set_name(self, name):
        self.__name= name
    def set_catalog(self, catalog):
        self.__catalog= catalog or self.default_catalog()
    def set_customers(self, customers):
        self.__customers= self.assign_customers(customers)
    def set_orders(self, orders):
        self.__orders= self.assign_orders(orders)
    # a comprehensive catalog of the store’s available e-books
    def default_catalog(self):
        return [EBook("The Art of War", "Sun Tzu", "2023-01-01", Genre.HISTORY, 10.0),
                EBook("Meditations", "Marcus Aurelius", "2023-01-01", Genre.BIOGRAPHY, 12.0),
                EBook("To Kill a Mockingbird", "Harper Lee", "1960-07-11", Genre.FICTION, 15.0),
                EBook("Pride and Prejudice", "Jane Austen", "1813-01-28", Genre.ROMANCE, 8.0),
                EBook("1984", "George Orwell", "1949-06-08", Genre.FICTION, 9.0),
                EBook("The Great Gatsby", "F. Scott Fitzgerald", "1925-04-10", Genre.FICTION, 10.0),
                EBook("The Catcher in the Rye", "J.D. Salinger", "1951-07-16", Genre.FICTION, 7.0),
                EBook("The Hobbit", "J.R.R. Tolkien", "1937-09-21", Genre.FANTASY, 12.0),
                EBook("Harry Potter", "J.K. Rowling", "1997-06-26", Genre.FANTASY, 15.0),
                EBook("The Alchemist", "Paulo Coelho", "1988-01-01", Genre.FICTION, 10.0),
                EBook("The Little Prince", "Antoine de Saint-Exupéry", "1943-04-06", Genre.FICTION, 5.0),
                EBook("Sapiens", "Yuval Noah Harari", "2011-01-01", Genre.HISTORY, 18.0),
                EBook("Becoming", "Michelle Obama", "2018-11-13", Genre.BIOGRAPHY, 20.0),
                EBook("The Power of Now", "Eckhart Tolle", "1997-01-01", Genre.SELF_HELP, 10.0),
                EBook("Atomic Habits", "James Clear", "2018-10-16", Genre.SELF_HELP, 14.0),
                EBook("The Lean Startup", "Eric Ries", "2011-09-13", Genre.BIOGRAPHY, 16.0),
                EBook("The 7 Habits of Highly Effective People", "Stephen Covey", "1989-08-15", Genre.SELF_HELP, 12.0),
                EBook("Man's Search for Meaning", "Viktor Frankl", "1946-01-01", Genre.BIOGRAPHY, 9.0),
                EBook("Thinking, Fast and Slow", "Daniel Kahneman", "2011-10-25", Genre.SELF_HELP, 14.0),
                EBook("Last Child", "Mark Manson", "2016-09-13", Genre.SELF_HELP, 10.0)]
    #assign customers list or empty list if None
    def assign_customers(self, customers):
        return customers or []
    def assign_orders(self, orders):
        return orders or []
    def add_customer(self, customer):  # to add a customer to the store
        if customer not in self.get_customers():  # check if customer is not already in the list
            customers = self.get_customers()  # get current customers list
            customers.append(customer)  # add customer to the list
            self.set_customers(customers)  # update customers list
        else:  # if customer is already in the list
            print(f"Customer '{customer.get_name()}' is already registered.")
    def create_order(self, customer, cart):  #to create a new order
        order_id= len(self.get_orders()) + 1  # generate unique ID
        order= Order(order_id, customer, cart)  #create a new order with ID, customer, and cart
        order.calculate_total()  #calculate total with any discounts
        orders= self.get_orders()  #get current orders list
        orders.append(order)  #add new order to orders list
        self.set_orders(orders)  #update orders list
        invoice= Invoice(order)  #create an invoice for the order
        invoice.calculate_invoice()  #calculate invoice total with VAT
        return order  #return created order
    def list_catalog(self):  #to list all ebooks in the catalog
        if not self.get_catalog():  #check if catalog is empty
            print("The catalog is currently empty.")  #notify catalog is empty
        else:  #if catalog has ebooks
            print("E-Books Catalog")  #title for catalog list
            for ebook in self.get_catalog():  #loop through each ebook in catalog
                print(ebook)  #print ebook details


def test_with_user_inputs(): #test cases with user's input below there is function that testing the code without using input
    store = EBookStore("The Great Ebooks Store")  # create eBook store object
    print("Welcome to the Great E-books Store!")

    name= None  # Initialize name to None, to be set by user input
    email= None
    mobile= None
    is_loyalty_member= False
    #get the customer’s name
    while name is None:  #loop until enter a name
        print("Enter Custmoer infromation")
        name= input("Enter your name: ").strip()
        if not name:  # check if name empty
            print("Name cannot be empty. Please enter a valid name.")
            name= None  #assing None to name to repeat the loop

    #get the customer’s email
    while email is None:  #repeat until a valid email is provided
        email= input("Enter your email: ").strip()
        if not email:  # check if email empty
            print("Email cannot be empty. Please enter a valid email.")
            email= None  #assign None to email to repeat the loop

    #get the customer’s mobile number
    while mobile is None:
        mobile_input= input("Enter your mobile number: ").strip()  # ask for mobile number
        if mobile_input.isdigit():  #check if input is a nmber
            mobile = int(mobile_input)  #store in mobile
        else:
            print("Error: Mobile number must be a valid integer.")

    #get loyalty membership status
    while True:
        is_loyalty_member_input= input("Are you a loyalty member? (yes/no): ").strip().lower()
        if is_loyalty_member_input == "yes":  #If input is yes
            is_loyalty_member= True  # et loyalty status to true
            break  #stop looping
        elif is_loyalty_member_input == "no":  # if input is no
            is_loyalty_member= False  #set loyatly status to false
            break  # stop looping
        else:
            print("Input must be 'yes' or 'no'.")

    #create customer and add to store
    try:
        customer = Customer(name, email, mobile, is_loyalty_member)  #customer object
        store.add_customer(customer)  #add customer to the store's customer List
        print(f"Customer '{customer.get_name()}' added to the store")
    except Exception as e:
        print(f"Error creating account: {e}")  #if failed
    try:
        while True:
            action = input("Would you like to manage your account? (update/delete/continue): ").strip().lower()
            if action == "update":  #if enter update
                name= input("Enter new name (leave blank to keep current): ").strip()
                email= input("Enter new email (leave blank to keep current): ").strip()
                mobile= input("Enter new mobile (leave blank to keep current): ").strip()

                #Convert mobile to integer if provided and valid
                if mobile:  #mobile will be equal to below
                    try:
                        mobile= int(mobile)
                    except ValueError:
                        print("Mobile number must be an integer.")
                        mobile = None #set mobile to none
                customer.update_account(name or None, email or None, mobile or None)
                print("Account updated successfully.")

            elif action == "delete":  #action will be equal to below
                confirm= input("Are you sure you want to delete your account? (yes/no): ").strip().lower()
                if confirm == "yes":  #if confirm = yes, delete and stop the programm
                    customer.delete_account()
                    print("Your account has been deleted.")
                    exit()  #exit after account deletion
            elif action == "continue":
                break  #Exit account management to continue shopping
            else:
                print("Invalid option. Please choose 'update', 'delete', or 'continue'.")

    except Exception as e:
        print(f"An error occurred while managing your account: {e}")
    finally:
        print("Thank you for creating account with us!")
    cart= ShoppingCart()  #create an empty shopping cart for the customer

    #books to cart
    while True:
        add_to_cart= input("Would you like to add a book to your cart? (yes/no): ").strip().lower()
        if add_to_cart == "no":  #stop if user enters "no"
            break
        elif add_to_cart != "yes":  #Error if input is invalid
            print("Error: Input must be 'yes' or 'no'.")
            continue
        store.list_catalog()  #Display catalog of available books

        title= input("Enter the title of the book you want to add: ").strip()

        #find the book in the catalog
        selected_ebook = None
        for ebook in store.get_catalog():  #loop through each book in the catalog
            if ebook.get_title().lower() == title.lower():  # check if the title matches
                selected_ebook = ebook  # set selected book
                break  #stop looping once the book is found
        if selected_ebook is None:  # if book is not found, notify user and start over
            print("Sorry, that book is not available in the catalog.")
            continue
        #ask for the quantity to add to the cart
        quantity= None  #initialize quantity as None To set it by the user
        while quantity is None:
            quantity_input= input(f"Enter the quantity for '{selected_ebook.get_title()}': ").strip()
            if quantity_input.isdigit() and int(quantity_input) > 0:  #must be number and positive integer
                quantity = int(quantity_input)  #store it in quantity
            else:
                print("Quantity must be a positive integer.")

        cart.add_to_cart(selected_ebook, quantity)  #add the selected book and quantity to the cart
        print(f"'{selected_ebook.get_title()}' added to your cart.")

    #check if the cart has items before proceeding to checkout
    if not cart.get_cart_items():  # if cart is empty
        print("Your cart is empty. Exiting the checkout process.")
        exit()  # shoutdown
    #view and update cart or proceed to checkout
    while True:
        action= input(
            "Would you like to update or remove items from your cart? (update/remove/checkout): ").strip().lower()
        if action == "checkout":  #if checkout is selected
            break  #eixt the loop to proceed to checkout
        elif action not in ["update", "remove"]:  # check the input
            print("Invalid option. Choose 'update', 'remove', or 'checkout'.")
            continue

        title = input("Enter the tilte of the book you want to update/remove: ").strip()

        #find the book in the cart that matche the title
        ebook = None
        for item in cart.get_cart_items():  #loop through each book in the cart
            if item.get_title().lower() == title.lower():  #if title matches
                ebook= item  #set the matched book
                break  # break once the book is found
        #if book is not found in the cart
        if ebook is None:
            print("That book is not in your cart.")
            continue  #next action
        #if user choose to update the quantity
        if action == "update":
            new_quantity = None  #initialize new quantity as None
            while new_quantity is None:  #repeat until a valid quantity is provided
                new_quantity_input= input(f"Enter the new quantity for '{ebook.get_title()}': ").strip()
                if new_quantity_input.isdigit() and int(new_quantity_input) > 0:  #check positive integer
                    new_quantity= int(new_quantity_input)  #set new quantity
                else:
                    print("Quantity must be a positive integer.")  # erro

            cart.update_quantity(ebook, new_quantity)  #update quantity in cart
            print(f"Updated '{ebook.get_title()}' quantity to {new_quantity}.")  # Confirm update
        #if user choose to remove the book from the cart
        elif action == "remove":
            cart.remove_from_cart(ebook)  #remove book from cart
            print(f"Removed '{ebook.get_title()}' from your cart.")
    #create an order and generate an invoice
    try:
        print("Processing your order")
        order = store.create_order(customer, cart)  #order object with customer and cart details

        #display Order details
        print("here is your final order summary:")
        print(order)

        print("Here is your invoice:")
        invoice= Invoice(order)  #create invoice from order details
        invoice.calculate_invoice()  #calculate total with VAT
        print(invoice)  #display invoice details
    except Exception as e:
        print(f"An error occurred while processing the order: {e}")
    finally:
        print("Thank you for shopping with us!")

test_with_user_inputs()

def test_without_user_inputs():
    print("_____________________________________________________________________________")
    print("             Testing code functionality without user's inputs")
    store= EBookStore("The Great Ebooks Store") #create store object
    print("Welcome to the Great E-books Store!")
    print("Here is the catalog of available e-books:")
    store.list_catalog() #display catalog
    #register a customer and add them to the store
    customer= Customer( name="Sife", email="sife_saleh@gmail.com", mobile=502222103, is_loyalty_member=True)
    store.add_customer(customer)
    print(f"Customer '{customer.get_name()}' added to the store")
    #Update the customer's account information
    customer.update_account(name="Abdulla", email="Abdulla@hotmail.com", mobile=502999111)
    print(f"Updated customer info: {customer}")
    #delete the customer account and check the deletion
    customer.delete_account()
    print(f"Customer account after deletion: {customer}")
    #re-register the customer for order testing
    customer= Customer(name="Ali",email="Ali@gmail.com",mobile=551229338,is_loyalty_member=True)
    store.add_customer(customer)
    print(f"Customer '{customer.get_name()}' re-added to the store")
    #initialize a shopping cart and add books to the cart directly
    cart = ShoppingCart()
    print("Adding books to the cart without user input...")
    #select books from catalog and add to cart
    catalog = store.get_catalog()
    cart.add_to_cart(catalog[1], 2)  #add 2 copies of the second book
    cart.add_to_cart(catalog[3], 1)
    cart.add_to_cart(catalog[4], 3)
    #update the quantity of an item in the cart
    cart.update_quantity(catalog[1], 5)  #update to 5 copies of the second book
    print("updated cart items:")
    print(cart)
    #remove an item from the cart
    cart.remove_from_cart(catalog[3])  #remove the fourth book from the cart
    print("Cart after removing one item:")
    print(cart)
    #create an order and calculate total with discounts
    print("Processing order...")
    order= store.create_order(customer, cart)
    print("Here is your final order summary:")
    print(order)
    #generate and print the invoice
    invoice = Invoice(order)
    invoice.calculate_invoice()
    print("Here is your invoice:")
    print(invoice)

test_without_user_inputs()