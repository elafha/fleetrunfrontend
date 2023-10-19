from django.core.validators import RegexValidator
from django.db import models
from uuid import uuid4
from datetime import datetime


# creating a default str id for each model based on uuid instead of serial number
def create_guid():
    return str(uuid4())


# Create your models here.
# ------------------------
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: "
                                                               "'+999999999'. Up to 15 digits allowed.")


# User Model // the main models of all types of users
class User(models.Model):
    id = models.UUIDField(primary_key=True, verbose_name='ID', default=create_guid)  # id
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=255, unique=True)  # username
    # -------------
    # if the user forget the password he can reset it by the email
    email = models.EmailField(max_length=50, unique=True)  # user's email
    # -------------
    # if the user forget the password he can reset it by the phone number
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # Validators should be a list
    # the phone number, we activate this user by its phone number
    # -------------
    password = models.TextField(max_length=50)  # the password
    created_at = models.DateTimeField(default=str(datetime.now()))  # the date that this user created this account
    date_joined = models.DateTimeField(default=str(datetime.now()))  # the date that this user activated this account
    is_superuser = models.BooleanField(default=False)  # is this user a superuser
    last_login = models.DateTimeField(default=str(datetime.now()))  # the last time that this user used our system

    def __str__(self):
        return self.username


class Address(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)  # id
    name = models.CharField(max_length=50)  # the address place: home, work, university, school, or something else
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    # --------------- we can send the (longitude+latitude) at least if the map link doesn't exist --------------- #
    longitude = models.IntegerField()  # the longitude of the address # it should be a number
    latitude = models.IntegerField()  # the latitude of the address  # it should be a number
    map_link = models.TextField(verbose_name="map")  # the link of the map to make it easier for navigation


class Agent(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)  # id
    # the link of the image that already stored (the logo of the agent's company)
    image = models.TextField()
    # the agent should have a user in our records
    user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    # the address of our agent
    address_id = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)
    # is this agent a main branch or sub branch
    is_main_branch = models.BooleanField()


class Driver(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)  # id
    image = models.TextField()  # the link to driver's image in our storage (its optional)
    user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)  # the driver has a user in our records
    # we have a drivers are working as an employee in our company, whereas the part-time job is available too
    is_freelance = models.BooleanField()
    # # the user who added this driver to our records | hint: it could be a super admin,
    # # or any member has the permission to add a driver
    # added_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


class MemberType(models.Model):
    # Constants in Model class
    DRIVER = 'driver'
    EMPLOYEE = 'employee'
    MEMBER_CHOICES = (
        (DRIVER, 'driver'),
        (EMPLOYEE, 'employee'),
    )

    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)  # id
    # driver or member with permissions the manager will specify
    name = models.CharField(max_length=50, choices=MEMBER_CHOICES, default=DRIVER)


class SystemMember(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)  # id
    # our system member who has a permission specified by the manager
    user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    # the type of the member could be driver, manager, supervisor or something else based on the permissions
    member_type_id = models.ForeignKey(MemberType, null=True, on_delete=models.CASCADE)


class AgentMember(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)  # id
    # agent's member who has a specific permissions added by a manager in the agent side
    user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    # the type of the member could be a driver or something else based on the permissions
    member_type_id = models.ForeignKey(MemberType, null=True, on_delete=models.CASCADE)


class Customer(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)  # id
    name = models.CharField(max_length=255)  # the name of the customer if exists
    number = models.IntegerField()  # customer's phone number


class Order(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)  # id
    added_at = models.DateTimeField()  # the datetime of creating this order
    # who add this order | the most time will be the restaurant but sometimes could be from our side
    added_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    # the driver will deliver the order
    driver_id = models.ForeignKey(Driver, null=True, on_delete=models.CASCADE)
    # where the driver should deliver the order | the customer's address
    # we put the address in order table because the customer could order for someone else with different address
    address_id = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)


class OrderItem(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)  # id
    name = models.CharField(max_length=255)  # the order name that has been added by the agent
    description = models.TextField()  # the description for the added order
    # the order code | at lease 6 digits (we can use regEXP to specify that or random number consists of 6 digits)
    code = models.IntegerField()


# we add this table to prevent redundancy in order item table because the same order could choose more than one time
class OrderData(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)
    # the order item id | this item added to specific order
    order_item_id = models.ForeignKey(OrderItem, null=True, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, null=False, on_delete=models.CASCADE)  # the order id


# # we created this table to track the address if changed more than one time during the trip
# class DeliveryOrder(models.Model):
#     id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)  # id
#     order_id = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)  # the order id
#     address_id = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)  # the address of the order


# class Policy(models.Model):
#     pass

# group of permissions
class Role(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)  # id
    name = models.CharField(max_length=50)
    # specifying which user added this role to the system,
    # hint: this role could be used by another user if he has the ability to access it
    added_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


class Permission(models.Model):
    # Constants in Model class
    ADMIN = 'admin'
    ORDER = 'order'
    DRIVER = 'driver'
    EMPLOYEE = 'member'
    FINANCE = 'finance'
    MEMBER_CHOICES = (
        (ADMIN, 'admin'),
        (ORDER, 'order'),
        (DRIVER, 'driver'),
        (EMPLOYEE, 'member'),
        (FINANCE, 'finance')
    )

    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)  # id
    # like a title of what this permission exactly doing
    name = models.CharField(max_length=50)
    # specifying the label of the permissions
    # it could belong to the driver (for ex: giving the ability to display the driver's data)
    label = models.CharField(max_length=50, choices=MEMBER_CHOICES, default=ADMIN)
    # the code of the permission's name we use it as an id of the permission
    codename = models.CharField(max_length=50, unique=True)


# group of permissions belong to a role
class RolePermissions(models.Model):
    permission_id = models.ForeignKey(Permission, null=True, on_delete=models.CASCADE)  # id of permission already added
    role_id = models.ForeignKey(Role, null=True, on_delete=models.CASCADE)  # id of role already added


class RoleMember(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)  # id
    role_id = models.ForeignKey(Role, null=True, on_delete=models.CASCADE)
    # the member who has the current role
    # the member could be added by the main user or someone else has the ability accessing and editing the role members
    member_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)





