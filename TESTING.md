# TESTING

I have conducted both manual and partly automated testing for Church of Iron application.

# Table of Content

-   [TESTING](#testing)
-   [Table of Content](#table-of-content)

    -   [Code Validation](#code-validation)
        -   [W3C HTML validation report](#w3c-html-validation-report)
        -   [W3C CSS validation report](#w3c-css-validation-report)
        -   [Python code validation](#python-code-validation)
    -   [Responsiveness Testing](#responsiveness-testing)
    -   [Lighthouse Testing](#lighthouse-testing)
    -   [Manual Testing](#manual-testing)

        -   [Home page](#home-page)
        -   [All gyms page](#all-gyms-page)
        -   [Individual Gym page](#individual-gym-page)
        -   [Memberships page](#memberships-page)
        -   [Profile page](#profile-page)
        -   [Cart page](#cart-page)

        -   [Bugs](#bugs)
        -   [Resolved Bugs](#resolved-bugs)

## Code Validation

### W3C HTML validation report

-   #### Home page

    ![W3C HTML]()

[Back to top](#testing)

-   #### Cart page

    ![Cart]()

-   #### Checkout page

    ![Checkout]()

[Back to top](#testing)

-   #### Profile page

    ![Profile]()

-   #### Sign in page

    ![Sign in]()

### W3C CSS validation report

![W3C CSS](docs\css-validator.png)

[Back to top](#testing)

### Python code validation

    ![Pep8online](docs\pep8.png)

## Responsiveness Testing

[Back to top](#testing)

## Lighthouse Testing

Church of Iron site has been tested on `Google Chrome Lighthouse` function on incognito window for the desktop and mobile screens.

-   #### Home - desktop

    ![Home]()

-   #### Home - mobile

    ![Home-mobile]()

[Back to top](#testing)

        -   [Home page](#home-page)
        -   [All gyms page](#all-gyms-page)
        -   [Individual Gym page](#individual-gym-page)
        -   [Memberships page](#memberships-page)
        -   [Profile page](#profile-page)
        -   [Cart page](#cart-page)

## Manual Testing

### Home Page, footer and navbar

#### Scenarios and results

|                                                                                     | Pass/Fail |
| ----------------------------------------------------------------------------------- | :-------: |
| Clicking the navbar logo homepage takes the user to the homepage                    |   Pass    |
| Clicking the gym, store and my profile links in the navbar opens a dropdown         |   Pass    |
| All links in the navbar lead to their intended locations                            |   Pass    |
| Navbar collapses in less than large screens and the hamburger button opens the menu |   Pass    |
| The cart counteer updates when items are added to the cart                          |   Pass    |
| Clicking Read more in the gym section take sthe user to the gym's page              |   Pass    |
| Clicking learn more in the membership section takes the user to the menbership page |   Pass    |
| Subscribing to the newsletter registers the email in Mailchimp                      |   Pass    |
| The links in the footer takes the user to their intended locations                  |   Pass    |

### All gyms page

#### Scenarios and results

|                                                                                 | Pass/Fail |
| ------------------------------------------------------------------------------- | :-------: |
| The different gyms on the page generates acuratlly from the gym model instances |   Pass    |
| Clicking the To Gym button goes to the individual gyms page                     |   Pass    |

### Individual Gym page

#### Scenarios and results

|                                                                     | Pass/Fail |
| ------------------------------------------------------------------- | :-------: |
| Carosel on the top of the page switches images                      |   Pass    |
| Amenities show as intended                                          |   Pass    |
| The map loads and displays when the user clicks the show map button |   Pass    |
| All model data loads and displays correctly                         |   Pass    |

### Memberships Page

#### Scenarios and results

|                                                                                                                                                                                 | Pass/Fail |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------: |
| Clicking show more on the memberships drops down with more information about the membership                                                                                     |   Pass    |
| Clicking Signup now takes the user to the membership signup page with prefilled information if any exist                                                                        |   Pass    |
| On less than large screens the membership tables displays as dropdown buttons                                                                                                   |   Pass    |
| The buttons opens the dropdown and displpay it's information                                                                                                                    |   Pass    |
| On the signup page if the user is not logged in, the user will fill out a form to sign up to for an account at the same time as they are filling out the membership information |   Pass    |
| On the signup page if the user is not logged in but have an account the can log in and sign up for a membership in the same form                                                |   Pass    |
| If the user tries to sign up an existing user without the correct password it fails                                                                                             |   Pass    |
| On the signup page the checkout button takes the user to the chekout page                                                                                                       |   Pass    |

### Checkout app

#### Scenarios and results

|                                                                                  | Pass/Fail |
| -------------------------------------------------------------------------------- | :-------: |
| The page shows all information about each item in the cart                       |   Pass    |
| The page displays the membership that the user has selected to sign up for       |   Pass    |
| Clicking the complete order button takes the user to the stripe payment page     |   Pass    |
| When the payment has gone through the user is taken to the checkout success page |   Pass    |
| All information abouit the order/membership is dispayed                          |   Pass    |

### Profile Page

#### Scenarios and results

|                                                                                                                                                    | Pass/Fail |
| -------------------------------------------------------------------------------------------------------------------------------------------------- | :-------: |
| All the user details are displayed                                                                                                                 |   Pass    |
| The details can be changed by clicking the change details, that changes the fields from editable to editable, clicking save, saves the information |   Pass    |
| If the user has a membership, all its information is displayed                                                                                     |   Pass    |
| If the user has made orders before their order history is displayed                                                                                |   Pass    |

### Cart Page

#### Scenarios and results

|                                                                                                                                | Pass/Fail |
| ------------------------------------------------------------------------------------------------------------------------------ | :-------: |
| All cart items are displayed individually and correctly                                                                        |   Pass    |
| The cart total and subtotal are calculated correctly                                                                           |   Pass    |
| Changing the quantity of an item and clicking updated saves the new quantity to the cart                                       |   Pass    |
| Clicking the remove button deletes the item from the cart                                                                      |   Pass    |
| The user cannot add more than 99 or less than 1 to the cart                                                                    |   Pass    |
| If the cart total is less than the free delivery threshold, the user is notified of if the spend X more they get free delivery |   Pass    |

### Notifications

#### Scenarios and results

|                                                                                                                                                                 | Pass/Fail |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------: |
| Adding to the cart displays a notification in the top left                                                                                                      |   Pass    |
| Updating an item form the cart quantity displays a notification in the top left                                                                                 |   Pass    |
| Deleting an item from the cart displays a notification in the top left                                                                                          |   Pass    |
| Logging in/out and signing up displays a notification in the top left                                                                                           |   Pass    |
| Updating the user profile displays a notification in the top left                                                                                               |   Pass    |
| If the user tries to access the checkout page without a membership in sessions or a cart item they are redirected to the home page notification in the top left |   Pass    |
| Trying to sign up for a equal or lower membership than the user has redirects the user and displays a notification                                              |   Pass    |
| If the user tries to register an email that exists but not with the correct password                                                                            |   Pass    |
| If a non autherized user tries to delete a product form the site by entering the delete url they are notified and redirected                                    |   Pass    |
|                                                                                                                                                                 |   Pass    |
|                                                                                                                                                                 |   Pass    |

### Bugs

### Resolved Bugs
