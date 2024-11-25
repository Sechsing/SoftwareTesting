System to test for Assignment 2 of FIT2107 at Monash University.

# System Under Test

_Anything Anytime Library_ (AAL) is a community library.
It offers access to books, magazines, newspapers, and public PCs connected to the internet.
It also has a collection of gardening and carpentry tools, and an on-site community makerspace.
Any registered member of the community can use the library as a place to work or study, to borrow books or tools, or to use the makerspace facilities.

AAL runs all of its operations with a single piece of software, _Borrowing Administration Terminal_ (BAT).
Unfortunately, BAT was made for more traditional libraries, so AAL have had to commission custom extensions.
With limited funding for public libraries, AAL were unable to afford particularly skilled developers, nor were they able to extend the contract to include testing.
So, their custom version of BAT has quite a few bugs.

The core functionality of AAL's modified BAT includes:
* Managing user registration to the library.
* Recording details about borrowed items (e.g., who borrowed it, when, when it should be returned).
* Notifying staff if an item is overdue.
* Upon return of the item, calculating a late fee.
* Prompting for payment of any late fees a patron has when they next attempt to borrow an item or use the library facilities.
* Processing payment of fees.
* Validating that patrons attempting to borrow gardening or carpentry tools are allowed to do so (i.e., have completed the required training, are of an appropriate age, and have no outstanding late fees).
* Validating that patrons attempting to access or book the makerspace facilities are allowed to do so (i.e., have completed the required training, are of an appropriate age, and have no outstanding late fees).

AAL also have a series of custom rules in BAT that have been developed and integrated haphazardly over the years.
These rules are:

* A patron can not borrow any item if they have fees to pay (after considering any discounts they are eligible for).
* Any patron over the age of 90 can not use the makerspace or borrow carpentry tools.
* Any patron under the age of 18 can not use the makerspace or borrow carpentry tools.
* Patrons of any age can not use the makerspace, or borrow gardening/carpentry tools if they have not completed the associated training.
* Any person over the age of 50 but under the age of 65 gets a 10% discount on their fees, rounded to the nearest cent.
* Any person aged 65 and over gets a 15% discount on their fees, rounded to the nearest cent.
* Patrons aged 90 and above do not have to pay fees.
* Fees can not be negative.
* Ivan Smith is banned from using the makerspace.
* Sandra Atkinson can borrow gardening and carpentry tools without completing the training.
* Brian Lancer does not receive any discounts on fees.

# Usage Notes

This is a redacted version of BAT's code.
Each part of the code has been documented to describe its purpose and intended logic.
In addition to this, you should note:

* It is assumed that a patron will never attempt to take out a loan for an item they are already borrowing (e.g., borrow two copies of the same book).
* It is assumed that there are no patrons with the same name and age.
* It is assumed that there are no logic errors in the JSON data provided to BAT (e.g., duplicate IDs, loans which aren't reflected in the catalogue). If there are any syntax errors in the data then BAT will not open.
* Changes to data are not saved until the "Quit" menu option is selected.
* All functionality to do with late fees has been removed, except the calculation of discounts for the purpose of determining if a patron is allowed to borrow an item or is not allowed due to fees owed.
* Ability to update training records has been removed.
* All analytics code (e.g., for generating overdue loans reports) has been removed.
* All user and catalogue data is fabricated.