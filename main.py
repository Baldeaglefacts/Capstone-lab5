"""
A menu - you need to add the database and fill in the functions. 
"""
from peewee import *

db = SqliteDatabase('chainsawJuggling.sqlite')


class Record(Model):
    """The record class, which sets up what information will be saved for each juggling record.
    This includes the person that set the record, their country of origin, and the number of juggles they got."""
    name = CharField()
    country = CharField()
    number_of_catches = IntegerField()

    class Meta:
        database = db

    def __str__(self):
        return f'{self.name}   {self.country}   {self.number_of_catches} catches'


db.connect()
db.create_tables([Record])


def main():
    menu_text = """
    1. Display all records
    2. Add new record
    3. Edit existing record
    4. Delete record
    5. Quit
    """

    while True:
        print(menu_text)
        choice = input('Enter your choice: ')
        if choice == '1':
            display_all_records()
        elif choice == '2':
            add_new_record()
        elif choice == '3':
            edit_existing_record()
        elif choice == '4':
            delete_record()
        elif choice == '5':
            break
        else:
            print('Not a valid selection, please try again')


def display_all_records():
    """The one part of this assignment that didn't make me want to rip my hair out trying to troubleshoot.
    It displays all the records in the database, and this simple block of code has yet to randomly fail me for
    seemingly no reason. This is more than I can say for everything else."""
    records = Record.select()

    for record in records:
        print(record)


def add_new_record():
    """This block of code adds entries to the database. It first checks that the user-inputted name is not already in
    the database, then adds it if it isn't. Names are automatically capitalized"""
    name = input('Enter name of record holder: ').strip().title()
    name_query = Record.select().where(Record.name == name)
    for record in name_query:
        # I used this for loop for validating if the name is already in the database or not.
        # It should always only go through the loop once, so I wanted to just make it an if else statement.
        # I tried using name_query[0] to do what [record] is currently doing, so that I wouldn't need the loop.
        # But that didn't work. I don't know why. So I kept the loop, even though it may be a little weird.
        if record is None:
            continue
        else:
            # this else statement is hit should a matching entry be found in the database.
            print(f'{name} already in database:')
            print(record)
            break  # This break ensures that the next else statement doesn't trigger if this one does.
    else:
        # This else block triggers if no matching records are found in the loop. I would've just had this block
        # be within the "if" statement, but for some reason that ensured the previous else statement
        # would never trigger, preventing me from displaying the "name already in database" message.
        county = input('Enter record holder\'s country: ')
        number_of_catches = int(input('Enter record holder\'s number of catches (as an integer): '))
        new_record = Record(name=name, country=county, number_of_catches=number_of_catches)
        new_record.save()


def edit_existing_record():
    """This code edits the number of juggles that someone has achieved. It's got most the same quarks as the above
    function, since it's largely a copy/paste of most the code."""
    name = input('Enter name of record holder: ').strip().title()
    name_query = Record.select().where(Record.name == name)
    for record in name_query:
        if record is None:
            continue
        else:
            record.number_of_catches = int(input('Enter record holder\'s number of catches (as an integer): '))
            record.save()
            break
    else:
        print(f'{name} not found in database')


def delete_record():
    """This function is also mostly a copy/paste of the last one. The only change is that it deletes the selected
    record, instead of modifying it."""
    name = input('Enter name of record holder: ').strip().title()
    name_query = Record.select().where(Record.name == name)
    for record in name_query:
        if record is None:
            continue
        else:
            rows_deleted = Record.delete().where(Record.name == name).execute()
            """I was about to turn this assignment in without the ability to delete, cause I couldn't get the code to
            work. Then I noticed that my .execute didn't have the () at the end of it. Added it, then it worked.
            I have wasted over half an hour trying to figure out why I couldn't delete anything. PAIN."""
            print('Rows deleted: ', rows_deleted)
            break
    else:
        print(f'{name} not found in database')


if __name__ == '__main__':
    main()
