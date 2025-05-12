import tkinter as tk
from tkinter import ttk, messagebox, font
from enum import Enum
from datetime import datetime
import pickle
import os
import re
import random
import uuid

# =================================================================
# ENUM CLASSES
# =================================================================

# This Enum defines types of payment methods users can choose from
class PaymentType(Enum):
    CREDIT_CARD = "Credit Card" # Paying with a credit card
    DIGITAL = "Digital" # Paying using digital methods like PayPal

# This Enum defines the result of a payment transaction
class PaymentTransactionStatus(Enum):
    SUCCESSFUL = "Successful" # Payment was successful
    FAILED = "Failed" # Payment failed
    PENDING = "Pending" # Payment is still processing

# This Enum defines the current status of a user's account
class AccountStatus(Enum):
    ACTIVE = "Active" # Account is active and usable
    INACTIVE = "Inactive" # Account exists but is not currently in use
    SUSPENDED = "Suspended" # Account has been temporarily blocked

# This Enum defines the status of a booking
class BookingStatus(Enum):
    PENDING = "Pending" # Booking request is waiting for confirmation
    CONFIRMED = "Confirmed" # Booking is confirmed
    CANCELLED = "Cancelled" # Booking has been cancelled

# This Enum defines the types of credit cards accepted
class CardType(Enum):
    VISA = "Visa"
    MASTERCARD = "MasterCard"
    AMEX = "Amex"

# =================================================================
# FILE OPERATIONS
# =================================================================

# Dictionary to store file paths for different data types
DATA_FILES = {
    'users': 'users.pkl',
    'customers': 'customers.pkl',
    'admins': 'admins.pkl',
    'events': 'events.pkl',
    'bookings': 'bookings.pkl',
    'tickets': 'tickets.pkl',
    'payments': 'payments.pkl',
    'discounts': 'discounts.pkl'
}

# Function to save data to a pickle file
def save_data(data, file_key):
    # Create a data directory if it does not exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Save the data to the corresponding file
    filepath = os.path.join('data', DATA_FILES[file_key])
    with open(filepath, 'wb') as file:
        pickle.dump(data, file)

# Function to load data from a pickle file
def load_data(file_key):
    filepath = os.path.join('data', DATA_FILES[file_key])
    
    # If the file exists, load and return the data
    if os.path.exists(filepath):
        try:
            with open(filepath, 'rb') as file:
                return pickle.load(file)
        except Exception as e:
            print("Error loading data: " + str(e))
            return []
    # If the file does not exist return an empty list
    return []

# =================================================================
# CORE CLASSES IMPLEMENTATION
# =================================================================

# Base class for any user in the system
class User:
    def __init__(self, user_name, user_id, user_password, user_email, registration_date):
        self._user_name = user_name # Name of the user
        self._user_id = user_id # Unique ID for the user
        self._user_password = user_password # User password should be encrypted
        self._user_email = user_email # Email address of the user
        self._registration_date = registration_date # Date user registered
    
    # Show user information
    def display_user_info(self):
        return "User: " + self._user_name + ", ID: " + str(self._user_id) + ", Email: " + self._user_email + ", Registered: " + str(self._registration_date)
    
    # Method to simulate a user requesting a special service
    def request_special_service(self):
        print(self._user_name + " requested a special service.")
    
    # Method to simulate user giving feedback
    def provide_feedback(self, feedback):
        print(self._user_name + " provided feedback: " + feedback)
    
    # Getters and setters for user attributes
    def get_user_name(self): return self._user_name
    def set_user_name(self, user_name): self._user_name = user_name
    
    def get_user_id(self): return self._user_id
    def set_user_id(self, user_id): self._user_id = user_id
    
    def get_user_password(self): return self._user_password
    def set_user_password(self, user_password): self._user_password = user_password
    
    def get_user_email(self): return self._user_email
    def set_user_email(self, user_email): self._user_email = user_email
    
    def get_registration_date(self): return self._registration_date
    def set_registration_date(self, registration_date): self._registration_date = registration_date

# Represents a customer inherits from User
class Customer(User):
    def __init__(self, user_name, user_id, user_password, user_email, registration_date, customer_address, customer_phone, payment_info):
        super().__init__(user_name, user_id, user_password, user_email, registration_date)
        self._customer_address = customer_address # Customer home or billing address
        self._customer_phone = customer_phone # Contact number
        self._payment_info = payment_info # Information about payment methods
    
    # Show customer details
    def display_customer_info(self):
        return self.display_user_info() + ", Address: " + self._customer_address + ", Phone: " + str(self._customer_phone) + ", Payment Info: " + self._payment_info
    
    # Getters and setters
    def get_customer_address(self): return self._customer_address
    def set_customer_address(self, customer_address): self._customer_address = customer_address
    
    def get_customer_phone(self): return self._customer_phone
    def set_customer_phone(self, customer_phone): self._customer_phone = customer_phone
    
    def get_payment_info(self): return self._payment_info
    def set_payment_info(self, payment_info): self._payment_info = payment_info

# Represents an admin user inherit from User
class Admin(User):
    def __init__(self, user_name, user_id, user_password, user_email, registration_date, admin_role, employee_id, account_status):
        super().__init__(user_name, user_id, user_password, user_email, registration_date)
        self._admin_role = admin_role # Role of the admin e.g Manager
        self._employee_id = employee_id # ID number assigned to employee
        self._account_status = account_status # Current status of the admin's account
    
    # Show admin details
    def display_admin_info(self):
        return self.display_user_info() + ", Role: " + self._admin_role + ", Employee ID: " + str(self._employee_id) + ", Account Status: " + self._account_status.value
    
    # Getters and setters
    def get_admin_role(self): return self._admin_role
    def set_admin_role(self, admin_role): self._admin_role = admin_role
    
    def get_employee_id(self): return self._employee_id
    def set_employee_id(self, employee_id): self._employee_id = employee_id
    
    def get_account_status(self): return self._account_status
    def set_account_status(self, account_status): self._account_status = account_status

# Class that represents a general payment made by a user
class Payment:
    def __init__(self, booking_id, payment_id, payment_type, transaction_date, transaction_status, refund_id=None, refund_reason=""):
        # Store all the payment details
        self._booking_id = booking_id # ID of the booking this payment is for
        self._payment_id = payment_id # Unique ID of the payment
        self._payment_type = payment_type # Type of payment Digital or Credit Card
        self._transaction_date = transaction_date # Date the payment was made
        self._transaction_status = transaction_status # Status of the payment Success, Failed, etc
        self._refund_id = refund_id # Optional refund ID if refunded
        self._refund_reason = refund_reason # Reason for the refund if any
    
    # Show payment information in a readable format
    def display_payment_info(self):
        return "Payment ID: " + str(self._payment_id) + ", Booking ID: " + str(self._booking_id) + ", Type: " + self._payment_type.value + ", Date: " + str(self._transaction_date) + ", Status: " + self._transaction_status.value + ", Refund ID: " + str(self._refund_id) + ", Reason: " + self._refund_reason
    
    # Return the payment details as a dictionary key value pairs
    def get_payment_details(self):
        return {
            "payment_id": self._payment_id,
            "booking_id": self._booking_id,
            "payment_type": self._payment_type,
            "transaction_date": self._transaction_date,
            "transaction_status": self._transaction_status,
            "refund_id": self._refund_id,
            "refund_reason": self._refund_reason,
        }
    
    # Get and set methods for each private attribute
    def get_payment_id(self): return self._payment_id
    def set_payment_id(self, payment_id): self._payment_id = payment_id
    
    def get_booking_id(self): return self._booking_id
    def set_booking_id(self, booking_id): self._booking_id = booking_id
    
    def get_payment_type(self): return self._payment_type
    def set_payment_type(self, payment_type): self._payment_type = payment_type
    
    def get_transaction_date(self): return self._transaction_date
    def set_transaction_date(self, transaction_date): self._transaction_date = transaction_date
    
    def get_transaction_status(self): return self._transaction_status
    def set_transaction_status(self, transaction_status): self._transaction_status = transaction_status
    
    def get_refund_id(self): return self._refund_id
    def set_refund_id(self, refund_id): self._refund_id = refund_id
    
    def get_refund_reason(self): return self._refund_reason
    def set_refund_reason(self, refund_reason): self._refund_reason = refund_reason

# Class for handling digital payments like PayPal, Apple Pay
class DigitalPayment(Payment):
    def __init__(self, booking_id, payment_id, transaction_id, account_identifier, authorization_code, transaction_date, transaction_status):
        # Call the Payment class constructor and set digital specific values
        super().__init__(booking_id, payment_id, PaymentType.DIGITAL, transaction_date, transaction_status)
        self._transaction_id = transaction_id # ID from the payment processor like PayPal
        self._account_identifier = account_identifier # Account email or username used for payment
        self._authorization_code = authorization_code # Code confirming authorization
    
    # Show all details about the digital payment
    def display_digital_payment_info(self):
        return self.display_payment_info() + ", Transaction ID: " + str(self._transaction_id) + ", Account: " + self._account_identifier + ", Auth Code: " + self._authorization_code
    
    # Getters and setters for digital payment fields
    def get_transaction_id(self): return self._transaction_id
    def set_transaction_id(self, transaction_id): self._transaction_id = transaction_id
    
    def get_account_identifier(self): return self._account_identifier
    def set_account_identifier(self, account_identifier): self._account_identifier = account_identifier
    
    def get_authorization_code(self): return self._authorization_code
    def set_authorization_code(self, authorization_code): self._authorization_code = authorization_code

# Class for credit card payments
class CreditCard(Payment):
    def __init__(self, booking_id, payment_id, card_number, expiry_date, card_type, transaction_date, transaction_status):
        # Call the Payment constructor and set credit card specific fields
        super().__init__(booking_id, payment_id, PaymentType.CREDIT_CARD, transaction_date, transaction_status)
        self._card_number = card_number # Credit card number should be stored securely
        self._expiry_date = expiry_date # Card expiration date
        self._card_type = card_type # Visa, MasterCard, etc
    
    # Show all credit card payment details
    def display_credit_card_info(self):
        return self.display_payment_info() + ", Card Number: " + self._card_number + ", Expiry: " + self._expiry_date + ", Type: " + self._card_type.value
    
    # Getters and setters for credit card details
    def get_card_number(self): return self._card_number
    def set_card_number(self, card_number): self._card_number = card_number
    
    def get_expiry_date(self): return self._expiry_date
    def set_expiry_date(self, expiry_date): self._expiry_date = expiry_date
    
    def get_card_type(self): return self._card_type
    def set_card_type(self, card_type): self._card_type = card_type

# Represents a booking for an event
class Booking:
    def __init__(self, user_id, event_id, booking_id, booking_date, number_of_tickets,
                 total_price, booking_status):
        # Initialize booking details
        self._user_id = user_id # ID of the user making the booking
        self._event_id = event_id # ID of the event
        self._booking_id = booking_id # Unique ID for the booking
        self._booking_date = booking_date # Date the booking was made
        self._number_of_tickets = number_of_tickets # Number of tickets booked
        self._total_price = total_price # Total price for the booking
        self._booking_status = booking_status # Status of the booking e.g confirmed, cancelled
        self._list_reservation = [] # List to hold reservations associated with the booking
    
    # Returns a formatted string of booking information
    def display_booking_info(self):
        return "Booking ID: " + str(self._booking_id) + ", User ID: " + str(self._user_id) + ", Event ID: " + str(self._event_id) + ", Date: " + str(self._booking_date) + ", Tickets: " + str(self._number_of_tickets) + ", Total Price: " + str(self._total_price) + ", Status: " + self._booking_status.value
    
    # Getter and setter methods for each attribute
    def get_user_id(self): return self._user_id
    def set_user_id(self, user_id): self._user_id = user_id
    
    def get_event_id(self): return self._event_id
    def set_event_id(self, event_id): self._event_id = event_id
    
    def get_booking_id(self): return self._booking_id
    def set_booking_id(self, booking_id): self._booking_id = booking_id
    
    def get_booking_date(self): return self._booking_date
    def set_booking_date(self, booking_date): self._booking_date = booking_date
    
    def get_number_of_tickets(self): return self._number_of_tickets
    def set_number_of_tickets(self, number_of_tickets): self._number_of_tickets = number_of_tickets
    
    def get_total_price(self): return self._total_price
    def set_total_price(self, total_price): self._total_price = total_price
    
    def get_booking_status(self): return self._booking_status
    def set_booking_status(self, booking_status): self._booking_status = booking_status
    
    def get_list_reservation(self): return self._list_reservation
    def set_list_reservation(self, list_reservation): self._list_reservation = list_reservation

# Represents a discount applied to a booking or ticket
class Discount:
    def __init__(self, discount_id, discount_percentage, discount_amount, discount_code,
                 max_discount_amount):
        self._discount_id = discount_id # Unique ID for the discount
        self._discount_percentage = discount_percentage # Percentage discount
        self._discount_amount = discount_amount # Flat amount discount
        self._discount_code = discount_code # Code used to apply the discount
        self._max_discount_amount = max_discount_amount # Max discount value allowed
    
    # Display discount information
    def display_discount_info(self):
        return "Discount ID: " + str(self._discount_id) + ", Percentage: " + str(self._discount_percentage) + "%, Amount: $" + str(self._discount_amount) + ", Code: " + self._discount_code + ", Max: $" + str(self._max_discount_amount)
    
    # Apply the discount to a price
    def apply_discount(self, original_price):
        # Calculate discount
        percentage_discount = original_price * (self._discount_percentage / 100)
        total_discount = percentage_discount + self._discount_amount
        
        # Ensure discount does not exceed maximum allowed
        if total_discount > self._max_discount_amount:
            total_discount = self._max_discount_amount
        
        # Return the discounted price
        return original_price - total_discount
    
    # Getter and setter methods
    def get_discount_id(self): return self._discount_id
    def set_discount_id(self, discount_id): self._discount_id = discount_id
    
    def get_discount_percentage(self): return self._discount_percentage
    def set_discount_percentage(self, discount_percentage): self._discount_percentage = discount_percentage
    
    def get_discount_amount(self): return self._discount_amount
    def set_discount_amount(self, discount_amount): self._discount_amount = discount_amount
    
    def get_discount_code(self): return self._discount_code
    def set_discount_code(self, discount_code): self._discount_code = discount_code
    
    def get_max_discount_amount(self): return self._max_discount_amount
    def set_max_discount_amount(self, max_discount_amount): self._max_discount_amount = max_discount_amount

# Represents a basic ticket for an event
class Ticket:
    def __init__(self, type_id, booking_id, ticket_id, seat_number, ticket_price, check_in_time, event_id=None):
        self._type_id = type_id # Type of ticket could be general, VIP, etc
        self._booking_id = booking_id # Associated booking ID
        self._ticket_id = ticket_id # Unique ticket ID
        self._seat_number = seat_number # Seat assigned to the ticket
        self._ticket_price = ticket_price # Price of the ticket
        self._check_in_time = check_in_time # Check-in time for the ticket holder
        self._event_id = event_id # ID of the event this ticket belongs to
    
    # Returns formatted ticket info
    def display_ticket_info(self):
        return "Ticket ID: " + str(self._ticket_id) + ", Booking ID: " + str(self._booking_id) + ", Seat: " + str(self._seat_number) + ", Price: " + str(self._ticket_price) + ", Check-in Time: " + str(self._check_in_time) + ", Event ID: " + str(self._event_id)
    
    # Getter and setter methods
    def get_type_id(self): return self._type_id
    def set_type_id(self, type_id): self._type_id = type_id
    
    def get_booking_id(self): return self._booking_id
    def set_booking_id(self, booking_id): self._booking_id = booking_id
    
    def get_ticket_id(self): return self._ticket_id
    def set_ticket_id(self, ticket_id): self._ticket_id = ticket_id
    
    def get_seat_number(self): return self._seat_number
    def set_seat_number(self, seat_number): self._seat_number = seat_number
    
    def get_ticket_price(self): return self._ticket_price
    def set_ticket_price(self, ticket_price): self._ticket_price = ticket_price
    
    def get_check_in_time(self): return self._check_in_time
    def set_check_in_time(self, check_in_time): self._check_in_time = check_in_time
    
    def get_event_id(self): return self._event_id
    def set_event_id(self, event_id): self._event_id = event_id

# Represents a group discounted ticket inherits from Ticket
class GroupDiscount(Ticket):
    def __init__(self, type_id, booking_id, ticket_id, seat_number, ticket_price, check_in_time,
                 group_id, group_count, group_gifts, event_id):
        super().__init__(type_id, booking_id, ticket_id, seat_number, ticket_price, check_in_time, event_id)
        self._group_id = group_id # ID of the group
        self._group_count = group_count # Number of people in the group
        self._group_gifts = group_gifts # Gifts provided to the group
    
    # Displays ticket + group discount info
    def display_group_discount_info(self):
        return self.display_ticket_info() + ", Group ID: " + str(self._group_id) + ", Group Count: " + str(self._group_count) + ", Group Gifts: " + self._group_gifts
    
    # Getter/setter for additional attribute
    def get_group_id(self): return self._group_id
    def set_group_id(self, group_id): self._group_id = group_id
    
    def get_group_count(self): return self._group_count
    def set_group_count(self, group_count): self._group_count = group_count
    
    def get_group_gifts(self): return self._group_gifts
    def set_group_gifts(self, group_gifts): self._group_gifts = group_gifts

# Represents a season membership ticket inherit from Ticket
class SeasonMembership(Ticket):
    def __init__(self, type_id, booking_id, ticket_id, seat_number, ticket_price, check_in_time, member_id, member_name, included_gifts, event_id):
        super().__init__(type_id, booking_id, ticket_id, seat_number, ticket_price, check_in_time, event_id)
        self._member_id = member_id # Unique member ID
        self._member_name = member_name # Member full name
        self._included_gifts = included_gifts # Gifts included in membership
    
    def display_season_membership_info(self):
        return self.display_ticket_info() + ", Member ID: " + str(self._member_id) + ", Name: " + self._member_name + ", Included Gifts: " + self._included_gifts
    
    def get_member_id(self): return self._member_id
    def set_member_id(self, member_id): self._member_id = member_id
    
    def get_member_name(self): return self._member_name
    def set_member_name(self, member_name): self._member_name = member_name
    
    def get_included_gifts(self): return self._included_gifts
    def set_included_gifts(self, included_gifts): self._included_gifts = included_gifts

# Represents a single-race access pass inherits from Ticket
class SingleRacePass(Ticket):
    def __init__(self, type_id, booking_id, ticket_id, seat_number, ticket_price, check_in_time,
                 single_race_pass_id, pass_expiry, pass_benefits, event_id):
        super().__init__(type_id, booking_id, ticket_id, seat_number, ticket_price, check_in_time, event_id)
        self._single_race_pass_id = single_race_pass_id # Unique ID for the pass
        self._pass_expiry = pass_expiry # Expiration date/time of the pass
        self._pass_benefits = pass_benefits # Benefits included with the pass
    
    def display_single_race_pass_info(self):
        return self.display_ticket_info() + ", Pass ID: " + str(self._single_race_pass_id) + ", Expiry: " + self._pass_expiry + ", Benefits: " + self._pass_benefits
    
    # Getter/setters
    def get_single_race_pass_id(self): return self._single_race_pass_id
    def set_single_race_pass_id(self, single_race_pass_id): self._single_race_pass_id = single_race_pass_id
    
    def get_pass_expiry(self): return self._pass_expiry
    def set_pass_expiry(self, pass_expiry): self._pass_expiry = pass_expiry
    
    def get_pass_benefits(self): return self._pass_benefits
    def set_pass_benefits(self, pass_benefits): self._pass_benefits = pass_benefits

# Represents a weekend package ticket with added benefits inherits from Ticket
class WeekendPackage(Ticket):
    def __init__(self, type_id, booking_id, ticket_id, seat_number, ticket_price, check_in_time,
                 package_id, package_type, package_benefits, event_id):
        super().__init__(type_id, booking_id, ticket_id, seat_number, ticket_price, check_in_time, event_id)
        self._package_id = package_id # ID of the package
        self._package_type = package_type # Type e.g deluxe, standard
        self._package_benefits = package_benefits # List of benefits included
    
    def display_weekend_package_info(self):
        return self.display_ticket_info() + ", Package ID: " + str(self._package_id) + ", Type: " + self._package_type + ", Benefits: " + self._package_benefits
    
    def get_package_id(self): return self._package_id
    def set_package_id(self, package_id): self._package_id = package_id
    
    def get_package_type(self): return self._package_type
    def set_package_type(self, package_type): self._package_type = package_type
    
    def get_package_benefits(self): return self._package_benefits
    def set_package_benefits(self, package_benefits): self._package_benefits = package_benefits

# Represents an event such as a Grand Prix race
class Event:
    # Initializes a new Event with details like name, ID, date, location, and capacity
    def __init__(self, event_name, event_id, event_date, event_location, event_capacity):
        self._event_name = event_name # Name of the event
        self._event_id = event_id # Unique identifier for the event
        self._event_date = event_date # Date of the event
        self._event_location = event_location # Location of the event
        self._event_capacity = event_capacity # Total number of tickets available
        self._list_user_tickets = [] # List to store Ticket objects for this event
        self._next_ticket_id = 1 # Simple way to generate unique ticket IDs for this event
    
    # Method to create a new ticket for this event
    def create_ticket(self, type_id, booking_id, seat_number, ticket_price, check_in_time):
        ticket_id = "TKT-" + str(self._event_id) + "-" + str(self._next_ticket_id)
        new_ticket = Ticket(type_id, booking_id, ticket_id, seat_number, ticket_price, check_in_time, self._event_id)
        self._list_user_tickets.append(new_ticket)
        self._next_ticket_id += 1
        return new_ticket
    
    # Returns a formatted string with the event's key information
    def display_event_info(self):
        return "Event: " + self._event_name + ", ID: " + str(self._event_id) + ", Date: " + str(self._event_date) + ", Location: " + self._event_location + ", Capacity: " + str(self._event_capacity)
    
    # Calculates and returns how many tickets are still available for the event
    def get_remaining_capacity(self):
        return self._event_capacity - len(self._list_user_tickets)
    
    # Returns the event's start time (simplified as the event date)
    def get_start_time(self): return self._event_date
    
    # Returns the event's end time (simplified as the event date)
    def get_end_time(self): return self._event_date
    
    # Getter and setter for event name
    def get_event_name(self): return self._event_name
    def set_event_name(self, event_name): self._event_name = event_name
    
    # Getter and setter for event ID
    def get_event_id(self): return self._event_id
    def set_event_id(self, event_id): self._event_id = event_id
    
    # Getter and setter for event date
    def get_event_date(self): return self._event_date
    def set_event_date(self, event_date): self._event_date = event_date
    
    # Getter and setter for event location
    def get_event_location(self): return self._event_location
    def set_event_location(self, event_location): self._event_location = event_location
    
    # Getter and setter for event capacity
    def get_event_capacity(self): return self._event_capacity
    def set_event_capacity(self, event_capacity): self._event_capacity = event_capacity
    
    # Getter for the list of user tickets
    def get_tickets(self): return self._list_user_tickets
    
    # Setter for the list of user tickets
    def set_tickets(self, tickets): self._list_user_tickets = tickets

# =================================================================
# DATA MANAGEMENT CLASS
# =================================================================

class DataManager:
    def __init__(self):
        # Initialize or load data from pickle files
        self.users = load_data('users')
        self.customers = load_data('customers')
        self.admins = load_data('admins')
        self.events = load_data('events')
        self.bookings = load_data('bookings')
        self.tickets = load_data('tickets')
        self.payments = load_data('payments')
        self.discounts = load_data('discounts')
        
        # Create sample data if nothing exists
        if not self.events:
            self._create_sample_data()
    
    # Create sample data for testing
    def _create_sample_data(self):
        # Create sample events
        event1 = Event("Grand Prix - Abu Dhabi", 201, datetime(2024, 11, 26), "Abu Dhabi Circuit", 1000)
        event2 = Event("Grand Prix - Silverstone", 202, datetime(2024, 12, 15), "Silverstone Circuit", 1200)
        self.events = [event1, event2]
        save_data(self.events, 'events')
        
        # Create sample discounts
        discount1 = Discount(1, 10, 0, "EARLY10", 100)  # 10% discount up to $100
        discount2 = Discount(2, 0, 15, "FLAT15", 15)    # Flat $15 discount
        self.discounts = [discount1, discount2]
        save_data(self.discounts, 'discounts')
        
        # Create admin user
        admin = Admin("Admin", 1, "111222333444555", "admin@zu.ac.ae", datetime.now(), "System Admin", 1001, AccountStatus.ACTIVE)
        self.admins = [admin]
        save_data(self.admins, 'admins')
    
    # User related methods
    def add_customer(self, customer):
        self.customers.append(customer)
        save_data(self.customers, 'customers')
    
    def add_admin(self, admin):
        self.admins.append(admin)
        save_data(self.admins, 'admins')
    
    def get_customer_by_id(self, customer_id):
        for customer in self.customers:
            if customer.get_user_id() == customer_id:
                return customer
        return None
    
    def get_admin_by_id(self, admin_id):
        for admin in self.admins:
            if admin.get_user_id() == admin_id:
                return admin
        return None
    
    def get_customer_by_email(self, email):
        for customer in self.customers:
            if customer.get_user_email() == email:
                return customer
        return None
    
    def get_admin_by_email(self, email):
        for admin in self.admins:
            if admin.get_user_email() == email:
                return admin
        return None
    
    def authenticate_user(self, email, password, is_admin=False):
        if is_admin:
            admin = self.get_admin_by_email(email)
            if admin and admin.get_user_password() == password:
                return admin
        else:
            customer = self.get_customer_by_email(email)
            if customer and customer.get_user_password() == password:
                return customer
        return None
    
    def update_customer(self, customer):
        for i, c in enumerate(self.customers):
            if c.get_user_id() == customer.get_user_id():
                self.customers[i] = customer
                save_data(self.customers, 'customers')
                return True
        return False
    
    def delete_customer(self, customer_id):
        for i, customer in enumerate(self.customers):
            if customer.get_user_id() == customer_id:
                del self.customers[i]
                save_data(self.customers, 'customers')
                return True
        return False
    
    # Event related methods
    def add_event(self, event):
        self.events.append(event)
        save_data(self.events, 'events')
    
    def get_event_by_id(self, event_id):
        for event in self.events:
            if event.get_event_id() == event_id:
                return event
        return None
    
    def update_event(self, event):
        for i, e in enumerate(self.events):
            if e.get_event_id() == event.get_event_id():
                self.events[i] = event
                save_data(self.events, 'events')
                return True
        return False
    
    def delete_event(self, event_id):
        for i, event in enumerate(self.events):
            if event.get_event_id() == event_id:
                del self.events[i]
                save_data(self.events, 'events')
                return True
        return False
    
    # Booking related methods
    def add_booking(self, booking):
        self.bookings.append(booking)
        save_data(self.bookings, 'bookings')
        return booking
    
    def get_booking_by_id(self, booking_id):
        for booking in self.bookings:
            if booking.get_booking_id() == booking_id:
                return booking
        return None
    
    def get_bookings_by_user_id(self, user_id):
        return [booking for booking in self.bookings if booking.get_user_id() == user_id]
    
    def get_bookings_by_event_id(self, event_id):
        return [booking for booking in self.bookings if booking.get_event_id() == event_id]
    
    def update_booking(self, booking):
        for i, b in enumerate(self.bookings):
            if b.get_booking_id() == booking.get_booking_id():
                self.bookings[i] = booking
                save_data(self.bookings, 'bookings')
                return True
        return False
    
    def delete_booking(self, booking_id):
        for i, booking in enumerate(self.bookings):
            if booking.get_booking_id() == booking_id:
                del self.bookings[i]
                save_data(self.bookings, 'bookings')
                return True
        return False
    
    # Ticket related methods
    def add_ticket(self, ticket):
        self.tickets.append(ticket)
        save_data(self.tickets, 'tickets')
        return ticket
    
    def get_ticket_by_id(self, ticket_id):
        for ticket in self.tickets:
            if ticket.get_ticket_id() == ticket_id:
                return ticket
        return None
    
    def get_tickets_by_booking_id(self, booking_id):
        return [ticket for ticket in self.tickets if ticket.get_booking_id() == booking_id]
    
    def get_tickets_by_event_id(self, event_id):
        return [ticket for ticket in self.tickets if ticket.get_event_id() == event_id]
    
    def update_ticket(self, ticket):
        for i, t in enumerate(self.tickets):
            if t.get_ticket_id() == ticket.get_ticket_id():
                self.tickets[i] = ticket
                save_data(self.tickets, 'tickets')
                return True
        return False
    
    def delete_ticket(self, ticket_id):
        for i, ticket in enumerate(self.tickets):
            if ticket.get_ticket_id() == ticket_id:
                del self.tickets[i]
                save_data(self.tickets, 'tickets')
                return True
        return False
    
    # Payment related methods
    def add_payment(self, payment):
        self.payments.append(payment)
        save_data(self.payments, 'payments')
        return payment
    
    def get_payment_by_id(self, payment_id):
        for payment in self.payments:
            if payment.get_payment_id() == payment_id:
                return payment
        return None
    
    def get_payments_by_booking_id(self, booking_id):
        return [payment for payment in self.payments if payment.get_booking_id() == booking_id]
    
    def update_payment(self, payment):
        for i, p in enumerate(self.payments):
            if p.get_payment_id() == payment.get_payment_id():
                self.payments[i] = payment
                save_data(self.payments, 'payments')
                return True
        return False
    
    # Discount related methods
    def add_discount(self, discount):
        self.discounts.append(discount)
        save_data(self.discounts, 'discounts')
    
    def get_discount_by_id(self, discount_id):
        for discount in self.discounts:
            if discount.get_discount_id() == discount_id:
                return discount
        return None
    
    def get_discount_by_code(self, discount_code):
        for discount in self.discounts:
            if discount.get_discount_code() == discount_code:
                return discount
        return None
    
    def update_discount(self, discount):
        for i, d in enumerate(self.discounts):
            if d.get_discount_id() == discount.get_discount_id():
                self.discounts[i] = discount
                save_data(self.discounts, 'discounts')
                return True
        return False
    
    def delete_discount(self, discount_id):
        for i, discount in enumerate(self.discounts):
            if discount.get_discount_id() == discount_id:
                del self.discounts[i]
                save_data(self.discounts, 'discounts')
                return True
        return False

# =================================================================
# GUI IMPLEMENTATION
# =================================================================

class GrandPrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grand Prix Experience Ticket Booking System")
        self.root.state('zoomed')  # Full screen
        
        # Set light blue color as background
        self.bg_color = "#e6f2ff"
        self.accent_color = "#4da6ff"
        self.root.configure(bg=self.bg_color)
        
        # Initialize data manager
        self.data_manager = DataManager()
        
        # Keep track of current user
        self.current_user = None
        self.is_admin = False
        
        # Create login frame
        self.create_login_frame()
    
    # Create the login screen
    def create_login_frame(self):
        # Clear any existing frames
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create a main frame for the login screen
        self.login_frame = tk.Frame(self.root, bg=self.bg_color)
        self.login_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Add title
        title_font = font.Font(family='Helvetica', size=24, weight='bold')
        title = tk.Label(self.login_frame, text="Grand Prix Experience", font=title_font, bg=self.bg_color)
        title.pack(pady=(20, 10))
        
        subtitle_font = font.Font(family='Helvetica', size=14)
        subtitle = tk.Label(self.login_frame, text="Ticket Booking System", font=subtitle_font, bg=self.bg_color)
        subtitle.pack(pady=(0, 30))
        
        # Create login container
        login_container = tk.Frame(self.login_frame, bg=self.bg_color, padx=20, pady=20, bd=1, relief=tk.SOLID)
        login_container.pack(padx=300, pady=20)
        
        # Header
        header_font = font.Font(family='Helvetica', size=16, weight='bold')
        login_header = tk.Label(login_container, text="Login to Your Account", font=header_font, bg=self.bg_color)
        login_header.pack(pady=(0, 20))
        
        # Email
        email_frame = tk.Frame(login_container, bg=self.bg_color)
        email_frame.pack(fill='x', pady=10)
        
        email_label = tk.Label(email_frame, text="Email:", width=15, anchor='w', bg=self.bg_color)
        email_label.pack(side=tk.LEFT)
        
        self.email_entry = tk.Entry(email_frame, width=30)
        self.email_entry.pack(side=tk.LEFT, padx=5)
        
        # Password
        password_frame = tk.Frame(login_container, bg=self.bg_color)
        password_frame.pack(fill='x', pady=10)
        
        password_label = tk.Label(password_frame, text="Password:", width=15, anchor='w', bg=self.bg_color)
        password_label.pack(side=tk.LEFT)
        
        self.password_entry = tk.Entry(password_frame, show="*", width=30)
        self.password_entry.pack(side=tk.LEFT, padx=5)
        
        # Admin checkbox
        self.is_admin_var = tk.BooleanVar()
        admin_check = tk.Checkbutton(login_container, text="Login as Admin", variable=self.is_admin_var, bg=self.bg_color)
        admin_check.pack(pady=10)
        
        # Login button
        login_button = tk.Button(login_container, text="Login", 
                                command=self.handle_login,
                                bg=self.accent_color, fg="white",
                                width=20, height=2)
        login_button.pack(pady=10)
        
        # Register new account button
        register_button = tk.Button(login_container, text="Create New Account", 
                                   command=self.show_registration,
                                   bg="#ffffff", fg="black",
                                   width=20, height=2)
        register_button.pack(pady=10)
    
    # Handle login attempt
    def handle_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        is_admin = self.is_admin_var.get()
        
        user = self.data_manager.authenticate_user(email, password, is_admin)
        
        if user:
            self.current_user = user
            self.is_admin = is_admin
            messagebox.showinfo("Login Successful", "Welcome " + user.get_user_name() + "!")
            
            if is_admin:
                self.show_admin_dashboard()
            else:
                self.show_customer_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid email or password")
    
    # Show registration screen
    def show_registration(self):
        # Clear login frame
        self.login_frame.destroy()
        
        # Create registration frame
        self.registration_frame = tk.Frame(self.root, bg=self.bg_color)
        self.registration_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Add title
        title_font = font.Font(family='Helvetica', size=24, weight='bold')
        title = tk.Label(self.registration_frame, text="Create Your Account", font=title_font, bg=self.bg_color)
        title.pack(pady=(20, 30))
        
        # Create registration form container
        form_container = tk.Frame(self.registration_frame, bg=self.bg_color, padx=20, pady=20, bd=1, relief=tk.SOLID)
        form_container.pack(padx=200, pady=20)
        
        # Name field
        name_frame = tk.Frame(form_container, bg=self.bg_color)
        name_frame.pack(fill='x', pady=10)
        
        name_label = tk.Label(name_frame, text="Full Name:", width=15, anchor='w', bg=self.bg_color)
        name_label.pack(side=tk.LEFT)
        
        self.name_entry = tk.Entry(name_frame, width=40)
        self.name_entry.pack(side=tk.LEFT, padx=5)
        
        # Email field
        email_frame = tk.Frame(form_container, bg=self.bg_color)
        email_frame.pack(fill='x', pady=10)
        
        email_label = tk.Label(email_frame, text="Email:", width=15, anchor='w', bg=self.bg_color)
        email_label.pack(side=tk.LEFT)
        
        self.reg_email_entry = tk.Entry(email_frame, width=40)
        self.reg_email_entry.pack(side=tk.LEFT, padx=5)
        
        # Password field
        password_frame = tk.Frame(form_container, bg=self.bg_color)
        password_frame.pack(fill='x', pady=10)
        
        password_label = tk.Label(password_frame, text="Password:", width=15, anchor='w', bg=self.bg_color)
        password_label.pack(side=tk.LEFT)
        
        self.reg_password_entry = tk.Entry(password_frame, show="*", width=40)
        self.reg_password_entry.pack(side=tk.LEFT, padx=5)
        
        # Address field
        address_frame = tk.Frame(form_container, bg=self.bg_color)
        address_frame.pack(fill='x', pady=10)
        
        address_label = tk.Label(address_frame, text="Address:", width=15, anchor='w', bg=self.bg_color)
        address_label.pack(side=tk.LEFT)
        
        self.address_entry = tk.Entry(address_frame, width=40)
        self.address_entry.pack(side=tk.LEFT, padx=5)
        
        # Phone field
        phone_frame = tk.Frame(form_container, bg=self.bg_color)
        phone_frame.pack(fill='x', pady=10)
        
        phone_label = tk.Label(phone_frame, text="Phone:", width=15, anchor='w', bg=self.bg_color)
        phone_label.pack(side=tk.LEFT)
        
        self.phone_entry = tk.Entry(phone_frame, width=40)
        self.phone_entry.pack(side=tk.LEFT, padx=5)
        
        # Payment info field
        payment_frame = tk.Frame(form_container, bg=self.bg_color)
        payment_frame.pack(fill='x', pady=10)
        
        payment_label = tk.Label(payment_frame, text="Payment Info:", width=15, anchor='w', bg=self.bg_color)
        payment_label.pack(side=tk.LEFT)
        
        self.payment_entry = tk.Entry(payment_frame, width=40)
        self.payment_entry.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = tk.Frame(form_container, bg=self.bg_color)
        button_frame.pack(fill='x', pady=20)
        
        # Register button
        register_button = tk.Button(button_frame, text="Register", 
                                   command=self.handle_registration,
                                   bg=self.accent_color, fg="white",
                                   width=15, height=2)
        register_button.pack(side=tk.LEFT, padx=10)
        
        # Back button
        back_button = tk.Button(button_frame, text="Back to Login", 
                               command=self.create_login_frame,
                               bg="#ffffff", fg="black", 
                               width=15, height=2)
        back_button.pack(side=tk.LEFT, padx=10)
    
    # Handle registration form submission
    def handle_registration(self):
        # Get form values
        name = self.name_entry.get()
        email = self.reg_email_entry.get()
        password = self.reg_password_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()
        payment_info = self.payment_entry.get()
        
        # Validate inputs
        if not name or not email or not password or not address or not phone:
            messagebox.showerror("Registration Error", "All fields are required")
            return
        
        # Check if email is already registered
        if self.data_manager.get_customer_by_email(email) or self.data_manager.get_admin_by_email(email):
            messagebox.showerror("Registration Error", "Email already registered")
            return
        
        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Registration Error", "Invalid email format")
            return
        
        # Create user ID
        user_id = len(self.data_manager.customers) + 100  # Start IDs from 100
        
        # Create customer object
        customer = Customer(
            name, 
            user_id, 
            password, 
            email, 
            datetime.now(), 
            address, 
            phone, 
            payment_info
        )
        
        # Add customer to data manager
        self.data_manager.add_customer(customer)
        
        messagebox.showinfo("Registration Successful", "Your account has been created. You can now login.")
        
        # Return to login screen
        self.create_login_frame()
    
    # Show customer dashboard
    def show_customer_dashboard(self):
        # Clear any existing frames
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create dashboard frame
        self.dashboard_frame = tk.Frame(self.root, bg=self.bg_color)
        self.dashboard_frame.pack(expand=True, fill='both')
        
        # Create sidebar and main content area
        self.sidebar_frame = tk.Frame(self.dashboard_frame, bg="#d4e6ff", width=200)
        self.sidebar_frame.pack(side=tk.LEFT, fill='y')
        
        # Make sure sidebar maintains its width
        self.sidebar_frame.pack_propagate(False)
        
        # Main content area
        self.content_frame = tk.Frame(self.dashboard_frame, bg=self.bg_color)
        self.content_frame.pack(side=tk.RIGHT, expand=True, fill='both')
        
        # Add user info to sidebar
        user_info_frame = tk.Frame(self.sidebar_frame, bg="#d4e6ff", pady=20)
        user_info_frame.pack(fill='x')
        
        # User avatar (placeholder)
        avatar_label = tk.Label(user_info_frame, text="👤", font=("Helvetica", 24), bg="#d4e6ff")
        avatar_label.pack()
        
        # User name
        name_label = tk.Label(user_info_frame, text=self.current_user.get_user_name(), font=("Helvetica", 12, "bold"), bg="#d4e6ff")
        name_label.pack(pady=(5, 0))
        
        # User email
        email_label = tk.Label(user_info_frame, text=self.current_user.get_user_email(), 
                              font=("Helvetica", 10), bg="#d4e6ff")
        email_label.pack()
        
        # Add separator
        ttk.Separator(self.sidebar_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Navigation menu
        menu_font = font.Font(family='Helvetica', size=11)
        
        # Dashboard button (selected by default)
        dashboard_btn = tk.Button(self.sidebar_frame, text="Dashboard", font=menu_font,
                               bg="#4da6ff", fg="white", bd=0, pady=8,
                               command=lambda: self.show_customer_dashboard_content())
        dashboard_btn.pack(fill='x', pady=2)
        
        # Events button
        events_btn = tk.Button(self.sidebar_frame, text="Browse Events", font=menu_font,
                            bg="#d4e6ff", fg="black", bd=0, pady=8,
                            command=lambda: self.show_events_list())
        events_btn.pack(fill='x', pady=2)
        
        # My Bookings button
        bookings_btn = tk.Button(self.sidebar_frame, text="My Bookings", font=menu_font,
                              bg="#d4e6ff", fg="black", bd=0, pady=8,
                              command=lambda: self.show_my_bookings())
        bookings_btn.pack(fill='x', pady=2)
        
        # Account button
        account_btn = tk.Button(self.sidebar_frame, text="My Account", font=menu_font,
                             bg="#d4e6ff", fg="black", bd=0, pady=8,
                             command=lambda: self.show_account_settings())
        account_btn.pack(fill='x', pady=2)
        
        # Add separator
        ttk.Separator(self.sidebar_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Logout button at bottom of sidebar
        logout_btn = tk.Button(self.sidebar_frame, text="Logout", font=menu_font,
                            bg="#ff6666", fg="white", bd=0, pady=8,
                            command=lambda: self.logout())
        logout_btn.pack(fill='x', pady=2, side=tk.BOTTOM)
        
        # Show default dashboard content
        self.show_customer_dashboard_content()
    
    # Show main dashboard content for customer
    def show_customer_dashboard_content(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create welcome header
        header_frame = tk.Frame(self.content_frame, bg=self.bg_color, pady=20)
        header_frame.pack(fill='x')
        
        welcome_label = tk.Label(header_frame, text="Welcome to Grand Prix Experience", 
                                font=("Helvetica", 18, "bold"), bg=self.bg_color)
        welcome_label.pack()
        
        date_label = tk.Label(header_frame, text="Today: " + datetime.now().strftime("%B %d, %Y"), 
                             font=("Helvetica", 10), bg=self.bg_color)
        date_label.pack()
        
        # Create dashboard cards
        cards_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        cards_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Configure grid
        cards_frame.columnconfigure(0, weight=1)
        cards_frame.columnconfigure(1, weight=1)
        cards_frame.rowconfigure(0, weight=1)
        cards_frame.rowconfigure(1, weight=1)
        
        # Card 1: Upcoming Events
        card1 = tk.Frame(cards_frame, bg="white", padx=15, pady=15, bd=1, relief=tk.SOLID)
        card1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        card1_title = tk.Label(card1, text="Upcoming Events", font=("Helvetica", 14, "bold"), bg="white")
        card1_title.pack(anchor='w')
        
        ttk.Separator(card1, orient='horizontal').pack(fill='x', pady=5)
        
        # Get upcoming events (showing max 3)
        upcoming_events = sorted(self.data_manager.events, key=lambda e: e.get_event_date())[:3]
        
        if upcoming_events:
            for event in upcoming_events:
                event_frame = tk.Frame(card1, bg="white", pady=5)
                event_frame.pack(fill='x')
                
                event_name = tk.Label(event_frame, text=event.get_event_name(), font=("Helvetica", 11), bg="white")
                event_name.pack(anchor='w')
                
                event_info = tk.Label(event_frame, text="Date: " + event.get_event_date().strftime("%B %d, %Y") + 
                                     " • " + event.get_event_location(), font=("Helvetica", 9), bg="white", fg="gray")
                event_info.pack(anchor='w')
                
                ttk.Separator(card1, orient='horizontal').pack(fill='x', pady=2)
        else:
            no_events = tk.Label(card1, text="No upcoming events", bg="white")
            no_events.pack(pady=10)
        
        view_all_btn = tk.Button(card1, text="View All Events", bg=self.accent_color, fg="white",
                              command=lambda: self.show_events_list())
        view_all_btn.pack(pady=10)
        
        # Card 2: My Tickets
        card2 = tk.Frame(cards_frame, bg="white", padx=15, pady=15, bd=1, relief=tk.SOLID)
        card2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        card2_title = tk.Label(card2, text="My Tickets", font=("Helvetica", 14, "bold"), bg="white")
        card2_title.pack(anchor='w')
        
        ttk.Separator(card2, orient='horizontal').pack(fill='x', pady=5)
        
        # Get user bookings
        user_bookings = self.data_manager.get_bookings_by_user_id(self.current_user.get_user_id())
        
        if user_bookings:
            ticket_count = sum(booking.get_number_of_tickets() for booking in user_bookings)
            ticket_label = tk.Label(card2, text="You have " + str(ticket_count) + " tickets", 
                                 font=("Helvetica", 12), bg="white")
            ticket_label.pack(pady=10)
            
            # Show recent bookings
            for i, booking in enumerate(sorted(user_bookings, key=lambda b: b.get_booking_date(), reverse=True)):
                if i >= 2:  # Show only the 2 most recent bookings
                    break
                
                event = self.data_manager.get_event_by_id(booking.get_event_id())
                if event:
                    booking_frame = tk.Frame(card2, bg="white", pady=5)
                    booking_frame.pack(fill='x')
                    
                    booking_info = tk.Label(booking_frame, 
                                          text=event.get_event_name() + " - " + str(booking.get_number_of_tickets()) + " tickets",
                                          font=("Helvetica", 11), bg="white")
                    booking_info.pack(anchor='w')
                    
                    booking_date = tk.Label(booking_frame, 
                                          text="Booked on: " + booking.get_booking_date().strftime("%B %d, %Y"),
                                          font=("Helvetica", 9), bg="white", fg="gray")
                    booking_date.pack(anchor='w')
                    
                    ttk.Separator(card2, orient='horizontal').pack(fill='x', pady=2)
        else:
            no_tickets = tk.Label(card2, text="You don't have any tickets yet", bg="white")
            no_tickets.pack(pady=10)
        
        view_tickets_btn = tk.Button(card2, text="View All Tickets", bg=self.accent_color, fg="white",
                                 command=lambda: self.show_my_bookings())
        view_tickets_btn.pack(pady=10)
        
        # Card 3: Quick Actions
        card3 = tk.Frame(cards_frame, bg="white", padx=15, pady=15, bd=1, relief=tk.SOLID)
        card3.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        card3_title = tk.Label(card3, text="Quick Actions", font=("Helvetica", 14, "bold"), bg="white")
        card3_title.pack(anchor='w')
        
        ttk.Separator(card3, orient='horizontal').pack(fill='x', pady=5)
        
        # Quick action buttons
        book_ticket_btn = tk.Button(card3, text="Book a New Ticket", bg="#4caf50", fg="white", width=20,
                                 command=lambda: self.show_events_list())
        book_ticket_btn.pack(pady=5)
        
        view_bookings_btn = tk.Button(card3, text="View My Bookings", bg="#2196f3", fg="white", width=20,
                                    command=lambda: self.show_my_bookings())
        view_bookings_btn.pack(pady=5)
        
        update_profile_btn = tk.Button(card3, text="Update My Profile", bg="#ff9800", fg="white", width=20,
                                     command=lambda: self.show_account_settings())
        update_profile_btn.pack(pady=5)
        
        # Card 4: Information
        card4 = tk.Frame(cards_frame, bg="white", padx=15, pady=15, bd=1, relief=tk.SOLID)
        card4.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        card4_title = tk.Label(card4, text="Information", font=("Helvetica", 14, "bold"), bg="white")
        card4_title.pack(anchor='w')
        
        ttk.Separator(card4, orient='horizontal').pack(fill='x', pady=5)
        
        info_text = """
        Welcome to the Grand Prix Experience Ticket Booking System!
        
        Here you can:
        • Book tickets for upcoming Formula One events
        • View and manage your bookings
        • Update your account information
        
        Need help? Contact our support team at support@grandprix.com
        """
        
        info_label = tk.Label(card4, text=info_text, bg="white", justify=tk.LEFT, wraplength=300)
        info_label.pack(pady=10, fill='both', expand=True)
    
    # Show events list for booking
    def show_events_list(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create events header
        header_frame = tk.Frame(self.content_frame, bg=self.bg_color, pady=20)
        header_frame.pack(fill='x')
        
        events_label = tk.Label(header_frame, text="Upcoming Events", 
                              font=("Helvetica", 18, "bold"), bg=self.bg_color)
        events_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Browse and book tickets for upcoming races", 
                                font=("Helvetica", 10), bg=self.bg_color)
        subtitle_label.pack()
        
        # Create scrollable events list
        events_container = tk.Frame(self.content_frame, bg=self.bg_color)
        events_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create canvas with scrollbar for events
        canvas = tk.Canvas(events_container, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(events_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Get sorted events by date
        sorted_events = sorted(self.data_manager.events, key=lambda e: e.get_event_date())
        
        if sorted_events:
            for event in sorted_events:
                # Create event card
                event_card = tk.Frame(scrollable_frame, bg="white", bd=1, relief=tk.SOLID, padx=15, pady=15)
                event_card.pack(fill='x', padx=10, pady=10)
                
                # Event details
                event_name = tk.Label(event_card, text=event.get_event_name(), 
                                    font=("Helvetica", 14, "bold"), bg="white")
                event_name.grid(row=0, column=0, sticky='w', pady=(0, 5))
                
                event_date = tk.Label(event_card, text="Date: " + event.get_event_date().strftime("%B %d, %Y"), 
                                    bg="white")
                event_date.grid(row=1, column=0, sticky='w')
                
                event_location = tk.Label(event_card, text="Location: " + event.get_event_location(), 
                                        bg="white")
                event_location.grid(row=2, column=0, sticky='w')
                
                event_capacity = tk.Label(event_card, 
                                        text="Available Tickets: " + str(event.get_remaining_capacity()) + 
                                        " of " + str(event.get_event_capacity()),
                                        bg="white")
                event_capacity.grid(row=3, column=0, sticky='w')
                
                # Book button
                book_button = tk.Button(event_card, text="Book Tickets", 
                                      bg=self.accent_color, fg="white",
                                      command=lambda e=event: self.show_booking_form(e))
                book_button.grid(row=1, column=1, rowspan=2, padx=(20, 0))
                
                # Set grid configuration
                event_card.columnconfigure(0, weight=1)
                event_card.columnconfigure(1, weight=0)
        else:
            no_events = tk.Label(scrollable_frame, text="No upcoming events available", 
                              font=("Helvetica", 12), bg=self.bg_color)
            no_events.pack(pady=50)
    
    def show_booking_form(self, event):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create booking form header
        header_frame = tk.Frame(self.content_frame, bg=self.bg_color, pady=10)
        header_frame.pack(fill='x')
        
        booking_label = tk.Label(header_frame, text="Book Tickets: " + event.get_event_name(), 
                            font=("Helvetica", 18, "bold"), bg=self.bg_color)
        booking_label.pack()
        
        event_info = tk.Label(header_frame, 
                            text="Date: " + event.get_event_date().strftime("%B %d, %Y") + 
                            " • " + event.get_event_location(),
                            font=("Helvetica", 10), bg=self.bg_color)
        event_info.pack()
        
        # Create main container
        main_container = tk.Frame(self.content_frame, bg=self.bg_color)
        main_container.pack(fill='both', expand=True, padx=20, pady=5)
        
        # Create canvas with scrollbar
        canvas = tk.Canvas(main_container, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        
        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create form container inside canvas
        form_container = tk.Frame(canvas, bg="white", bd=1, relief=tk.SOLID)
        
        # Create window in canvas
        canvas_window = canvas.create_window((0, 0), window=form_container, anchor="nw", width=canvas.winfo_width())
        
        # Function to update canvas scroll region
        def update_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            
        # Function to update form width
        def update_form_width(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        # Bind events
        form_container.bind("<Configure>", update_scrollregion)
        canvas.bind("<Configure>", update_form_width)
        
        # Bind mousewheel - using a more reliable approach that's contained to this canvas
        def on_mousewheel(event):
            # Only scroll if the canvas is visible and has a scrollable area
            if canvas.winfo_exists():
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        # Bind only to the canvas widget itself, not globally
        canvas.bind("<MouseWheel>", on_mousewheel)
        
        # Ticket type selection
        ticket_type_frame = tk.Frame(form_container, bg="white", pady=15)
        ticket_type_frame.pack(fill='x', padx=20)
        
        ticket_type_label = tk.Label(ticket_type_frame, text="Select Ticket Type:", 
                                    font=("Helvetica", 12, "bold"), bg="white")
        ticket_type_label.pack(anchor='w')
        
        # Ticket types (radio buttons)
        self.ticket_type_var = tk.StringVar(value="standard")
        
        ticket_types_frame = tk.Frame(ticket_type_frame, bg="white", pady=10)
        ticket_types_frame.pack(fill='x')
        
        # Standard ticket
        standard_frame = tk.Frame(ticket_types_frame, bg="white", pady=5, bd=1, relief=tk.SOLID)
        standard_frame.pack(fill='x', pady=5)
        
        standard_radio = tk.Radiobutton(standard_frame, text="Standard Ticket", 
                                    variable=self.ticket_type_var, value="standard", bg="white")
        standard_radio.grid(row=0, column=0, sticky='w', padx=10)
        
        standard_price = tk.Label(standard_frame, text="$100", font=("Helvetica", 12, "bold"), bg="white")
        standard_price.grid(row=0, column=1, sticky='e', padx=10)
        
        standard_desc = tk.Label(standard_frame, 
                            text="Regular seating with good view of the track",
                            bg="white", wraplength=400, justify=tk.LEFT)
        standard_desc.grid(row=1, column=0, columnspan=2, sticky='w', padx=35, pady=(0, 5))
        
        # VIP ticket
        vip_frame = tk.Frame(ticket_types_frame, bg="white", pady=5, bd=1, relief=tk.SOLID)
        vip_frame.pack(fill='x', pady=5)
        
        vip_radio = tk.Radiobutton(vip_frame, text="VIP Experience", 
                                variable=self.ticket_type_var, value="vip", bg="white")
        vip_radio.grid(row=0, column=0, sticky='w', padx=10)
        
        vip_price = tk.Label(vip_frame, text="$250", font=("Helvetica", 12, "bold"), bg="white")
        vip_price.grid(row=0, column=1, sticky='e', padx=10)
        
        vip_desc = tk.Label(vip_frame, 
                        text="Premium seating with complimentary food and drinks",
                        bg="white", wraplength=400, justify=tk.LEFT)
        vip_desc.grid(row=1, column=0, columnspan=2, sticky='w', padx=35, pady=(0, 5))
        
        # Weekend package
        weekend_frame = tk.Frame(ticket_types_frame, bg="white", pady=5, bd=1, relief=tk.SOLID)
        weekend_frame.pack(fill='x', pady=5)
        
        weekend_radio = tk.Radiobutton(weekend_frame, text="Weekend Package", 
                                    variable=self.ticket_type_var, value="weekend", bg="white")
        weekend_radio.grid(row=0, column=0, sticky='w', padx=10)
        
        weekend_price = tk.Label(weekend_frame, text="$400", font=("Helvetica", 12, "bold"), bg="white")
        weekend_price.grid(row=0, column=1, sticky='e', padx=10)
        
        weekend_desc = tk.Label(weekend_frame, 
                            text="3-day pass with access to practice, qualifying, and race sessions",
                            bg="white", wraplength=400, justify=tk.LEFT)
        weekend_desc.grid(row=1, column=0, columnspan=2, sticky='w', padx=35, pady=(0, 5))
        
        # Configure grid columns for all frames
        standard_frame.columnconfigure(0, weight=1)
        standard_frame.columnconfigure(1, weight=0)
        vip_frame.columnconfigure(0, weight=1)
        vip_frame.columnconfigure(1, weight=0)
        weekend_frame.columnconfigure(0, weight=1)
        weekend_frame.columnconfigure(1, weight=0)
        
        # Number of tickets
        quantity_frame = tk.Frame(form_container, bg="white", pady=15)
        quantity_frame.pack(fill='x', padx=20)
        
        quantity_label = tk.Label(quantity_frame, text="Number of Tickets:", 
                                font=("Helvetica", 12, "bold"), bg="white")
        quantity_label.pack(anchor='w')
        
        # Ticket quantity spinner
        self.ticket_quantity_var = tk.StringVar(value="1")
        quantity_spinner = ttk.Spinbox(quantity_frame, from_=1, to=10, textvariable=self.ticket_quantity_var, 
                                    width=5, state="readonly")
        quantity_spinner.pack(anchor='w', pady=5)
        
        # Add separator
        ttk.Separator(form_container, orient='horizontal').pack(fill='x', padx=20, pady=10)
        
        # Discount code
        discount_frame = tk.Frame(form_container, bg="white", pady=10)
        discount_frame.pack(fill='x', padx=20)
        
        discount_label = tk.Label(discount_frame, text="Discount Code (if any):", 
                                font=("Helvetica", 12, "bold"), bg="white")
        discount_label.pack(anchor='w')
        
        self.discount_code_entry = tk.Entry(discount_frame, width=20)
        self.discount_code_entry.pack(anchor='w', pady=5)
        
        # Add separator
        ttk.Separator(form_container, orient='horizontal').pack(fill='x', padx=20, pady=10)
        
        # Payment method
        payment_frame = tk.Frame(form_container, bg="white", pady=15)
        payment_frame.pack(fill='x', padx=20)
        
        payment_label = tk.Label(payment_frame, text="Payment Method:", 
                            font=("Helvetica", 12, "bold"), bg="white")
        payment_label.pack(anchor='w')
        
        # Payment type selection
        self.payment_type_var = tk.StringVar(value="credit_card")
        
        credit_card_radio = tk.Radiobutton(payment_frame, text="Credit Card", 
                                        variable=self.payment_type_var, value="credit_card", 
                                        bg="white", command=self.toggle_payment_form)
        credit_card_radio.pack(anchor='w', pady=5)
        
        digital_radio = tk.Radiobutton(payment_frame, text="Digital Payment (PayPal, etc)", 
                                    variable=self.payment_type_var, value="digital", 
                                    bg="white", command=self.toggle_payment_form)
        digital_radio.pack(anchor='w')
        
        # Credit card form (default)
        self.credit_card_frame = tk.Frame(payment_frame, bg="white", pady=10)
        self.credit_card_frame.pack(fill='x')
        
        # Card number
        card_num_frame = tk.Frame(self.credit_card_frame, bg="white")
        card_num_frame.pack(fill='x', pady=5)
        
        card_num_label = tk.Label(card_num_frame, text="Card Number:", width=15, anchor='w', bg="white")
        card_num_label.pack(side=tk.LEFT)
        
        self.card_num_entry = tk.Entry(card_num_frame, width=25)
        self.card_num_entry.pack(side=tk.LEFT)
        
        # Expiry date
        expiry_frame = tk.Frame(self.credit_card_frame, bg="white")
        expiry_frame.pack(fill='x', pady=5)
        
        expiry_label = tk.Label(expiry_frame, text="Expiry Date (MM/YY):", width=15, anchor='w', bg="white")
        expiry_label.pack(side=tk.LEFT)
        
        self.expiry_entry = tk.Entry(expiry_frame, width=10)
        self.expiry_entry.pack(side=tk.LEFT)
        
        # CVV
        cvv_frame = tk.Frame(self.credit_card_frame, bg="white")
        cvv_frame.pack(fill='x', pady=5)
        
        cvv_label = tk.Label(cvv_frame, text="CVV:", width=15, anchor='w', bg="white")
        cvv_label.pack(side=tk.LEFT)
        
        self.cvv_entry = tk.Entry(cvv_frame, width=5, show="*")
        self.cvv_entry.pack(side=tk.LEFT)
        
        # Card type
        card_type_frame = tk.Frame(self.credit_card_frame, bg="white")
        card_type_frame.pack(fill='x', pady=5)
        
        card_type_label = tk.Label(card_type_frame, text="Card Type:", width=15, anchor='w', bg="white")
        card_type_label.pack(side=tk.LEFT)
        
        self.card_type_var = tk.StringVar(value="VISA")
        card_types = ["VISA", "MASTERCARD", "AMEX"]
        card_type_dropdown = ttk.Combobox(card_type_frame, textvariable=self.card_type_var, 
                                    values=card_types, state="readonly", width=12)
        card_type_dropdown.pack(side=tk.LEFT)
        
        # Digital payment form (hidden by default)
        self.digital_frame = tk.Frame(payment_frame, bg="white", pady=10)
        
        # Digital account id
        account_frame = tk.Frame(self.digital_frame, bg="white")
        account_frame.pack(fill='x', pady=5)
        
        account_label = tk.Label(account_frame, text="Email/Account ID:", width=15, anchor='w', bg="white")
        account_label.pack(side=tk.LEFT)
        
        self.account_entry = tk.Entry(account_frame, width=25)
        self.account_entry.pack(side=tk.LEFT)
        
        # Digital provider
        provider_frame = tk.Frame(self.digital_frame, bg="white")
        provider_frame.pack(fill='x', pady=5)
        
        provider_label = tk.Label(provider_frame, text="Provider:", width=15, anchor='w', bg="white")
        provider_label.pack(side=tk.LEFT)
        
        self.provider_var = tk.StringVar(value="PayPal")
        providers = ["PayPal", "Apple Pay", "Google Pay", "Other"]
        provider_dropdown = ttk.Combobox(provider_frame, textvariable=self.provider_var, 
                                    values=providers, state="readonly", width=12)
        provider_dropdown.pack(side=tk.LEFT)
        
        # Summary
        summary_frame = tk.Frame(form_container, bg="#f5f5f5", pady=15)
        summary_frame.pack(fill='x', padx=20, pady=10)
        
        summary_label = tk.Label(summary_frame, text="Booking Summary", 
                            font=("Helvetica", 12, "bold"), bg="#f5f5f5")
        summary_label.pack(anchor='w')
        
        # Calculate prices based on selection
        def update_price(*args):
            ticket_type = self.ticket_type_var.get()
            quantity = int(self.ticket_quantity_var.get())
            
            # Base prices
            if ticket_type == "standard":
                base_price = 100
            elif ticket_type == "vip":
                base_price = 250
            else:  # weekend
                base_price = 400
            
            total = base_price * quantity
            
            # Update labels
            base_price_label.config(text="$" + str(base_price) + " × " + str(quantity))
            subtotal_value_label.config(text="$" + str(total))
            total_value_label.config(text="$" + str(total))
        
        # Track changes to update price
        self.ticket_type_var.trace_add("write", update_price)
        self.ticket_quantity_var.trace_add("write", update_price)
        
        # Price breakdown
        price_frame = tk.Frame(summary_frame, bg="#f5f5f5", pady=5)
        price_frame.pack(fill='x')
        
        base_label = tk.Label(price_frame, text="Base Price:", bg="#f5f5f5")
        base_label.grid(row=0, column=0, sticky='w')
        
        base_price_label = tk.Label(price_frame, text="$100 × 1", bg="#f5f5f5")
        base_price_label.grid(row=0, column=1, sticky='e')
        
        subtotal_label = tk.Label(price_frame, text="Subtotal:", bg="#f5f5f5")
        subtotal_label.grid(row=1, column=0, sticky='w')
        
        subtotal_value_label = tk.Label(price_frame, text="$100", bg="#f5f5f5")
        subtotal_value_label.grid(row=1, column=1, sticky='e')
        
        discount_label = tk.Label(price_frame, text="Discount:", bg="#f5f5f5")
        discount_label.grid(row=2, column=0, sticky='w')
        
        discount_value_label = tk.Label(price_frame, text="$0", bg="#f5f5f5")
        discount_value_label.grid(row=2, column=1, sticky='e')
        
        ttk.Separator(price_frame, orient='horizontal').grid(row=3, column=0, columnspan=2, sticky='ew', pady=5)
        
        total_label = tk.Label(price_frame, text="Total:", font=("Helvetica", 12, "bold"), bg="#f5f5f5")
        total_label.grid(row=4, column=0, sticky='w')
        
        total_value_label = tk.Label(price_frame, text="$100", font=("Helvetica", 12, "bold"), bg="#f5f5f5")
        total_value_label.grid(row=4, column=1, sticky='e')
        
        # Configure grid
        price_frame.columnconfigure(0, weight=1)
        price_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = tk.Frame(form_container, bg="white", pady=15)
        button_frame.pack(fill='x', padx=20)
        
        # Back button
        back_button = tk.Button(button_frame, text="Back to Events", 
                            command=lambda: self.show_events_list(),
                            bg="#f0f0f0", fg="black", width=15)
        back_button.pack(side=tk.LEFT, padx=5)
        
        # Book button
        book_button = tk.Button(button_frame, text="Complete Booking", 
                            command=lambda: self.process_booking(event),
                            bg="#4caf50", fg="white", width=15)
        book_button.pack(side=tk.RIGHT, padx=5)
        
        # Initialize price
        update_price()    
    # Toggle between credit card and digital payment forms
    def toggle_payment_form(self):
        payment_type = self.payment_type_var.get()
        
        if payment_type == "credit_card":
            self.digital_frame.pack_forget()
            self.credit_card_frame.pack(fill='x')
        else:
            self.credit_card_frame.pack_forget()
            self.digital_frame.pack(fill='x')
    
    # Process booking submission
    def process_booking(self, event):
        # Get form values
        ticket_type = self.ticket_type_var.get()
        quantity = int(self.ticket_quantity_var.get())
        discount_code = self.discount_code_entry.get()
        payment_type = self.payment_type_var.get()
        
        # Calculate prices
        if ticket_type == "standard":
            base_price = 100
            ticket_type_id = 1
        elif ticket_type == "vip":
            base_price = 250
            ticket_type_id = 2
        else:  # weekend
            base_price = 400
            ticket_type_id = 3
        
        total_price = base_price * quantity
        
        # Check discount code
        discount = None
        if discount_code:
            discount = self.data_manager.get_discount_by_code(discount_code)
            if discount:
                total_price = discount.apply_discount(total_price)
        
        # Check if enough tickets are available
        if event.get_remaining_capacity() < quantity:
            messagebox.showerror("Booking Error", "Not enough tickets available for this event")
            return
        
        # Create booking ID
        booking_id = len(self.data_manager.bookings) + 1001  # Start IDs from 1001
        
        # Create booking
        new_booking = Booking(
            self.current_user.get_user_id(),
            event.get_event_id(),
            booking_id,
            datetime.now(),
            quantity,
            total_price,
            BookingStatus.CONFIRMED
        )
        
        # Add booking to data manager
        self.data_manager.add_booking(new_booking)
        
        # Process payment
        payment_id = len(self.data_manager.payments) + 2001  # Start payment IDs from 2001
        
        if payment_type == "credit_card":
            # Get credit card details
            card_number = self.card_num_entry.get()
            expiry_date = self.expiry_entry.get()
            card_type_str = self.card_type_var.get()
            
            # Validate card details
            if not card_number or not expiry_date:
                messagebox.showerror("Payment Error", "Please enter all card details")
                return
            
            # Map string to enum
            card_type_map = {
                "VISA": CardType.VISA,
                "MASTERCARD": CardType.MASTERCARD,
                "AMEX": CardType.AMEX
            }
            
            # Create credit card payment
            payment = CreditCard(
                booking_id,
                payment_id,
                card_number,
                expiry_date,
                card_type_map[card_type_str],
                datetime.now(),
                PaymentTransactionStatus.SUCCESSFUL
            )
        else:
            # Get digital payment details
            account = self.account_entry.get()
            provider = self.provider_var.get()
            
            # Validate details
            if not account:
                messagebox.showerror("Payment Error", "Please enter your account/email")
                return
            
            # Create auth code
            auth_code = "AUTH-" + str(random.randint(10000, 99999))
            
            # Create digital payment
            payment = DigitalPayment(
                booking_id,
                payment_id,
                random.randint(100000, 999999),  # Transaction ID
                account,
                auth_code,
                datetime.now(),
                PaymentTransactionStatus.SUCCESSFUL
            )
        
        # Add payment to data manager
        self.data_manager.add_payment(payment)
        
        # Create tickets
        seat_prefix = "A" if ticket_type == "standard" else ("B" if ticket_type == "vip" else "C")
        
        for i in range(quantity):
            seat_number = seat_prefix + str(100 + i)
            
            # Create ticket based on type
            if ticket_type == "weekend":
                new_ticket = WeekendPackage(
                    ticket_type_id,
                    booking_id,
                    f"T{booking_id}-{i+1}",
                    seat_number,
                    base_price,
                    event.get_event_date(),
                    random.randint(5001, 5999),  # Package ID
                    "Standard Weekend",
                    "Access to all weekend events, pit lane walk, driver autograph session",
                    event.get_event_id()
                )
            elif ticket_type == "vip":
                new_ticket = SeasonMembership(
                    ticket_type_id,
                    booking_id,
                    f"T{booking_id}-{i+1}",
                    seat_number,
                    base_price,
                    event.get_event_date(),
                    random.randint(3001, 3999),  # Member ID
                    self.current_user.get_user_name(),
                    "VIP Lounge access, complimentary food and drinks",
                    event.get_event_id()
                )
            else:  # standard
                new_ticket = SingleRacePass(
                    ticket_type_id,
                    booking_id,
                    f"T{booking_id}-{i+1}",
                    seat_number,
                    base_price,
                    event.get_event_date(),
                    random.randint(4001, 4999),  # Pass ID
                    event.get_event_date().strftime("%Y-%m-%d"),
                    "Standard race day access",
                    event.get_event_id()
                )
            
            # Add ticket to data manager
            self.data_manager.add_ticket(new_ticket)
        
        # Show success message
        messagebox.showinfo("Booking Successful", 
                           "Your booking is confirmed! " + str(quantity) + " tickets for " + 
                           event.get_event_name() + " have been booked.")
        
        # Show bookings
        self.show_my_bookings()
    
    # Show user's bookings
    def show_my_bookings(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create bookings header
        header_frame = tk.Frame(self.content_frame, bg=self.bg_color, pady=20)
        header_frame.pack(fill='x')
        
        bookings_label = tk.Label(header_frame, text="My Bookings", 
                                font=("Helvetica", 18, "bold"), bg=self.bg_color)
        bookings_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="View and manage your bookings", 
                                font=("Helvetica", 10), bg=self.bg_color)
        subtitle_label.pack()
        
        # Create scrollable bookings list
        bookings_container = tk.Frame(self.content_frame, bg=self.bg_color)
        bookings_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create canvas with scrollbar for bookings
        canvas = tk.Canvas(bookings_container, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(bookings_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Get user's bookings
        user_bookings = self.data_manager.get_bookings_by_user_id(self.current_user.get_user_id())
        
        if user_bookings:
            # Sort bookings by date (newest first)
            sorted_bookings = sorted(user_bookings, key=lambda b: b.get_booking_date(), reverse=True)
            
            for booking in sorted_bookings:
                # Get related event
                event = self.data_manager.get_event_by_id(booking.get_event_id())
                if not event:
                    continue
                
                # Get related tickets
                tickets = self.data_manager.get_tickets_by_booking_id(booking.get_booking_id())
                
                # Create booking card
                booking_card = tk.Frame(scrollable_frame, bg="white", bd=1, relief=tk.SOLID, padx=15, pady=15)
                booking_card.pack(fill='x', padx=10, pady=10)
                
                # Booking details
                booking_title = tk.Label(booking_card, 
                                       text=event.get_event_name() + " (" + str(len(tickets)) + " tickets)",
                                       font=("Helvetica", 14, "bold"), bg="white")
                booking_title.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 10))
                
                # Event date and location
                event_info = tk.Label(booking_card, 
                                    text="Event: " + event.get_event_date().strftime("%B %d, %Y") + 
                                    " at " + event.get_event_location(),
                                    bg="white")
                event_info.grid(row=1, column=0, sticky='w')
                
                # Booking date
                booking_date = tk.Label(booking_card, 
                                      text="Booked on: " + booking.get_booking_date().strftime("%B %d, %Y"),
                                      bg="white")
                booking_date.grid(row=2, column=0, sticky='w')
                
                # Total price
                price_label = tk.Label(booking_card, 
                                     text="Total Price: $" + str(booking.get_total_price()),
                                     bg="white")
                price_label.grid(row=3, column=0, sticky='w')
                
                # Status
                status_label = tk.Label(booking_card, 
                                      text="Status: " + booking.get_booking_status().value,
                                      bg="white", fg="green" if booking.get_booking_status() == BookingStatus.CONFIRMED else "orange")
                status_label.grid(row=4, column=0, sticky='w')
                
                # View tickets button
                view_button = tk.Button(booking_card, text="View Tickets", 
                                      bg=self.accent_color, fg="white",
                                      command=lambda b=booking, e=event: self.show_booking_details(b, e))
                view_button.grid(row=2, column=1, rowspan=2, padx=(20, 0))
                
                # Cancel button (only for upcoming events)
                if event.get_event_date() > datetime.now() and booking.get_booking_status() != BookingStatus.CANCELLED:
                    cancel_button = tk.Button(booking_card, text="Cancel Booking", 
                                           bg="#ff6666", fg="white",
                                           command=lambda b=booking: self.cancel_booking(b))
                    cancel_button.grid(row=4, column=1, padx=(20, 0))
                
                # Set grid configuration
                booking_card.columnconfigure(0, weight=1)
                booking_card.columnconfigure(1, weight=0)
        else:
            no_bookings = tk.Label(scrollable_frame, text="You don't have any bookings yet", 
                                 font=("Helvetica", 12), bg=self.bg_color)
            no_bookings.pack(pady=50)
    
    # Show booking details
    def show_booking_details(self, booking, event):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create booking details header
        header_frame = tk.Frame(self.content_frame, bg=self.bg_color, pady=10)
        header_frame.pack(fill='x')
        
        details_label = tk.Label(header_frame, text="Booking Details", 
                            font=("Helvetica", 18, "bold"), bg=self.bg_color)
        details_label.pack()
        
        event_label = tk.Label(header_frame, text=event.get_event_name(), 
                            font=("Helvetica", 14), bg=self.bg_color)
        event_label.pack()
        
        # Create main container
        main_container = tk.Frame(self.content_frame, bg=self.bg_color)
        main_container.pack(fill='both', expand=True, padx=20, pady=5)
        
        # Create canvas with scrollbar
        canvas = tk.Canvas(main_container, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        
        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create details container inside canvas
        details_container = tk.Frame(canvas, bg="white", bd=1, relief=tk.SOLID)
        
        # Create window in canvas
        canvas_window = canvas.create_window((0, 0), window=details_container, anchor="nw", width=canvas.winfo_width())
        
        # Function to update canvas scroll region
        def update_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            
        # Function to update details width
        def update_details_width(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        # Bind events
        details_container.bind("<Configure>", update_scrollregion)
        canvas.bind("<Configure>", update_details_width)
        
        # Bind mousewheel specifically to this canvas
        def on_mousewheel(event):
            if canvas.winfo_exists():
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind("<MouseWheel>", on_mousewheel)
        
        # Booking summary
        summary_frame = tk.Frame(details_container, bg="white", pady=15)
        summary_frame.pack(fill='x', padx=20)
        
        # Booking ID
        booking_id_label = tk.Label(summary_frame, text="Booking Reference: " + str(booking.get_booking_id()), 
                                font=("Helvetica", 12, "bold"), bg="white")
        booking_id_label.pack(anchor='w', pady=(0, 10))
        
        # Event details
        event_date_label = tk.Label(summary_frame, text="Event Date: " + event.get_event_date().strftime("%B %d, %Y"), 
                                bg="white")
        event_date_label.pack(anchor='w', pady=2)
        
        event_location_label = tk.Label(summary_frame, text="Location: " + event.get_event_location(), 
                                    bg="white")
        event_location_label.pack(anchor='w', pady=2)
        
        # Booking details
        booking_date_label = tk.Label(summary_frame, text="Booking Date: " + booking.get_booking_date().strftime("%B %d, %Y"), 
                                    bg="white")
        booking_date_label.pack(anchor='w', pady=2)
        
        ticket_count_label = tk.Label(summary_frame, text="Number of Tickets: " + str(booking.get_number_of_tickets()), 
                                    bg="white")
        ticket_count_label.pack(anchor='w', pady=2)
        
        total_price_label = tk.Label(summary_frame, text="Total Price: $" + str(booking.get_total_price()), 
                                bg="white")
        total_price_label.pack(anchor='w', pady=2)
        
        status_label = tk.Label(summary_frame, text="Status: " + booking.get_booking_status().value, 
                            bg="white", fg="green" if booking.get_booking_status() == BookingStatus.CONFIRMED else "orange")
        status_label.pack(anchor='w', pady=2)
        
        # Add separator
        ttk.Separator(details_container, orient='horizontal').pack(fill='x', padx=20, pady=10)
        
        # Tickets section
        tickets_frame = tk.Frame(details_container, bg="white", pady=15)
        tickets_frame.pack(fill='x', padx=20)
        
        tickets_label = tk.Label(tickets_frame, text="Your Tickets", 
                            font=("Helvetica", 12, "bold"), bg="white")
        tickets_label.pack(anchor='w', pady=(0, 10))
        
        # Get tickets for this booking
        tickets = self.data_manager.get_tickets_by_booking_id(booking.get_booking_id())
        
        if tickets:
            for i, ticket in enumerate(tickets):
                ticket_frame = tk.Frame(tickets_frame, bg="#f9f9f9", bd=1, relief=tk.SOLID, padx=10, pady=10)
                ticket_frame.pack(fill='x', pady=5)
                
                # Basic ticket info
                ticket_id_label = tk.Label(ticket_frame, text="Ticket #" + str(i+1) + ": " + ticket.get_ticket_id(), 
                                        font=("Helvetica", 11, "bold"), bg="#f9f9f9")
                ticket_id_label.grid(row=0, column=0, sticky='w')
                
                # Determine ticket type and display appropriate info
                if isinstance(ticket, WeekendPackage):
                    ticket_type_label = tk.Label(ticket_frame, text="Weekend Package", 
                                            bg="#f9f9f9", fg="#9c27b0")
                    ticket_type_label.grid(row=0, column=1, sticky='e')
                    
                    benefits_label = tk.Label(ticket_frame, text="Benefits: " + ticket.get_package_benefits(), 
                                        bg="#f9f9f9", wraplength=400, justify=tk.LEFT)
                    benefits_label.grid(row=2, column=0, columnspan=2, sticky='w')
                    
                elif isinstance(ticket, SeasonMembership):
                    ticket_type_label = tk.Label(ticket_frame, text="VIP Experience", 
                                            bg="#f9f9f9", fg="#2196f3")
                    ticket_type_label.grid(row=0, column=1, sticky='e')
                    
                    benefits_label = tk.Label(ticket_frame, text="Benefits: " + ticket.get_included_gifts(), 
                                        bg="#f9f9f9", wraplength=400, justify=tk.LEFT)
                    benefits_label.grid(row=2, column=0, columnspan=2, sticky='w')
                    
                elif isinstance(ticket, SingleRacePass):
                    ticket_type_label = tk.Label(ticket_frame, text="Standard Ticket", 
                                            bg="#f9f9f9", fg="#4caf50")
                    ticket_type_label.grid(row=0, column=1, sticky='e')
                    
                    benefits_label = tk.Label(ticket_frame, text="Benefits: " + ticket.get_pass_benefits(), 
                                        bg="#f9f9f9", wraplength=400, justify=tk.LEFT)
                    benefits_label.grid(row=2, column=0, columnspan=2, sticky='w')
                    
                else:
                    ticket_type_label = tk.Label(ticket_frame, text="Regular Ticket", 
                                            bg="#f9f9f9")
                    ticket_type_label.grid(row=0, column=1, sticky='e')
                
                # Common ticket info
                seat_label = tk.Label(ticket_frame, text="Seat: " + ticket.get_seat_number(), 
                                    bg="#f9f9f9")
                seat_label.grid(row=1, column=0, sticky='w')
                
                price_label = tk.Label(ticket_frame, text="Price: $" + str(ticket.get_ticket_price()), 
                                    bg="#f9f9f9")
                price_label.grid(row=1, column=1, sticky='e')
                
                # Configure grid
                ticket_frame.columnconfigure(0, weight=1)
                ticket_frame.columnconfigure(1, weight=1)
        else:
            no_tickets = tk.Label(tickets_frame, text="No tickets found for this booking", 
                                bg="white")
            no_tickets.pack(pady=20)
        
        # Add separator
        ttk.Separator(details_container, orient='horizontal').pack(fill='x', padx=20, pady=10)
        
        # Payment section
        payment_frame = tk.Frame(details_container, bg="white", pady=15)
        payment_frame.pack(fill='x', padx=20)
        
        payment_label = tk.Label(payment_frame, text="Payment Information", 
                            font=("Helvetica", 12, "bold"), bg="white")
        payment_label.pack(anchor='w', pady=(0, 10))
        
        # Get payments for this booking
        payments = self.data_manager.get_payments_by_booking_id(booking.get_booking_id())
        
        if payments:
            for payment in payments:
                payment_info_frame = tk.Frame(payment_frame, bg="#f9f9f9", bd=1, relief=tk.SOLID, padx=10, pady=10)
                payment_info_frame.pack(fill='x', pady=5)
                
                # Payment ID
                payment_id_label = tk.Label(payment_info_frame, text="Payment ID: " + str(payment.get_payment_id()), 
                                        bg="#f9f9f9", font=("Helvetica", 11, "bold"))
                payment_id_label.pack(anchor='w')
                
                # Payment type
                payment_type_label = tk.Label(payment_info_frame, text="Payment Type: " + payment.get_payment_type().value, 
                                        bg="#f9f9f9")
                payment_type_label.pack(anchor='w')
                
                # Transaction date
                transaction_date_label = tk.Label(payment_info_frame, 
                                            text="Transaction Date: " + payment.get_transaction_date().strftime("%B %d, %Y %H:%M"), 
                                            bg="#f9f9f9")
                transaction_date_label.pack(anchor='w')
                
                # Transaction status
                status_color = "green" if payment.get_transaction_status() == PaymentTransactionStatus.SUCCESSFUL else "red"
                transaction_status_label = tk.Label(payment_info_frame, 
                                                text="Status: " + payment.get_transaction_status().value, 
                                                bg="#f9f9f9", fg=status_color)
                transaction_status_label.pack(anchor='w')
                
                # Show additional details based on payment type
                if isinstance(payment, CreditCard):
                    card_info_label = tk.Label(payment_info_frame, 
                                            text="Card: " + payment.get_card_type().value + " ending in " + 
                                            payment.get_card_number()[-4:], 
                                            bg="#f9f9f9")
                    card_info_label.pack(anchor='w')
                    
                elif isinstance(payment, DigitalPayment):
                    digital_info_label = tk.Label(payment_info_frame, 
                                            text="Account: " + payment.get_account_identifier(),
                                            bg="#f9f9f9")
                    digital_info_label.pack(anchor='w')
        else:
            no_payment = tk.Label(payment_frame, text="No payment information found", 
                                bg="white")
            no_payment.pack(pady=20)
        
        # Buttons
        button_frame = tk.Frame(details_container, bg="white", pady=15)
        button_frame.pack(fill='x', padx=20)
        
        back_button = tk.Button(button_frame, text="Back to My Bookings", 
                            command=lambda: self.show_my_bookings(),
                            bg="#f0f0f0", fg="black", width=20)
        back_button.pack(side=tk.LEFT)
        
        # Add print button
        print_button = tk.Button(button_frame, text="Print Tickets", 
                            command=lambda: messagebox.showinfo("Print Tickets", "Tickets sent to printer"),
                            bg=self.accent_color, fg="white", width=20)
        print_button.pack(side=tk.RIGHT)
        
    # Cancel a booking
    def cancel_booking(self, booking):
        # Ask for confirmation
        confirm = messagebox.askyesno("Cancel Booking", 
                                     "Are you sure you want to cancel this booking? This action cannot be undone.")
        
        if confirm:
            # Update booking status
            booking.set_booking_status(BookingStatus.CANCELLED)
            self.data_manager.update_booking(booking)
            
            messagebox.showinfo("Booking Cancelled", "Your booking has been cancelled successfully")
            
            # Refresh bookings view
            self.show_my_bookings()
    
    # Show account settings
    def show_account_settings(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create account settings header
        header_frame = tk.Frame(self.content_frame, bg=self.bg_color, pady=20)
        header_frame.pack(fill='x')
        
        settings_label = tk.Label(header_frame, text="Account Settings", 
                                font=("Helvetica", 18, "bold"), bg=self.bg_color)
        settings_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Manage your account information", 
                                font=("Helvetica", 10), bg=self.bg_color)
        subtitle_label.pack()
        
        # Create settings container
        settings_container = tk.Frame(self.content_frame, bg="white", bd=1, relief=tk.SOLID)
        settings_container.pack(fill='both', expand=True, padx=100, pady=20)
        
        # User information section
        user_info_frame = tk.Frame(settings_container, bg="white", pady=15)
        user_info_frame.pack(fill='x', padx=20)
        
        user_info_label = tk.Label(user_info_frame, text="Your Information", 
                                 font=("Helvetica", 12, "bold"), bg="white")
        user_info_label.pack(anchor='w', pady=(0, 10))
        
        # Form fields - prepopulated with current user data
        
        # Name field
        name_frame = tk.Frame(user_info_frame, bg="white")
        name_frame.pack(fill='x', pady=10)
        
        name_label = tk.Label(name_frame, text="Full Name:", width=15, anchor='w', bg="white")
        name_label.pack(side=tk.LEFT)
        
        self.settings_name_entry = tk.Entry(name_frame, width=40)
        self.settings_name_entry.insert(0, self.current_user.get_user_name())
        self.settings_name_entry.pack(side=tk.LEFT, padx=5)
        
        # Email field
        email_frame = tk.Frame(user_info_frame, bg="white")
        email_frame.pack(fill='x', pady=10)
        
        email_label = tk.Label(email_frame, text="Email:", width=15, anchor='w', bg="white")
        email_label.pack(side=tk.LEFT)
        
        self.settings_email_entry = tk.Entry(email_frame, width=40)
        self.settings_email_entry.insert(0, self.current_user.get_user_email())
        self.settings_email_entry.pack(side=tk.LEFT, padx=5)
        
        # Get customer-specific fields if current user is a customer
        if isinstance(self.current_user, Customer):
            # Address field
            address_frame = tk.Frame(user_info_frame, bg="white")
            address_frame.pack(fill='x', pady=10)
            
            address_label = tk.Label(address_frame, text="Address:", width=15, anchor='w', bg="white")
            address_label.pack(side=tk.LEFT)
            
            self.settings_address_entry = tk.Entry(address_frame, width=40)
            self.settings_address_entry.insert(0, self.current_user.get_customer_address())
            self.settings_address_entry.pack(side=tk.LEFT, padx=5)
            
            # Phone field
            phone_frame = tk.Frame(user_info_frame, bg="white")
            phone_frame.pack(fill='x', pady=10)
            
            phone_label = tk.Label(phone_frame, text="Phone:", width=15, anchor='w', bg="white")
            phone_label.pack(side=tk.LEFT)
            
            self.settings_phone_entry = tk.Entry(phone_frame, width=40)
            self.settings_phone_entry.insert(0, self.current_user.get_customer_phone())
            self.settings_phone_entry.pack(side=tk.LEFT, padx=5)
            
            # Payment info field
            payment_frame = tk.Frame(user_info_frame, bg="white")
            payment_frame.pack(fill='x', pady=10)
            
            payment_label = tk.Label(payment_frame, text="Payment Info:", width=15, anchor='w', bg="white")
            payment_label.pack(side=tk.LEFT)
            
            self.settings_payment_entry = tk.Entry(payment_frame, width=40)
            self.settings_payment_entry.insert(0, self.current_user.get_payment_info())
            self.settings_payment_entry.pack(side=tk.LEFT, padx=5)
        
        # Password change section
        password_section = tk.Frame(settings_container, bg="white", pady=15)
        password_section.pack(fill='x', padx=20)
        
        # Add separator before password section
        ttk.Separator(settings_container, orient='horizontal').pack(fill='x', padx=20, pady=10)
        
        password_label = tk.Label(password_section, text="Change Password", 
                                font=("Helvetica", 12, "bold"), bg="white")
        password_label.pack(anchor='w', pady=(0, 10))
        
        # Current password field
        current_pw_frame = tk.Frame(password_section, bg="white")
        current_pw_frame.pack(fill='x', pady=10)
        
        current_pw_label = tk.Label(current_pw_frame, text="Current Password:", width=15, anchor='w', bg="white")
        current_pw_label.pack(side=tk.LEFT)
        
        self.current_pw_entry = tk.Entry(current_pw_frame, width=40, show="*")
        self.current_pw_entry.pack(side=tk.LEFT, padx=5)
        
        # New password field
        new_pw_frame = tk.Frame(password_section, bg="white")
        new_pw_frame.pack(fill='x', pady=10)
        
        new_pw_label = tk.Label(new_pw_frame, text="New Password:", width=15, anchor='w', bg="white")
        new_pw_label.pack(side=tk.LEFT)
        
        self.new_pw_entry = tk.Entry(new_pw_frame, width=40, show="*")
        self.new_pw_entry.pack(side=tk.LEFT, padx=5)
        
        # Confirm new password field
        confirm_pw_frame = tk.Frame(password_section, bg="white")
        confirm_pw_frame.pack(fill='x', pady=10)
        
        confirm_pw_label = tk.Label(confirm_pw_frame, text="Confirm Password:", width=15, anchor='w', bg="white")
        confirm_pw_label.pack(side=tk.LEFT)
        
        self.confirm_pw_entry = tk.Entry(confirm_pw_frame, width=40, show="*")
        self.confirm_pw_entry.pack(side=tk.LEFT, padx=5)
        
        # Update buttons
        button_frame = tk.Frame(settings_container, bg="white", pady=15)
        button_frame.pack(fill='x', padx=20)
        
        # Update profile button
        update_profile_button = tk.Button(button_frame, text="Update Profile", 
                                       command=lambda: self.update_user_profile(),
                                       bg=self.accent_color, fg="white",
                                       width=15)
        update_profile_button.pack(side=tk.LEFT, padx=5)
        
        # Change password button
        change_pw_button = tk.Button(button_frame, text="Change Password", 
                                   command=lambda: self.change_password(),
                                   bg="#ff9800", fg="white",
                                   width=15)
        change_pw_button.pack(side=tk.LEFT, padx=5)
    
    # Update user profile
    def update_user_profile(self):
        # Get updated values
        new_name = self.settings_name_entry.get()
        new_email = self.settings_email_entry.get()
        
        # Basic validation
        if not new_name or not new_email:
            messagebox.showerror("Update Error", "Name and email cannot be empty")
            return
        
        # Check email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
            messagebox.showerror("Update Error", "Invalid email format")
            return
        
        # Check if email is already used by another user
        if new_email != self.current_user.get_user_email():
            existing_customer = self.data_manager.get_customer_by_email(new_email)
            existing_admin = self.data_manager.get_admin_by_email(new_email)
            
            if (existing_customer and existing_customer.get_user_id() != self.current_user.get_user_id()) or \
               (existing_admin and existing_admin.get_user_id() != self.current_user.get_user_id()):
                messagebox.showerror("Update Error", "Email is already used by another account")
                return
        
        # Update user information
        self.current_user.set_user_name(new_name)
        self.current_user.set_user_email(new_email)
        
        # Update customer-specific fields if applicable
        if isinstance(self.current_user, Customer):
            new_address = self.settings_address_entry.get()
            new_phone = self.settings_phone_entry.get()
            new_payment_info = self.settings_payment_entry.get()
            
            if not new_address or not new_phone:
                messagebox.showerror("Update Error", "Address and phone cannot be empty")
                return
            
            self.current_user.set_customer_address(new_address)
            self.current_user.set_customer_phone(new_phone)
            self.current_user.set_payment_info(new_payment_info)
            
            # Update in data manager
            self.data_manager.update_customer(self.current_user)
        elif isinstance(self.current_user, Admin):
            # Update in data manager
            self.data_manager.update_admin(self.current_user)
        
        messagebox.showinfo("Profile Updated", "Your profile has been updated successfully")
    
    # Change password
    def change_password(self):
        current_pw = self.current_pw_entry.get()
        new_pw = self.new_pw_entry.get()
        confirm_pw = self.confirm_pw_entry.get()
        
        # Validate inputs
        if not current_pw or not new_pw or not confirm_pw:
            messagebox.showerror("Password Error", "All password fields are required")
            return
        
        # Check current password
        if current_pw != self.current_user.get_user_password():
            messagebox.showerror("Password Error", "Current password is incorrect")
            return
        
        # Check if new passwords match
        if new_pw != confirm_pw:
            messagebox.showerror("Password Error", "New passwords do not match")
            return
        
        # Update password
        self.current_user.set_user_password(new_pw)
        
        # Update in data manager
        if isinstance(self.current_user, Customer):
            self.data_manager.update_customer(self.current_user)
        elif isinstance(self.current_user, Admin):
            self.data_manager.update_admin(self.current_user)
        
        messagebox.showinfo("Password Changed", "Your password has been changed successfully")
        
        # Clear password fields
        self.current_pw_entry.delete(0, tk.END)
        self.new_pw_entry.delete(0, tk.END)
        self.confirm_pw_entry.delete(0, tk.END)
    
    # Show admin dashboard
    def show_admin_dashboard(self):
        # Clear any existing frames
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create dashboard frame
        self.dashboard_frame = tk.Frame(self.root, bg=self.bg_color)
        self.dashboard_frame.pack(expand=True, fill='both')
        
        # Create sidebar and main content area
        self.sidebar_frame = tk.Frame(self.dashboard_frame, bg="#d4e6ff", width=200)
        self.sidebar_frame.pack(side=tk.LEFT, fill='y')
        
        # Make sure sidebar maintains its width
        self.sidebar_frame.pack_propagate(False)
        
        # Main content area
        self.content_frame = tk.Frame(self.dashboard_frame, bg=self.bg_color)
        self.content_frame.pack(side=tk.RIGHT, expand=True, fill='both')
        
        # Add admin info to sidebar
        admin_info_frame = tk.Frame(self.sidebar_frame, bg="#d4e6ff", pady=20)
        admin_info_frame.pack(fill='x')
        
        # Admin avatar (placeholder)
        avatar_label = tk.Label(admin_info_frame, text="👨‍💼", font=("Helvetica", 24), bg="#d4e6ff")
        avatar_label.pack()
        
        # Admin name
        name_label = tk.Label(admin_info_frame, text=self.current_user.get_user_name(), 
                            font=("Helvetica", 12, "bold"), bg="#d4e6ff")
        name_label.pack(pady=(5, 0))
        
        # Admin role
        role_label = tk.Label(admin_info_frame, text=self.current_user.get_admin_role(), 
                            font=("Helvetica", 10), bg="#d4e6ff")
        role_label.pack()
        
        # Add separator
        ttk.Separator(self.sidebar_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Navigation menu
        menu_font = font.Font(family='Helvetica', size=11)
        
        # Dashboard button (selected by default)
        dashboard_btn = tk.Button(self.sidebar_frame, text="Dashboard", font=menu_font,
                               bg="#4da6ff", fg="white", bd=0, pady=8,
                               command=lambda: self.show_admin_dashboard_content())
        dashboard_btn.pack(fill='x', pady=2)
        
        # Manage events button
        events_btn = tk.Button(self.sidebar_frame, text="Manage Events", font=menu_font,
                            bg="#d4e6ff", fg="black", bd=0, pady=8,
                            command=lambda: self.show_manage_events())
        events_btn.pack(fill='x', pady=2)
        
        # Manage users button
        users_btn = tk.Button(self.sidebar_frame, text="Manage Users", font=menu_font,
                           bg="#d4e6ff", fg="black", bd=0, pady=8,
                           command=lambda: self.show_manage_users())
        users_btn.pack(fill='x', pady=2)
        
        # Manage discounts button
        discounts_btn = tk.Button(self.sidebar_frame, text="Manage Discounts", font=menu_font,
                               bg="#d4e6ff", fg="black", bd=0, pady=8,
                               command=lambda: self.show_manage_discounts())
        discounts_btn.pack(fill='x', pady=2)
        
        # Booking reports button
        reports_btn = tk.Button(self.sidebar_frame, text="Booking Reports", font=menu_font,
                             bg="#d4e6ff", fg="black", bd=0, pady=8,
                             command=lambda: self.show_booking_reports())
        reports_btn.pack(fill='x', pady=2)
        
        # Add separator
        ttk.Separator(self.sidebar_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Logout button at bottom of sidebar
        logout_btn = tk.Button(self.sidebar_frame, text="Logout", font=menu_font,
                            bg="#ff6666", fg="white", bd=0, pady=8,
                            command=lambda: self.logout())
        logout_btn.pack(fill='x', pady=2, side=tk.BOTTOM)
        
        # Show default admin dashboard content
        self.show_admin_dashboard_content()
    
    # Admin dashboard content
    def show_admin_dashboard_content(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create welcome header
        header_frame = tk.Frame(self.content_frame, bg=self.bg_color, pady=20)
        header_frame.pack(fill='x')
        
        welcome_label = tk.Label(header_frame, text="Admin Dashboard", 
                              font=("Helvetica", 18, "bold"), bg=self.bg_color)
        welcome_label.pack()
        
        date_label = tk.Label(header_frame, text="Today: " + datetime.now().strftime("%B %d, %Y"), 
                           font=("Helvetica", 10), bg=self.bg_color)
        date_label.pack()
        
        # Create dashboard stats
        stats_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        stats_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Configure grid
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)
        stats_frame.columnconfigure(2, weight=1)
        stats_frame.rowconfigure(0, weight=1)
        stats_frame.rowconfigure(1, weight=1)
        
        # Stat 1: Total Events
        stat1 = tk.Frame(stats_frame, bg="white", padx=15, pady=15, bd=1, relief=tk.SOLID)
        stat1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        stat1_title = tk.Label(stat1, text="Total Events", font=("Helvetica", 14, "bold"), bg="white")
        stat1_title.pack()
        
        stat1_value = tk.Label(stat1, text=str(len(self.data_manager.events)), 
                            font=("Helvetica", 24), bg="white", fg="#2196f3")
        stat1_value.pack()
        
        # Stat 2: Total Bookings
        stat2 = tk.Frame(stats_frame, bg="white", padx=15, pady=15, bd=1, relief=tk.SOLID)
        stat2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        stat2_title = tk.Label(stat2, text="Total Bookings", font=("Helvetica", 14, "bold"), bg="white")
        stat2_title.pack()
        
        stat2_value = tk.Label(stat2, text=str(len(self.data_manager.bookings)), 
                            font=("Helvetica", 24), bg="white", fg="#4caf50")
        stat2_value.pack()
        
        # Stat 3: Total Users
        stat3 = tk.Frame(stats_frame, bg="white", padx=15, pady=15, bd=1, relief=tk.SOLID)
        stat3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        stat3_title = tk.Label(stat3, text="Total Users", font=("Helvetica", 14, "bold"), bg="white")
        stat3_title.pack()
        
        stat3_value = tk.Label(stat3, text=str(len(self.data_manager.customers)), 
                            font=("Helvetica", 24), bg="white", fg="#ff9800")
        stat3_value.pack()
        
        # Upcoming events section
        upcoming_frame = tk.Frame(stats_frame, bg="white", padx=15, pady=15, bd=1, relief=tk.SOLID)
        upcoming_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        upcoming_title = tk.Label(upcoming_frame, text="Upcoming Events", 
                               font=("Helvetica", 14, "bold"), bg="white")
        upcoming_title.pack(anchor='w')
        
        ttk.Separator(upcoming_frame, orient='horizontal').pack(fill='x', pady=5)
        
        # Get upcoming events
        upcoming_events = sorted(self.data_manager.events, key=lambda e: e.get_event_date())
        upcoming_events = [e for e in upcoming_events if e.get_event_date() > datetime.now()][:5]
        
        if upcoming_events:
            for event in upcoming_events:
                event_frame = tk.Frame(upcoming_frame, bg="white", pady=5)
                event_frame.pack(fill='x')
                
                event_name = tk.Label(event_frame, text=event.get_event_name(), 
                                   font=("Helvetica", 11), bg="white")
                event_name.pack(side=tk.LEFT, anchor='w')
                
                event_date = tk.Label(event_frame, text=event.get_event_date().strftime("%B %d, %Y"), 
                                   bg="white", fg="gray")
                event_date.pack(side=tk.RIGHT, anchor='e')
                
                ttk.Separator(upcoming_frame, orient='horizontal').pack(fill='x', pady=2)
        else:
            no_events = tk.Label(upcoming_frame, text="No upcoming events", bg="white")
            no_events.pack(pady=10)
        
        # Quick actions
        actions_frame = tk.Frame(stats_frame, bg="white", padx=15, pady=15, bd=1, relief=tk.SOLID)
        actions_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        
        actions_title = tk.Label(actions_frame, text="Quick Actions", 
                              font=("Helvetica", 14, "bold"), bg="white")
        actions_title.pack(anchor='w')
        
        ttk.Separator(actions_frame, orient='horizontal').pack(fill='x', pady=5)
        
        # Action buttons
        add_event_btn = tk.Button(actions_frame, text="Add New Event", 
                               bg="#4caf50", fg="white", width=20,
                               command=lambda: self.show_add_event_form())
        add_event_btn.pack(pady=5)
        
        view_bookings_btn = tk.Button(actions_frame, text="View All Bookings", 
                                   bg="#2196f3", fg="white", width=20,
                                   command=lambda: self.show_booking_reports())
        view_bookings_btn.pack(pady=5)
        
        add_discount_btn = tk.Button(actions_frame, text="Add New Discount", 
                                  bg="#ff9800", fg="white", width=20,
                                  command=lambda: self.show_add_discount_form())
        add_discount_btn.pack(pady=5)
    
    # Manage events
    def show_manage_events(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create header
        header_frame = tk.Frame(self.content_frame, bg=self.bg_color, pady=20)
        header_frame.pack(fill='x')
        
        events_label = tk.Label(header_frame, text="Manage Events", 
                             font=("Helvetica", 18, "bold"), bg=self.bg_color)
        events_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Add, edit, or delete events", 
                               font=("Helvetica", 10), bg=self.bg_color)
        subtitle_label.pack()
        
        # Add event button
        add_btn = tk.Button(header_frame, text="Add New Event", 
                         bg="#4caf50", fg="white", padx=10, pady=5,
                         command=lambda: self.show_add_event_form())
        add_btn.pack(pady=10)
        
        # Create scrollable events list
        events_container = tk.Frame(self.content_frame, bg=self.bg_color)
        events_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create canvas with scrollbar for events
        canvas = tk.Canvas(events_container, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(events_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Get sorted events by date
        sorted_events = sorted(self.data_manager.events, key=lambda e: e.get_event_date())
        
        if sorted_events:
            for event in sorted_events:
                # Create event card
                event_card = tk.Frame(scrollable_frame, bg="white", bd=1, relief=tk.SOLID, padx=15, pady=15)
                event_card.pack(fill='x', padx=10, pady=10)
                
                # Event details
                event_name = tk.Label(event_card, text=event.get_event_name(), 
                                   font=("Helvetica", 14, "bold"), bg="white")
                event_name.grid(row=0, column=0, sticky='w', pady=(0, 5))
                
                event_id = tk.Label(event_card, text="ID: " + str(event.get_event_id()), 
                                 bg="white", fg="gray")
                event_id.grid(row=0, column=1, sticky='e')
                
                event_date = tk.Label(event_card, text="Date: " + event.get_event_date().strftime("%B %d, %Y"), 
                                   bg="white")
                event_date.grid(row=1, column=0, sticky='w')
                
                event_location = tk.Label(event_card, text="Location: " + event.get_event_location(), 
                                       bg="white")
                event_location.grid(row=2, column=0, sticky='w')
                
                event_capacity = tk.Label(event_card, 
                                       text="Available Tickets: " + str(event.get_remaining_capacity()) + 
                                       " of " + str(event.get_event_capacity()),
                                       bg="white")
                event_capacity.grid(row=3, column=0, sticky='w')
                
                # Edit button
                edit_button = tk.Button(event_card, text="Edit", 
                                     bg=self.accent_color, fg="white",
                                     command=lambda e=event: self.show_edit_event_form(e))
                edit_button.grid(row=1, column=1, padx=(20, 0))
                
                # Delete button
                delete_button = tk.Button(event_card, text="Delete", 
                                       bg="#ff6666", fg="white",
                                       command=lambda e=event: self.delete_event(e))
                delete_button.grid(row=2, column=1, padx=(20, 0))
                
                # Set grid configuration
                event_card.columnconfigure(0, weight=1)
                event_card.columnconfigure(1, weight=0)
        else:
            no_events = tk.Label(scrollable_frame, text="No events available", 
                              font=("Helvetica", 12), bg=self.bg_color)
            no_events.pack(pady=50)
    
    # Show add event form
    def show_add_event_form(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create header
        header_frame = tk.Frame(self.content_frame, bg=self.bg_color, pady=20)
        header_frame.pack(fill='x')
        
        add_label = tk.Label(header_frame, text="Add New Event", 
                          font=("Helvetica", 18, "bold"), bg=self.bg_color)
        add_label.pack()
        
        # Create form container
        form_container = tk.Frame(self.content_frame, bg="white", bd=1, relief=tk.SOLID)
        form_container.pack(fill='both', expand=True, padx=100, pady=20)
        
        # Event name field
        name_frame = tk.Frame(form_container, bg="white", pady=10)
        name_frame.pack(fill='x', padx=20)
        
        name_label = tk.Label(name_frame, text="Event Name:", width=15, anchor='w', bg="white")
        name_label.pack(side=tk.LEFT)
        
        self.event_name_entry = tk.Entry(name_frame, width=40)
        self.event_name_entry.pack(side=tk.LEFT, padx=5)
        
        # Event ID field
        id_frame = tk.Frame(form_container, bg="white", pady=10)
        id_frame.pack(fill='x', padx=20)
        
        id_label = tk.Label(id_frame, text="Event ID:", width=15, anchor='w', bg="white")
        id_label.pack(side=tk.LEFT)
        
        # Auto-generate an event ID
        next_id = max([e.get_event_id() for e in self.data_manager.events], default=200) + 1
        
        self.event_id_entry = tk.Entry(id_frame, width=10)
        self.event_id_entry.insert(0, str(next_id))
        self.event_id_entry.config(state='readonly')
        self.event_id_entry.pack(side=tk.LEFT, padx=5)
        
        # Event date field
        date_frame = tk.Frame(form_container, bg="white", pady=10)
        date_frame.pack(fill='x', padx=20)
        
        date_label = tk.Label(date_frame, text="Event Date (YYYY-MM-DD):", width=15, anchor='w', bg="white")
        date_label.pack(side=tk.LEFT)
        
        self.event_date_entry = tk.Entry(date_frame, width=15)
        self.event_date_entry.pack(side=tk.LEFT, padx=5)
        
        # Event location field
        location_frame = tk.Frame(form_container, bg="white", pady=10)
        location_frame.pack(fill='x', padx=20)
        
        location_label = tk.Label(location_frame, text="Location:", width=15, anchor='w', bg="white")
        location_label.pack(side=tk.LEFT)
        
        self.event_location_entry = tk.Entry(location_frame, width=40)
        self.event_location_entry.pack(side=tk.LEFT, padx=5)
        
        # Capacity field
        capacity_frame = tk.Frame(form_container, bg="white", pady=10)
        capacity_frame.pack(fill='x', padx=20)
        
        capacity_label = tk.Label(capacity_frame, text="Capacity:", width=15, anchor='w', bg="white")
        capacity_label.pack(side=tk.LEFT)
        
        self.event_capacity_entry = tk.Entry(capacity_frame, width=10)
        self.event_capacity_entry.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = tk.Frame(form_container, bg="white", pady=20)
        button_frame.pack(fill='x', padx=20)
        
        # Back button
        back_button = tk.Button(button_frame, text="Cancel", 
                             command=lambda: self.show_manage_events(),
                             bg="#f0f0f0", fg="black", width=10)
        back_button.pack(side=tk.LEFT, padx=5)
        
        # Save button
        save_button = tk.Button(button_frame, text="Save Event", 
                             command=lambda: self.save_event(),
                             bg="#4caf50", fg="white", width=10)
        save_button.pack(side=tk.RIGHT, padx=5)
    
    # Save new event
    def save_event(self):
        # Get form values
        name = self.event_name_entry.get()
        event_id = int(self.event_id_entry.get())
        date_str = self.event_date_entry.get()
        location = self.event_location_entry.get()
        capacity_str = self.event_capacity_entry.get()
        
        # Validate inputs
        if not name or not date_str or not location or not capacity_str:
            messagebox.showerror("Input Error", "All fields are required")
            return
        
        try:
            # Parse date
            date_parts = date_str.split('-')
            if len(date_parts) != 3:
                raise ValueError("Invalid date format")
                
            year, month, day = map(int, date_parts)
            date = datetime(year, month, day)
            
            # Parse capacity
            capacity = int(capacity_str)
            if capacity <= 0:
                raise ValueError("Capacity must be positive")
                
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return
        
        # Create new event
        new_event = Event(name, event_id, date, location, capacity)
        
        # Add to data manager
        self.data_manager.add_event(new_event)
        
        messagebox.showinfo("Event Added", "The event has been added successfully")
        
        # Return to events list
        self.show_manage_events()
    
    # Show edit event form
    def show_edit_event_form(self, event):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create header
        header_frame = tk.Frame(self.content_frame, bg=self.bg_color, pady=20)
        header_frame.pack(fill='x')
        
        edit_label = tk.Label(header_frame, text="Edit Event", 
                           font=("Helvetica", 18, "bold"), bg=self.bg_color)
        edit_label.pack()
        
        # Create form container
        form_container = tk.Frame(self.content_frame, bg="white", bd=1, relief=tk.SOLID)
        form_container.pack(fill='both', expand=True, padx=100, pady=20)
        
        # Event name field
        name_frame = tk.Frame(form_container, bg="white", pady=10)
        name_frame.pack(fill='x', padx=20)
        
        name_label = tk.Label(name_frame, text="Event Name:", width=15, anchor='w', bg="white")
        name_label.pack(side=tk.LEFT)
        
        self.event_name_entry = tk.Entry(name_frame, width=40)
        self.event_name_entry.insert(0, event.get_event_name())
        self.event_name_entry.pack(side=tk.LEFT, padx=5)
        
        # Event ID field
        id_frame = tk.Frame(form_container, bg="white", pady=10)
        id_frame.pack(fill='x', padx=20)
        
        id_label = tk.Label(id_frame, text="Event ID:", width=15, anchor='w', bg="white")
        id_label.pack(side=tk.LEFT)
        
        self.event_id_entry = tk.Entry(id_frame, width=10)
        self.event_id_entry.insert(0, str(event.get_event_id()))
        self.event_id_entry.config(state='readonly')
        self.event_id_entry.pack(side=tk.LEFT, padx=5)
        
        # Event date field
        date_frame = tk.Frame(form_container, bg="white", pady=10)
        date_frame.pack(fill='x', padx=20)
        
        date_label = tk.Label(date_frame, text="Event Date (YYYY-MM-DD):", width=15, anchor='w', bg="white")
        date_label.pack(side=tk.LEFT)
        
        self.event_date_entry = tk.Entry(date_frame, width=15)
        self.event_date_entry.insert(0, event.get_event_date().strftime("%Y-%m-%d"))
        self.event_date_entry.pack(side=tk.LEFT, padx=5)
        
        # Event location field
        location_frame = tk.Frame(form_container, bg="white", pady=10)
        location_frame.pack(fill='x', padx=20)
        
        location_label = tk.Label(location_frame, text="Location:", width=15, anchor='w', bg="white")
        location_label.pack(side=tk.LEFT)
        
        self.event_location_entry = tk.Entry(location_frame, width=40)
        self.event_location_entry.insert(0, event.get_event_location())
        self.event_location_entry.pack(side=tk.LEFT, padx=5)
        
        # Capacity field
        capacity_frame = tk.Frame(form_container, bg="white", pady=10)
        capacity_frame.pack(fill='x', padx=20)
        
        capacity_label = tk.Label(capacity_frame, text="Capacity:", width=15, anchor='w', bg="white")
        capacity_label.pack(side=tk.LEFT)
        
        self.event_capacity_entry = tk.Entry(capacity_frame, width=10)
        self.event_capacity_entry.insert(0, str(event.get_event_capacity()))
        self.event_capacity_entry.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = tk.Frame(form_container, bg="white", pady=20)
        button_frame.pack(fill='x', padx=20)
        
        # Back button
        back_button = tk.Button(button_frame, text="Cancel", 
                             command=lambda: self.show_manage_events(),
                             bg="#f0f0f0", fg="black", width=10)
        back_button.pack(side=tk.LEFT, padx=5)
        
        # Update button
        update_button = tk.Button(button_frame, text="Update Event", 
                               command=lambda: self.update_event(event),
                               bg="#4caf50", fg="white", width=10)
        update_button.pack(side=tk.RIGHT, padx=5)
    
    # Update existing event
    def update_event(self, event):
        # Get form values
        name = self.event_name_entry.get()
        date_str = self.event_date_entry.get()
        location = self.event_location_entry.get()
        capacity_str = self.event_capacity_entry.get()
        
        # Validate inputs
        if not name or not date_str or not location or not capacity_str:
            messagebox.showerror("Input Error", "All fields are required")
            return
        
        try:
            # Parse date
            date_parts = date_str.split('-')
            if len(date_parts) != 3:
                raise ValueError("Invalid date format")
                
            year, month, day = map(int, date_parts)
            date = datetime(year, month, day)
            
            # Parse capacity
            capacity = int(capacity_str)
            if capacity <= 0:
                raise ValueError("Capacity must be positive")
                
            # Check if new capacity is less than tickets sold
            tickets_sold = event.get_event_capacity() - event.get_remaining_capacity()
            if capacity < tickets_sold:
                raise ValueError("New capacity cannot be less than tickets already sold")
                
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return
        
        # Update event
        event.set_event_name(name)
        event.set_event_date(date)
        event.set_event_location(location)
        event.set_event_capacity(capacity)
        
        # Update in data manager
        self.data_manager.update_event(event)
        
        messagebox.showinfo("Event Updated", "The event has been updated successfully")
        
        # Return to events list
        self.show_manage_events()
    
    # Delete event
    def delete_event(self, event):
        # Check if there are bookings for this event
        event_bookings = self.data_manager.get_bookings_by_event_id(event.get_event_id())
        
        if event_bookings:
            messagebox.showerror("Delete Error", 
                              "Cannot delete this event because there are bookings associated with it")
            return
        
        # Ask for confirmation
        confirm = messagebox.askyesno("Delete Event", 
                                    "Are you sure you want to delete this event? This action cannot be undone.")
        
        if confirm:
            # Delete event
            self.data_manager.delete_event(event.get_event_id())
            
            messagebox.showinfo("Event Deleted", "The event has been deleted successfully")
            
            # Refresh events list
            self.show_manage_events()
    
    # Manage users
    def show_manage_users(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create header
        header_frame = tk.Frame(self.content_frame, bg=self.bg_color, pady=20)
        header_frame.pack(fill='x')
        
        users_label = tk.Label(header_frame, text="Manage Users", 
                            font=("Helvetica", 18, "bold"), bg=self.bg_color)
        users_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="View and manage user accounts", 
                               font=("Helvetica", 10), bg=self.bg_color)
        subtitle_label.pack()
        
        # Create scrollable users list
        users_container = tk.Frame(self.content_frame, bg=self.bg_color)
        users_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create canvas with scrollbar for users
        canvas = tk.Canvas(users_container, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(users_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Get sorted customers by name
        sorted_customers = sorted(self.data_manager.customers, key=lambda c: c.get_user_name())
        
        if sorted_customers:
            for customer in sorted_customers:
                # Create user card
                user_card = tk.Frame(scrollable_frame, bg="white", bd=1, relief=tk.SOLID, padx=15, pady=15)
                user_card.pack(fill='x', padx=10, pady=10)
                
                # User details
                user_name = tk.Label(user_card, text=customer.get_user_name(), 
                                  font=("Helvetica", 14, "bold"), bg="white")
                user_name.grid(row=0, column=0, sticky='w', pady=(0, 5))
                
                user_id = tk.Label(user_card, text="ID: " + str(customer.get_user_id()), 
                                bg="white", fg="gray")
                user_id.grid(row=0, column=1, sticky='e')
                
                user_email = tk.Label(user_card, text="Email: " + customer.get_user_email(), 
                                   bg="white")
                user_email.grid(row=1, column=0, sticky='w')
                
                user_phone = tk.Label(user_card, text="Phone: " + str(customer.get_customer_phone()), 
                                   bg="white")
                user_phone.grid(row=2, column=0, sticky='w')
                
                user_address = tk.Label(user_card, text="Address: " + customer.get_customer_address(), 
                                     bg="white")
                user_address.grid(row=3, column=0, sticky='w')
                
                user_registered = tk.Label(user_card, 
                                        text="Registered: " + customer.get_registration_date().strftime("%B %d, %Y"),
                                        bg="white")
                user_registered.grid(row=4, column=0, sticky='w')
                
                # View bookings button
                bookings_button = tk.Button(user_card, text="View Bookings", 
                                         bg=self.accent_color, fg="white",
                                         command=lambda c=customer: self.show_user_bookings(c))
                bookings_button.grid(row=1, column=1, padx=(20, 0))
                
                # Delete button
                delete_button = tk.Button(user_card, text="Delete User", 
                                       bg="#ff6666", fg="white",
                                       command=lambda c=customer: self.delete_user(c))
                delete_button.grid(row=2, column=1, padx=(20, 0))
                
                # Set grid configuration
                user_card.columnconfigure(0, weight=1)
                user_card.columnconfigure(1, weight=0)
        else:
            no_users = tk.Label(scrollable_frame, text="No users available", 
                             font=("Helvetica", 12), bg=self.bg_color)
            no_users.pack(pady=50)
    
    # Show user's bookings
    def show_user_bookings(self, customer):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create header
        header_frame = tk.Frame(self.content_frame, bg=self.bg_color, pady=20)
        header_frame.pack(fill='x')
        
        bookings_label = tk.Label(header_frame, text="Bookings for " + customer.get_user_name(), 
                               font=("Helvetica", 18, "bold"), bg=self.bg_color)
        bookings_label.pack()
        
        # Back button
        back_button = tk.Button(header_frame, text="Back to Users", 
                             command=lambda: self.show_manage_users(),
                             bg="#f0f0f0", fg="black")
        back_button.pack(pady=10)
        
        # Create scrollable bookings list
        bookings_container = tk.Frame(self.content_frame, bg=self.bg_color)
        bookings_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Get user's bookings
        user_bookings = self.data_manager.get_bookings_by_user_id(customer.get_user_id())
        
        if user_bookings:
            # Sort bookings by date (newest first)
            sorted_bookings = sorted(user_bookings, key=lambda b: b.get_booking_date(), reverse=True)
            
            for booking in sorted_bookings:
                # Get related event
                event = self.data_manager.get_event_by_id(booking.get_event_id())
                if not event:
                    continue
                
                # Create booking card
                booking_card = tk.Frame(bookings_container, bg="white", bd=1, relief=tk.SOLID, padx=15, pady=15)
                booking_card.pack(fill='x', padx=10, pady=10)
                
                # Booking details
                booking_title = tk.Label(booking_card, 
                                      text="Booking ID: " + str(booking.get_booking_id()),
                                      font=("Helvetica", 14, "bold"), bg="white")
                booking_title.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 10))
                
                # Event name
                event_name = tk.Label(booking_card, text="Event: " + event.get_event_name(), bg="white")
                event_name.grid(row=1, column=0, sticky='w')
                
                # Event date and location
                event_info = tk.Label(booking_card, 
                                   text="Date: " + event.get_event_date().strftime("%B %d, %Y") + 
                                   " at " + event.get_event_location(),
                                   bg="white")
                event_info.grid(row=2, column=0, sticky='w')
                
                # Booking date
                booking_date = tk.Label(booking_card, 
                                     text="Booked on: " + booking.get_booking_date().strftime("%B %d, %Y"),
                                     bg="white")
                booking_date.grid(row=3, column=0, sticky='w')
                
                # Ticket count
                tickets_label = tk.Label(booking_card, text="Tickets: " + str(booking.get_number_of_tickets()), 
                                      bg="white")
                tickets_label.grid(row=4, column=0, sticky='w')
                
                # Total price
                price_label = tk.Label(booking_card, text="Total Price: $" + str(booking.get_total_price()), 
                                    bg="white")
                price_label.grid(row=5, column=0, sticky='w')
                
                # Status
                status_label = tk.Label(booking_card, 
                                     text="Status: " + booking.get_booking_status().value,
                                     bg="white", 
                                     fg="green" if booking.get_booking_status() == BookingStatus.CONFIRMED 
                                     else "orange" if booking.get_booking_status() == BookingStatus.PENDING
                                     else "red")
                status_label.grid(row=6, column=0, sticky='w')
                
                # Set grid configuration
                booking_card.columnconfigure(0, weight=1)
                booking_card.columnconfigure(1, weight=0)
        else:
            no_bookings = tk.Label(bookings_container, text="This user has no bookings", 
                                font=("Helvetica", 12), bg=self.bg_color)
            no_bookings.pack(pady=50)
    
    # Delete user
    def delete_user(self, customer):
        # Check if there are bookings for this user
        user_bookings = self.data_manager.get_bookings_by_user_id(customer.get_user_id())
        
        if user_bookings:
            messagebox.showerror("Delete Error", 
                              "Cannot delete this user because they have bookings associated with them")
            return
        
        # Ask for confirmation
        confirm = messagebox.askyesno("Delete User", 
                                    "Are you sure you want to delete this user? This action cannot be undone.")
        
        if confirm:
            # Delete user
            self.data_manager.delete_customer(customer.get_user_id())
            
            messagebox.showinfo("User Deleted", "The user has been deleted successfully")
            
            # Refresh users list
            self.show_manage_users()
    
    # Manage discounts
    def show_manage_discounts(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create header
        header_frame = tk.Frame(self.content_frame, bg=self.bg_color, pady=20)
        header_frame.pack(fill='x')
        
        discounts_label = tk.Label(header_frame, text="Manage Discounts", 
                                font=("Helvetica", 18, "bold"), bg=self.bg_color)
        discounts_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Add, edit, or delete discount codes", 
                               font=("Helvetica", 10), bg=self.bg_color)
        subtitle_label.pack()
        
        # Add discount button
        add_btn = tk.Button(header_frame, text="Add New Discount", 
                         bg="#4caf50", fg="white", padx=10, pady=5,
                         command=lambda: self.show_add_discount_form())
        add_btn.pack(pady=10)
        
        # Create discount list
        discounts_container = tk.Frame(self.content_frame, bg=self.bg_color)
        discounts_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Get discounts
        if self.data_manager.discounts:
            for discount in self.data_manager.discounts:
                # Create discount card
                discount_card = tk.Frame(discounts_container, bg="white", bd=1, relief=tk.SOLID, padx=15, pady=15)
                discount_card.pack(fill='x', padx=10, pady=10)
                
                # Discount details
                discount_code = tk.Label(discount_card, text=discount.get_discount_code(), 
                                      font=("Helvetica", 14, "bold"), bg="white")
                discount_code.grid(row=0, column=0, sticky='w', pady=(0, 5))
                
                discount_id = tk.Label(discount_card, text="ID: " + str(discount.get_discount_id()), 
                                    bg="white", fg="gray")
                discount_id.grid(row=0, column=1, sticky='e')
                
                # Display percentage or fixed amount
                if discount.get_discount_percentage() > 0:
                    discount_value = tk.Label(discount_card, 
                                           text="Discount: " + str(discount.get_discount_percentage()) + "%", 
                                           bg="white")
                else:
                    discount_value = tk.Label(discount_card, 
                                           text="Discount: $" + str(discount.get_discount_amount()), 
                                           bg="white")
                discount_value.grid(row=1, column=0, sticky='w')
                
                # Max amount
                max_amount = tk.Label(discount_card, 
                                   text="Maximum Discount: $" + str(discount.get_max_discount_amount()),
                                   bg="white")
                max_amount.grid(row=2, column=0, sticky='w')
                
                # Edit button
                edit_button = tk.Button(discount_card, text="Edit", 
                                     bg=self.accent_color, fg="white",
                                     command=lambda d=discount: self.show_edit_discount_form(d))
                edit_button.grid(row=1, column=1, padx=(20, 0))
                
                # Delete button
                delete_button = tk.Button(discount_card, text="Delete", 
                                       bg="#ff6666", fg="white",
                                       command=lambda d=discount: self.delete_discount(d))
                delete_button.grid(row=2, column=1, padx=(20, 0))
                
                # Set grid configuration
                discount_card.columnconfigure(0, weight=1)
                discount_card.columnconfigure(1, weight=0)
        else:
            no_discounts = tk.Label(discounts_container, text="No discounts available", 
                                 font=("Helvetica", 12), bg=self.bg_color)
            no_discounts.pack(pady=50)
    
    # Show add discount form
    def show_add_discount_form(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create header
        header_frame = tk.Frame(self.content_frame, bg=self.bg_color, pady=20)
        header_frame.pack(fill='x')
        
        add_label = tk.Label(header_frame, text="Add New Discount", 
                          font=("Helvetica", 18, "bold"), bg=self.bg_color)
        add_label.pack()
        
        # Create form container
        form_container = tk.Frame(self.content_frame, bg="white", bd=1, relief=tk.SOLID)
        form_container.pack(fill='both', expand=True, padx=100, pady=20)
        
        # Discount code field
        code_frame = tk.Frame(form_container, bg="white", pady=10)
        code_frame.pack(fill='x', padx=20)
        
        code_label = tk.Label(code_frame, text="Discount Code:", width=15, anchor='w', bg="white")
        code_label.pack(side=tk.LEFT)
        
        self.discount_code_entry = tk.Entry(code_frame, width=20)
        self.discount_code_entry.pack(side=tk.LEFT, padx=5)
        
        # Discount ID field
        id_frame = tk.Frame(form_container, bg="white", pady=10)
        id_frame.pack(fill='x', padx=20)
        
        id_label = tk.Label(id_frame, text="Discount ID:", width=15, anchor='w', bg="white")
        id_label.pack(side=tk.LEFT)
        
        # Auto-generate a discount ID
        next_id = max([d.get_discount_id() for d in self.data_manager.discounts], default=0) + 1
        
        self.discount_id_entry = tk.Entry(id_frame, width=10)
        self.discount_id_entry.insert(0, str(next_id))
        self.discount_id_entry.config(state='readonly')
        self.discount_id_entry.pack(side=tk.LEFT, padx=5)
        
        # Discount type selection
        type_frame = tk.Frame(form_container, bg="white", pady=10)
        type_frame.pack(fill='x', padx=20)
        
        type_label = tk.Label(type_frame, text="Discount Type:", width=15, anchor='w', bg="white")
        type_label.pack(side=tk.LEFT)
        
        self.discount_type_var = tk.StringVar(value="percentage")
        
        percentage_radio = tk.Radiobutton(type_frame, text="Percentage", 
                                        variable=self.discount_type_var, value="percentage", 
                                        bg="white", command=self.toggle_discount_fields)
        percentage_radio.pack(side=tk.LEFT, padx=5)
        
        amount_radio = tk.Radiobutton(type_frame, text="Fixed Amount", 
                                    variable=self.discount_type_var, value="amount", 
                                    bg="white", command=self.toggle_discount_fields)
        amount_radio.pack(side=tk.LEFT, padx=5)
        
        # Percentage field
        self.percentage_frame = tk.Frame(form_container, bg="white", pady=10)
        self.percentage_frame.pack(fill='x', padx=20)
        
        percentage_label = tk.Label(self.percentage_frame, text="Percentage (%):", width=15, anchor='w', bg="white")
        percentage_label.pack(side=tk.LEFT)
        
        self.percentage_entry = tk.Entry(self.percentage_frame, width=10)
        self.percentage_entry.pack(side=tk.LEFT, padx=5)
        
        # Amount field (hidden by default)
        self.amount_frame = tk.Frame(form_container, bg="white", pady=10)
        
        amount_label = tk.Label(self.amount_frame, text="Amount ($):", width=15, anchor='w', bg="white")
        amount_label.pack(side=tk.LEFT)
        
        self.amount_entry = tk.Entry(self.amount_frame, width=10)
        self.amount_entry.pack(side=tk.LEFT, padx=5)
        
        # Maximum discount amount field
        max_frame = tk.Frame(form_container, bg="white", pady=10)
        max_frame.pack(fill='x', padx=20)
        
        max_label = tk.Label(max_frame, text="Max Amount ($):", width=15, anchor='w', bg="white")
        max_label.pack(side=tk.LEFT)
        
        self.max_amount_entry = tk.Entry(max_frame, width=10)
        self.max_amount_entry.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = tk.Frame(form_container, bg="white", pady=20)
        button_frame.pack(fill='x', padx=20)
        
        # Back button
        back_button = tk.Button(button_frame, text="Cancel", 
                             command=lambda: self.show_manage_discounts(),
                             bg="#f0f0f0", fg="black", width=10)
        back_button.pack(side=tk.LEFT, padx=5)
        
        # Save button
        save_button = tk.Button(button_frame, text="Save Discount", 
                             command=lambda: self.save_discount(),
                             bg="#4caf50", fg="white", width=10)
        save_button.pack(side=tk.RIGHT, padx=5)
    
    # Toggle between percentage and amount discount fields
    def toggle_discount_fields(self):
        discount_type = self.discount_type_var.get()
        
        if discount_type == "percentage":
            self.amount_frame.pack_forget()
            self.percentage_frame.pack(fill='x', padx=20, after=self.discount_type_var.get())
        else:
            self.percentage_frame.pack_forget()
            self.amount_frame.pack(fill='x', padx=20, after=self.discount_type_var.get())
    
    # Save new discount
    def save_discount(self):
        # Get form values
        code = self.discount_code_entry.get()
        discount_id = int(self.discount_id_entry.get())
        discount_type = self.discount_type_var.get()
        max_amount_str = self.max_amount_entry.get()
        
        # Validate inputs
        if not code or not max_amount_str:
            messagebox.showerror("Input Error", "Discount code and maximum amount are required")
            return
        
        try:
            # Parse max amount
            max_amount = float(max_amount_str)
            if max_amount <= 0:
                raise ValueError("Maximum amount must be positive")
            
            # Parse percentage or amount based on type
            if discount_type == "percentage":
                percentage_str = self.percentage_entry.get()
                if not percentage_str:
                    raise ValueError("Percentage is required")
                    
                percentage = float(percentage_str)
                if percentage <= 0 or percentage > 100:
                    raise ValueError("Percentage must be between 1 and 100")
                
                amount = 0
            else:
                amount_str = self.amount_entry.get()
                if not amount_str:
                    raise ValueError("Amount is required")
                    
                amount = float(amount_str)
                if amount <= 0:
                    raise ValueError("Amount must be positive")
                
                percentage = 0
                
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return
        
        # Check if discount code already exists
        if self.data_manager.get_discount_by_code(code):
            messagebox.showerror("Input Error", "Discount code already exists")
            return
        
        # Create new discount
        new_discount = Discount(discount_id, percentage, amount, code, max_amount)
        
        # Add to data manager
        self.data_manager.add_discount(new_discount)
        
        messagebox.showinfo("Discount Added", "The discount has been added successfully")
        
        # Return to discounts list
        self.show_manage_discounts()
    
    # Show edit discount form
    def show_edit_discount_form(self, discount):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create header
        header_frame = tk.Frame(self.content_frame, bg=self.bg_color, pady=20)
        header_frame.pack(fill='x')
        
        edit_label = tk.Label(header_frame, text="Edit Discount", 
                           font=("Helvetica", 18, "bold"), bg=self.bg_color)
        edit_label.pack()
        
        # Create form container
        form_container = tk.Frame(self.content_frame, bg="white", bd=1, relief=tk.SOLID)
        form_container.pack(fill='both', expand=True, padx=100, pady=20)
        
        # Discount code field
        code_frame = tk.Frame(form_container, bg="white", pady=10)
        code_frame.pack(fill='x', padx=20)
        
        code_label = tk.Label(code_frame, text="Discount Code:", width=15, anchor='w', bg="white")
        code_label.pack(side=tk.LEFT)
        
        self.discount_code_entry = tk.Entry(code_frame, width=20)
        self.discount_code_entry.insert(0, discount.get_discount_code())
        self.discount_code_entry.pack(side=tk.LEFT, padx=5)
        
        # Discount ID field
        id_frame = tk.Frame(form_container, bg="white", pady=10)
        id_frame.pack(fill='x', padx=20)
        
        id_label = tk.Label(id_frame, text="Discount ID:", width=15, anchor='w', bg="white")
        id_label.pack(side=tk.LEFT)
        
        self.discount_id_entry = tk.Entry(id_frame, width=10)
        self.discount_id_entry.insert(0, str(discount.get_discount_id()))
        self.discount_id_entry.config(state='readonly')
        self.discount_id_entry.pack(side=tk.LEFT, padx=5)
        
        # Discount type selection
        type_frame = tk.Frame(form_container, bg="white", pady=10)
        type_frame.pack(fill='x', padx=20)
        
        type_label = tk.Label(type_frame, text="Discount Type:", width=15, anchor='w', bg="white")
        type_label.pack(side=tk.LEFT)
        
        # Determine current discount type
        current_type = "percentage" if discount.get_discount_percentage() > 0 else "amount"
        self.discount_type_var = tk.StringVar(value=current_type)
        
        percentage_radio = tk.Radiobutton(type_frame, text="Percentage", 
                                        variable=self.discount_type_var, value="percentage", 
                                        bg="white", command=self.toggle_discount_fields)
        percentage_radio.pack(side=tk.LEFT, padx=5)
        
        amount_radio = tk.Radiobutton(type_frame, text="Fixed Amount", 
                                    variable=self.discount_type_var, value="amount", 
                                    bg="white", command=self.toggle_discount_fields)
        amount_radio.pack(side=tk.LEFT, padx=5)
        
        # Percentage field
        self.percentage_frame = tk.Frame(form_container, bg="white", pady=10)
        
        percentage_label = tk.Label(self.percentage_frame, text="Percentage (%):", width=15, anchor='w', bg="white")
        percentage_label.pack(side=tk.LEFT)
        
        self.percentage_entry = tk.Entry(self.percentage_frame, width=10)
        self.percentage_entry.insert(0, str(discount.get_discount_percentage()))
        self.percentage_entry.pack(side=tk.LEFT, padx=5)
        
        # Amount field
        self.amount_frame = tk.Frame(form_container, bg="white", pady=10)
        
        amount_label = tk.Label(self.amount_frame, text="Amount ($):", width=15, anchor='w', bg="white")
        amount_label.pack(side=tk.LEFT)
        
        self.amount_entry = tk.Entry(self.amount_frame, width=10)
        self.amount_entry.insert(0, str(discount.get_discount_amount()))
        self.amount_entry.pack(side=tk.LEFT, padx=5)
        
        # Show appropriate frame based on current discount type
        if current_type == "percentage":
            self.percentage_frame.pack(fill='x', padx=20)
        else:
            self.amount_frame.pack(fill='x', padx=20)
        
        # Maximum discount amount field
        max_frame = tk.Frame(form_container, bg="white", pady=10)
        max_frame.pack(fill='x', padx=20)
        
        max_label = tk.Label(max_frame, text="Max Amount ($):", width=15, anchor='w', bg="white")
        max_label.pack(side=tk.LEFT)
        
        self.max_amount_entry = tk.Entry(max_frame, width=10)
        self.max_amount_entry.insert(0, str(discount.get_max_discount_amount()))
        self.max_amount_entry.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = tk.Frame(form_container, bg="white", pady=20)
        button_frame.pack(fill='x', padx=20)
        
        # Back button
        back_button = tk.Button(button_frame, text="Cancel", 
                             command=lambda: self.show_manage_discounts(),
                             bg="#f0f0f0", fg="black", width=10)
        back_button.pack(side=tk.LEFT, padx=5)
        
        # Update button
        update_button = tk.Button(button_frame, text="Update Discount", 
                               command=lambda: self.update_discount(discount),
                               bg="#4caf50", fg="white", width=10)
        update_button.pack(side=tk.RIGHT, padx=5)
    
    # Update existing discount
    def update_discount(self, discount):
        # Get form values
        code = self.discount_code_entry.get()
        discount_type = self.discount_type_var.get()
        max_amount_str = self.max_amount_entry.get()
        
        # Validate inputs
        if not code or not max_amount_str:
            messagebox.showerror("Input Error", "Discount code and maximum amount are required")
            return
        
        try:
            # Parse max amount
            max_amount = float(max_amount_str)
            if max_amount <= 0:
                raise ValueError("Maximum amount must be positive")
            
            # Parse percentage or amount based on type
            if discount_type == "percentage":
                percentage_str = self.percentage_entry.get()
                if not percentage_str:
                    raise ValueError("Percentage is required")
                    
                percentage = float(percentage_str)
                if percentage <= 0 or percentage > 100:
                    raise ValueError("Percentage must be between 1 and 100")
                
                amount = 0
            else:
                amount_str = self.amount_entry.get()
                if not amount_str:
                    raise ValueError("Amount is required")
                    
                amount = float(amount_str)
                if amount <= 0:
                    raise ValueError("Amount must be positive")
                
                percentage = 0
                
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return
        
        # Check if discount code already exists (except for this discount)
        existing_discount = self.data_manager.get_discount_by_code(code)
        if existing_discount and existing_discount.get_discount_id() != discount.get_discount_id():
            messagebox.showerror("Input Error", "Discount code already exists")
            return
        
        # Update discount
        discount.set_discount_code(code)
        discount.set_discount_percentage(percentage)
        discount.set_discount_amount(amount)
        discount.set_max_discount_amount(max_amount)
        
        # Update in data manager
        self.data_manager.update_discount(discount)
        
        messagebox.showinfo("Discount Updated", "The discount has been updated successfully")
        
        # Return to discounts list
        self.show_manage_discounts()
    
    # Delete discount
    def delete_discount(self, discount):
        # Ask for confirmation
        confirm = messagebox.askyesno("Delete Discount", 
                                    "Are you sure you want to delete this discount? This action cannot be undone.")
        
        if confirm:
            # Delete discount
            self.data_manager.delete_discount(discount.get_discount_id())
            
            messagebox.showinfo("Discount Deleted", "The discount has been deleted successfully")
            
            # Refresh discounts list
            self.show_manage_discounts()
    
    # Show booking reports
    def show_booking_reports(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create header
        header_frame = tk.Frame(self.content_frame, bg=self.bg_color, pady=20)
        header_frame.pack(fill='x')
        
        reports_label = tk.Label(header_frame, text="Booking Reports", 
                              font=("Helvetica", 18, "bold"), bg=self.bg_color)
        reports_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="View booking statistics and reports", 
                               font=("Helvetica", 10), bg=self.bg_color)
        subtitle_label.pack()
        
        # Create tabs for different reports
        tab_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        tab_frame.pack(fill='x', padx=20, pady=10)
        
        # Tab buttons
        daily_btn = tk.Button(tab_frame, text="Daily Sales", 
                           bg=self.accent_color, fg="white", padx=15, pady=5,
                           command=lambda: self.show_daily_sales())
        daily_btn.pack(side=tk.LEFT, padx=5)
        
        event_btn = tk.Button(tab_frame, text="Sales by Event", 
                           bg="#f0f0f0", fg="black", padx=15, pady=5,
                           command=lambda: self.show_event_sales())
        event_btn.pack(side=tk.LEFT, padx=5)
        
        all_bookings_btn = tk.Button(tab_frame, text="All Bookings", 
                                  bg="#f0f0f0", fg="black", padx=15, pady=5,
                                  command=lambda: self.show_all_bookings())
        all_bookings_btn.pack(side=tk.LEFT, padx=5)
        
        # Create container for report content
        self.report_container = tk.Frame(self.content_frame, bg="white", bd=1, relief=tk.SOLID)
        self.report_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Show daily sales by default
        self.show_daily_sales()
    
    # Show daily sales report
    def show_daily_sales(self):
        # Clear report container
        for widget in self.report_container.winfo_children():
            widget.destroy()
        
        # Create report header
        report_header = tk.Frame(self.report_container, bg="white", pady=15)
        report_header.pack(fill='x', padx=20)
        
        header_label = tk.Label(report_header, text="Daily Ticket Sales", 
                             font=("Helvetica", 14, "bold"), bg="white")
        header_label.pack(anchor='w')
        
        # Group bookings by date
        date_sales = {}
        for booking in self.data_manager.bookings:
            date_key = booking.get_booking_date().strftime("%Y-%m-%d")
            
            if date_key not in date_sales:
                date_sales[date_key] = {
                    "count": 0,
                    "tickets": 0,
                    "revenue": 0
                }
            
            date_sales[date_key]["count"] += 1
            date_sales[date_key]["tickets"] += booking.get_number_of_tickets()
            date_sales[date_key]["revenue"] += booking.get_total_price()
        
        # Sort dates
        sorted_dates = sorted(date_sales.keys(), reverse=True)
        
        # Create table header
        table_frame = tk.Frame(self.report_container, bg="white")
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Table header
        header_frame = tk.Frame(table_frame, bg="#f0f0f0")
        header_frame.pack(fill='x')
        
        date_header = tk.Label(header_frame, text="Date", width=15, font=("Helvetica", 11, "bold"), 
                            bg="#f0f0f0", padx=10, pady=5)
        date_header.grid(row=0, column=0, sticky='w')
        
        bookings_header = tk.Label(header_frame, text="Bookings", width=10, font=("Helvetica", 11, "bold"), 
                                bg="#f0f0f0", padx=10, pady=5)
        bookings_header.grid(row=0, column=1, sticky='w')
        
        tickets_header = tk.Label(header_frame, text="Tickets", width=10, font=("Helvetica", 11, "bold"), 
                               bg="#f0f0f0", padx=10, pady=5)
        tickets_header.grid(row=0, column=2, sticky='w')
        
        revenue_header = tk.Label(header_frame, text="Revenue", width=15, font=("Helvetica", 11, "bold"), 
                               bg="#f0f0f0", padx=10, pady=5)
        revenue_header.grid(row=0, column=3, sticky='w')
        
        # Configure grid
        header_frame.columnconfigure(0, weight=0)
        header_frame.columnconfigure(1, weight=0)
        header_frame.columnconfigure(2, weight=0)
        header_frame.columnconfigure(3, weight=1)
        
        # Create scrollable table content
        table_content = tk.Frame(table_frame, bg="white")
        table_content.pack(fill='both', expand=True)
        
        # Create canvas with scrollbar
        canvas = tk.Canvas(table_content, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(table_content, orient="vertical", command=canvas.yview)
        scrollable_table = tk.Frame(canvas, bg="white")
        
        scrollable_table.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_table, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Table rows
        total_bookings = 0
        total_tickets = 0
        total_revenue = 0
        
        for i, date in enumerate(sorted_dates):
            sales = date_sales[date]
            row_bg = "#f9f9f9" if i % 2 == 0 else "white"
            
            # Date
            date_label = tk.Label(scrollable_table, text=date, width=15, 
                               bg=row_bg, padx=10, pady=5)
            date_label.grid(row=i, column=0, sticky='w')
            
            # Bookings
            bookings_label = tk.Label(scrollable_table, text=str(sales["count"]), width=10, 
                                   bg=row_bg, padx=10, pady=5)
            bookings_label.grid(row=i, column=1, sticky='w')
            
            # Tickets
            tickets_label = tk.Label(scrollable_table, text=str(sales["tickets"]), width=10, 
                                  bg=row_bg, padx=10, pady=5)
            tickets_label.grid(row=i, column=2, sticky='w')
            
            # Revenue
            revenue_label = tk.Label(scrollable_table, text="$" + str(sales["revenue"]), width=15, 
                                  bg=row_bg, padx=10, pady=5)
            revenue_label.grid(row=i, column=3, sticky='w')
            
            # Update totals
            total_bookings += sales["count"]
            total_tickets += sales["tickets"]
            total_revenue += sales["revenue"]
            
            # Configure grid
            scrollable_table.columnconfigure(0, weight=0)
            scrollable_table.columnconfigure(1, weight=0)
            scrollable_table.columnconfigure(2, weight=0)
            scrollable_table.columnconfigure(3, weight=1)
        
        # Add totals row
        total_separator = ttk.Separator(self.report_container, orient='horizontal')
        total_separator.pack(fill='x', padx=20)
        
        total_frame = tk.Frame(self.report_container, bg="white", pady=10)
        total_frame.pack(fill='x', padx=20)
        
        total_label = tk.Label(total_frame, text="Totals:", font=("Helvetica", 11, "bold"), 
                            bg="white", width=15)
        total_label.grid(row=0, column=0, sticky='w', padx=10)
        
        total_bookings_label = tk.Label(total_frame, text=str(total_bookings), 
                                     font=("Helvetica", 11), bg="white", width=10)
        total_bookings_label.grid(row=0, column=1, sticky='w', padx=10)
        
        total_tickets_label = tk.Label(total_frame, text=str(total_tickets), 
                                    font=("Helvetica", 11), bg="white", width=10)
        total_tickets_label.grid(row=0, column=2, sticky='w', padx=10)
        
        total_revenue_label = tk.Label(total_frame, text="$" + str(total_revenue), 
                                    font=("Helvetica", 11, "bold"), bg="white", width=15)
        total_revenue_label.grid(row=0, column=3, sticky='w', padx=10)
        
        # Configure grid
        total_frame.columnconfigure(0, weight=0)
        total_frame.columnconfigure(1, weight=0)
        total_frame.columnconfigure(2, weight=0)
        total_frame.columnconfigure(3, weight=1)
    
    # Show sales by event report
    def show_event_sales(self):
        # Clear report container
        for widget in self.report_container.winfo_children():
            widget.destroy()
        
        # Create report header
        report_header = tk.Frame(self.report_container, bg="white", pady=15)
        report_header.pack(fill='x', padx=20)
        
        header_label = tk.Label(report_header, text="Sales by Event", 
                             font=("Helvetica", 14, "bold"), bg="white")
        header_label.pack(anchor='w')
        
        # Group bookings by event
        event_sales = {}
        for booking in self.data_manager.bookings:
            event_id = booking.get_event_id()
            event = self.data_manager.get_event_by_id(event_id)
            
            if not event:
                continue
                
            event_key = str(event_id)
            
            if event_key not in event_sales:
                event_sales[event_key] = {
                    "name": event.get_event_name(),
                    "date": event.get_event_date(),
                    "count": 0,
                    "tickets": 0,
                    "revenue": 0
                }
            
            event_sales[event_key]["count"] += 1
            event_sales[event_key]["tickets"] += booking.get_number_of_tickets()
            event_sales[event_key]["revenue"] += booking.get_total_price()
        
        # Sort events by date
        sorted_events = sorted(event_sales.items(), key=lambda x: x[1]["date"])
        
        # Create table header
        table_frame = tk.Frame(self.report_container, bg="white")
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Table header
        header_frame = tk.Frame(table_frame, bg="#f0f0f0")
        header_frame.pack(fill='x')
        
        event_header = tk.Label(header_frame, text="Event", width=30, font=("Helvetica", 11, "bold"), 
                             bg="#f0f0f0", padx=10, pady=5)
        event_header.grid(row=0, column=0, sticky='w')
        
        date_header = tk.Label(header_frame, text="Date", width=15, font=("Helvetica", 11, "bold"), 
                            bg="#f0f0f0", padx=10, pady=5)
        date_header.grid(row=0, column=1, sticky='w')
        
        bookings_header = tk.Label(header_frame, text="Bookings", width=10, font=("Helvetica", 11, "bold"), 
                                bg="#f0f0f0", padx=10, pady=5)
        bookings_header.grid(row=0, column=2, sticky='w')
        
        tickets_header = tk.Label(header_frame, text="Tickets", width=10, font=("Helvetica", 11, "bold"), 
                               bg="#f0f0f0", padx=10, pady=5)
        tickets_header.grid(row=0, column=3, sticky='w')
        
        revenue_header = tk.Label(header_frame, text="Revenue", width=15, font=("Helvetica", 11, "bold"), 
                               bg="#f0f0f0", padx=10, pady=5)
        revenue_header.grid(row=0, column=4, sticky='w')
        
        # Configure grid
        header_frame.columnconfigure(0, weight=1)
        header_frame.columnconfigure(1, weight=0)
        header_frame.columnconfigure(2, weight=0)
        header_frame.columnconfigure(3, weight=0)
        header_frame.columnconfigure(4, weight=0)
        
        # Create table content
        content_frame = tk.Frame(table_frame, bg="white")
        content_frame.pack(fill='both', expand=True)
        
        # Table rows
        total_bookings = 0
        total_tickets = 0
        total_revenue = 0
        
        for i, (event_id, sales) in enumerate(sorted_events):
            row_bg = "#f9f9f9" if i % 2 == 0 else "white"
            
            # Event
            event_label = tk.Label(content_frame, text=sales["name"], 
                                bg=row_bg, padx=10, pady=5, anchor='w')
            event_label.grid(row=i, column=0, sticky='w')
            
            # Date
            date_label = tk.Label(content_frame, text=sales["date"].strftime("%Y-%m-%d"), 
                               bg=row_bg, padx=10, pady=5)
            date_label.grid(row=i, column=1, sticky='w')
            
            # Bookings
            bookings_label = tk.Label(content_frame, text=str(sales["count"]), 
                                   bg=row_bg, padx=10, pady=5)
            bookings_label.grid(row=i, column=2, sticky='w')
            
            # Tickets
            tickets_label = tk.Label(content_frame, text=str(sales["tickets"]), 
                                  bg=row_bg, padx=10, pady=5)
            tickets_label.grid(row=i, column=3, sticky='w')
            
            # Revenue
            revenue_label = tk.Label(content_frame, text="$" + str(sales["revenue"]), 
                                  bg=row_bg, padx=10, pady=5)
            revenue_label.grid(row=i, column=4, sticky='w')
            
            # Update totals
            total_bookings += sales["count"]
            total_tickets += sales["tickets"]
            total_revenue += sales["revenue"]
            
            # Configure grid
            content_frame.columnconfigure(0, weight=1)
            content_frame.columnconfigure(1, weight=0)
            content_frame.columnconfigure(2, weight=0)
            content_frame.columnconfigure(3, weight=0)
            content_frame.columnconfigure(4, weight=0)
        
        # Add totals row
        total_separator = ttk.Separator(self.report_container, orient='horizontal')
        total_separator.pack(fill='x', padx=20)
        
        total_frame = tk.Frame(self.report_container, bg="white", pady=10)
        total_frame.pack(fill='x', padx=20)
        
        total_label = tk.Label(total_frame, text="Totals:", font=("Helvetica", 11, "bold"), 
                            bg="white")
        total_label.grid(row=0, column=0, sticky='e', padx=10)
        
        total_bookings_label = tk.Label(total_frame, text=str(total_bookings), 
                                     font=("Helvetica", 11), bg="white", width=10)
        total_bookings_label.grid(row=0, column=2, sticky='w', padx=10)
        
        total_tickets_label = tk.Label(total_frame, text=str(total_tickets), 
                                    font=("Helvetica", 11), bg="white", width=10)
        total_tickets_label.grid(row=0, column=3, sticky='w', padx=10)
        
        total_revenue_label = tk.Label(total_frame, text="$" + str(total_revenue), 
                                    font=("Helvetica", 11, "bold"), bg="white", width=15)
        total_revenue_label.grid(row=0, column=4, sticky='w', padx=10)
        
        # Configure grid
        total_frame.columnconfigure(0, weight=1)
        total_frame.columnconfigure(1, weight=0)
        total_frame.columnconfigure(2, weight=0)
        total_frame.columnconfigure(3, weight=0)
        total_frame.columnconfigure(4, weight=0)
    
    # Show all bookings report
    def show_all_bookings(self):
        # Clear report container
        for widget in self.report_container.winfo_children():
            widget.destroy()
        
        # Create report header
        report_header = tk.Frame(self.report_container, bg="white", pady=15)
        report_header.pack(fill='x', padx=20)
        
        header_label = tk.Label(report_header, text="All Bookings", 
                             font=("Helvetica", 14, "bold"), bg="white")
        header_label.pack(anchor='w')
        
        # Create table header
        table_frame = tk.Frame(self.report_container, bg="white")
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Table header
        header_frame = tk.Frame(table_frame, bg="#f0f0f0")
        header_frame.pack(fill='x')
        
        booking_header = tk.Label(header_frame, text="Booking ID", width=10, font=("Helvetica", 11, "bold"), 
                               bg="#f0f0f0", padx=10, pady=5)
        booking_header.grid(row=0, column=0, sticky='w')
        
        date_header = tk.Label(header_frame, text="Date", width=15, font=("Helvetica", 11, "bold"), 
                            bg="#f0f0f0", padx=10, pady=5)
        date_header.grid(row=0, column=1, sticky='w')
        
        user_header = tk.Label(header_frame, text="User", width=20, font=("Helvetica", 11, "bold"), 
                            bg="#f0f0f0", padx=10, pady=5)
        user_header.grid(row=0, column=2, sticky='w')
        
        event_header = tk.Label(header_frame, text="Event", width=25, font=("Helvetica", 11, "bold"), 
                             bg="#f0f0f0", padx=10, pady=5)
        event_header.grid(row=0, column=3, sticky='w')
        
        tickets_header = tk.Label(header_frame, text="Tickets", width=10, font=("Helvetica", 11, "bold"), 
                               bg="#f0f0f0", padx=10, pady=5)
        tickets_header.grid(row=0, column=4, sticky='w')
        
        total_header = tk.Label(header_frame, text="Total", width=10, font=("Helvetica", 11, "bold"), 
                             bg="#f0f0f0", padx=10, pady=5)
        total_header.grid(row=0, column=5, sticky='w')
        
        status_header = tk.Label(header_frame, text="Status", width=10, font=("Helvetica", 11, "bold"), 
                              bg="#f0f0f0", padx=10, pady=5)
        status_header.grid(row=0, column=6, sticky='w')
        
        # Configure grid
        header_frame.columnconfigure(0, weight=0)
        header_frame.columnconfigure(1, weight=0)
        header_frame.columnconfigure(2, weight=0)
        header_frame.columnconfigure(3, weight=1)
        header_frame.columnconfigure(4, weight=0)
        header_frame.columnconfigure(5, weight=0)
        header_frame.columnconfigure(6, weight=0)
        
        # Create scrollable table content
        content_container = tk.Frame(table_frame, bg="white")
        content_container.pack(fill='both', expand=True)
        
        # Create canvas with scrollbar
        canvas = tk.Canvas(content_container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_container, orient="vertical", command=canvas.yview)
        scrollable_content = tk.Frame(canvas, bg="white")
        
        scrollable_content.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Sort bookings by date (newest first)
        sorted_bookings = sorted(self.data_manager.bookings, key=lambda b: b.get_booking_date(), reverse=True)
        
        # Table rows
        for i, booking in enumerate(sorted_bookings):
            row_bg = "#f9f9f9" if i % 2 == 0 else "white"
            
            # Get related user and event
            user = self.data_manager.get_customer_by_id(booking.get_user_id())
            event = self.data_manager.get_event_by_id(booking.get_event_id())
            
            if not user or not event:
                continue
            
            # Booking ID
            booking_label = tk.Label(scrollable_content, text=str(booking.get_booking_id()), 
                                  bg=row_bg, padx=10, pady=5)
            booking_label.grid(row=i, column=0, sticky='w')
            
            # Date
            date_label = tk.Label(scrollable_content, text=booking.get_booking_date().strftime("%Y-%m-%d"), 
                               bg=row_bg, padx=10, pady=5)
            date_label.grid(row=i, column=1, sticky='w')
            
            # User
            user_label = tk.Label(scrollable_content, text=user.get_user_name(), 
                               bg=row_bg, padx=10, pady=5)
            user_label.grid(row=i, column=2, sticky='w')
            
            # Event
            event_label = tk.Label(scrollable_content, text=event.get_event_name(), 
                                bg=row_bg, padx=10, pady=5)
            event_label.grid(row=i, column=3, sticky='w')
            
            # Tickets
            tickets_label = tk.Label(scrollable_content, text=str(booking.get_number_of_tickets()), 
                                  bg=row_bg, padx=10, pady=5)
            tickets_label.grid(row=i, column=4, sticky='w')
            
            # Total
            total_label = tk.Label(scrollable_content, text="$" + str(booking.get_total_price()), 
                                bg=row_bg, padx=10, pady=5)
            total_label.grid(row=i, column=5, sticky='w')
            
            # Status (with color)
            status_text = booking.get_booking_status().value
            status_color = "green" if booking.get_booking_status() == BookingStatus.CONFIRMED else \
                          "orange" if booking.get_booking_status() == BookingStatus.PENDING else "red"
            
            status_label = tk.Label(scrollable_content, text=status_text, 
                                 bg=row_bg, fg=status_color, padx=10, pady=5)
            status_label.grid(row=i, column=6, sticky='w')
            
            # Configure grid
            scrollable_content.columnconfigure(0, weight=0)
            scrollable_content.columnconfigure(1, weight=0)
            scrollable_content.columnconfigure(2, weight=0)
            scrollable_content.columnconfigure(3, weight=1)
            scrollable_content.columnconfigure(4, weight=0)
            scrollable_content.columnconfigure(5, weight=0)
            scrollable_content.columnconfigure(6, weight=0)
    
    # Logout
    def logout(self):
        self.current_user = None
        self.is_admin = False
        self.create_login_frame()

# Main function to run the application
def main():
    root = tk.Tk()
    app = GrandPrixApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()