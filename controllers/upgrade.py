# -*- coding: utf-8 -*-

from general_helpers import max_string_length
from general_helpers import get_ajax_loader

from openstudio.openstudio import Invoice, WorkshopProduct

from os_upgrade import set_version


def to_login(var=None):
    redirect(URL('default', 'user', args=['login']))


def index():
    """
        This function executes commands needed for upgrades to new versions
    """
    # first check if a version is set
    if not db.sys_properties(Property='Version'):
        db.sys_properties.insert(Property='Version',
                                 PropertyValue=0)
        db.sys_properties.insert(Property='VersionRelease',
                                 PropertyValue=0)

    # check if a version is set and get it
    if db.sys_properties(Property='Version'):
        version = float(db.sys_properties(Property='Version').PropertyValue)

        if version < 2018.1:
            print version
            session.flash = T("Please upgrade to at least 2018.1 before running upgrade for any later versions")

        if version < 2018.2:
            print version
            upgrade_to_20182()
            session.flash = T("Upgraded db to 2018.2")
        else:
            session.flash = T('Already up to date')

        if version < 2018.3:
            print version
            upgrade_to_20183()
            session.flash = T("Upgraded db to 2018.3")
        else:
            session.flash = T('Already up to date')

        if version < 2018.4:
            print version
            upgrade_to_20184()
            session.flash = T("Upgraded db to 2018.4")
        else:
            session.flash = T('Already up to date')

        # always renew permissions for admin group after update
        set_permissions_for_admin_group()

    set_version()

    # Clear system properties cache
    cache_clear_sys_properties()

    # Clear menu cache
    cache_clear_menu_backend()

    # Back to square one
    to_login()


def upgrade_to_20181():
    """
        Upgrade operations to 2018.1
    """
    ##
    # clear cache
    ##
    cache.ram.clear(regex='.*')

    ##
    # Set sorting order for subscriptions
    ##
    query = (db.school_subscriptions.SortOrder == None)
    db(query).update(SortOrder = 0)

    ##
    # Create default subscription group, add all subscriptions to it and give the group full permissions for each class
    # to maintain similar behaviour compared to before the update
    ##

    # Subscriptions
    ssgID = db.school_subscriptions_groups.insert(
        Name = 'All subscriptions',
        Description = 'All subscriptions',
    )

    query = (db.school_subscriptions.Archived == False)
    rows = db(query).select(db.school_subscriptions.ALL)
    for row in rows:
        db.school_subscriptions_groups_subscriptions.insert(
            school_subscriptions_id = row.id,
            school_subscriptions_groups_id = ssgID
        )

    # Class cards
    scgID = db.school_classcards_groups.insert(
        Name = 'All class cards',
        Description = 'All class cards'
    )

    query = (db.school_classcards.Archived == False)
    rows = db(query).select(db.school_classcards.ALL)
    for row in rows:
        db.school_classcards_groups_classcards.insert(
            school_classcards_id = row.id,
            school_classcards_groups_id = scgID
        )

    # Link subscription & class card groups to classes and give permissions
    rows = db(db.classes).select(db.classes.ALL)
    for row in rows:
        db.classes_school_subscriptions_groups.insert(
            classes_id = row.id,
            school_subscriptions_groups_id = ssgID,
            Enroll = True,
            ShopBook = True,
            Attend = True
        )

        db.classes_school_classcards_groups.insert(
            classes_id = row.id,
            school_classcards_groups_id = scgID,
            Enroll = True,
            ShopBook = True,
            Attend = True
        )

    ##
    # set Booking status to attending for all historical data in classes_attendance
    ##
    query = (db.classes_attendance.BookingStatus == None)
    db(query).update(BookingStatus='attending')
    # TODO: repeat the 2 lines above for all coming upgrades


def upgrade_to_20182():
    """
        Upgrade operations to 2018.2
    """
    ##
    # Set archived customers to deleted
    ##
    query = (db.auth_user.archived == True)
    db(query).update(trashed = True)

    ##
    # Set archived for all users to False
    ##
    db(db.auth_user).update(archived = False)

    ##
    # Migrate links to invoices
    ##
    query = (db.invoices)
    rows = db(query).select(db.invoices.ALL)
    for row in rows:
        iID = row.id
        db.invoices_customers.insert(
            invoices_id = iID,
            auth_customer_id = row.auth_customer_id
        )

        if row.customers_subscriptions_id:
            db.invoices_customers_subscriptions.insert(
                invoices_id = iID,
                customers_subscriptions_id = row.customers_subscriptions_id
            )

    db(query).update(auth_customer_id = None,
                     customers_subscriptions_id = None)

    ##
    # Set default values for createdOn fields
    ##
    # auth_user
    now = datetime.datetime.now()
    query = (db.auth_user.created_on == None)
    db(query).update(created_on = now)

    # workshops_products_customers
    query = (db.workshops_products_customers.CreatedOn == None)
    db(query).update(CreatedOn = now)

    ##
    # Clean up old tables
    ##
    tables = [
        'paymentsummary',
        'overduepayments',
        'customers_payments',
        'workshops_messages',
        'workshops_products_messages',
        'customers_subscriptions_exceeded'
    ]

    for table in tables:
        try:
            db.executesql('''DROP TABLE '{table'}'''.format(table=table))
        except:
            pass

    ##
    # Remove email from merges customers
    ##
    query = (db.auth_user.merged_into != None)
    db(query).update(email=None)

    ##
    # set Booking status to attending for all historical data in classes_attendance
    ##
    query = (db.classes_attendance.BookingStatus == None)
    db(query).update(BookingStatus='attending')

    ##
    # clear cache
    ##
    cache.ram.clear(regex='.*')


def upgrade_to_20183():
    """
        Upgrade operations to 2018.3
    """
    ##
    # Set invoice customer data
    ##
    query = (db.invoices_customers.id > 0)

    rows = db(query).select(db.invoices_customers.ALL)
    for row in rows:
        invoice = Invoice(row.invoices_id)
        invoice.set_customer_info(row.auth_customer_id)

    ##
    # clear cache
    ##
    cache.ram.clear(regex='.*')


def upgrade_to_20184():
    """
        Upgrade operations to 2018.4
    """
    ##
    # Set default value for db.classes.AllowShopTrial
    ##
    query = (db.classes.AllowShopTrial == None)
    db(query).update(AllowShopTrial = False)

    ##
    # clear cache
    ##
    cache.ram.clear(regex='.*')


def upgrade_to_20185():
    """
        Upgrade operations to 2018.5
    """
    ##
    # Set default group for teacher credit invoices
    ##
    db.invoices_groups_product_types.insert(
        ProductType='teacher_payments',
        invoices_groups_id=100
    )

    ##
    # clear cache
    ##
    cache.ram.clear(regex='.*')