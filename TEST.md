<br>
<div>
    <img src="static/assets/img/readme/readme_img.png" alt="Inscribe Logo">
</div>

<br>

# Testing

Throughout the project, I chose to manually test my work so I had a firm understanding of my mistakes, and how the features I chose to implement
were going to be accessed by other users, across various device-types. This was challenging in itself, whilst trying to come to grips with certain
elements that I had experienced difficulty with, however am happy with the end result.

---
## TEST Document Navigation
* [Pages and Features](#pages-and-features)
  * [Home Page](#home-page)
  * [Registration](#registration)
  * [Sign In and Sign Out](#sign-in-and-sign-out)
  * [Profile](#profile)
  * [New Entry](#new_entry)
  * [Edit Entry](#edit-entry)
  * [More Info](#more-info)
  * [Community Suggestion](#community-suggestion)
  * [Other Community Suggestion](#other-community-suggestion)
  * [Admin Rights](#admin-rights)
* [Responsive Design](#responsive-design)


---
## Pages and Features

### Home Page
When entering the site for the first time, there is little information, other than the animated hero text, regarding the sites purpose.
This encourages the user to navigate to the relevant links, 'About' or 'Registration'. On recognition by the browser, that there is still
a current ```session user```, the 'Home' page will display a different set of navigation links whilst on a desktop viewport.

### Registration
In order for a new user to register a new account with (in)Scribe, there are three input fields which are required to be completed:
* A 'Username', taking the ```html pattern attribute``` into consideration, has to contain a minimum of five characters, however less than
  twelve, and can also contain a number.
* The 'Your Password' input field shares the ```pattern```.
* The 'Confirm Your Password' field must match when compared with the previous password input field.

<div>
    <img src="static/assets/img/test/acc_creation.gif" alt="Account Creation gif">
</div>

### Sign In and Sign Out


### Profile
### New Entry
<div>
    <img src="static/assets/img/test/entry_creation.gif" alt="Entry Creation gif">
</div>

### Edit Entry
<div>
    <img src="static/assets/img/test/entry_edit.gif" alt="Edit Entry gif">
</div>

### More Info
<div>
    <img src="static/assets/img/test/entry_more_info.gif" alt="More Info gif">
</div>

### Delete Entry
<div>
    <img src="static/assets/img/test/entry_delete.gif" alt="Entry Delete gif">
</div>

### Search
<div>
    <img src="static/assets/img/test/entry_search.gif" alt="Entry Search gif">
</div>

### Community Suggestion
<div>
    <img src="static/assets/img/test/sugg_create.gif" alt="Suggestion Creation gif">
</div>

### Other Community Suggestion
<div>
    <img src="static/assets/img/test/other_sugg_create.gif" alt="Other Suggestion gif">
</div>

### Admin Rights
<div>
    <img src="static/assets/img/test/admin_rights.gif" alt="Admin Rights gif">
</div>

### Error Handling
<div>
    <img src="static/assets/img/test/abort_error.gif" alt="Abort Error gif">
</div>

---

## Responsive Design

As this platform was built upon the concept that a user be able to access their account, providing they had an internet connection, it was vital
that it be available across multiple screen sizes, i.e. Mobile, Tablet and Desktop. 

Using various browser Developer Tools; Chrome, Safari and Opera and testing different viewport windows, such as:
  * Google Pixel
  * Huawei Mate 20X
  * Samsung Galaxy Z
  * iPhone Models 5, 6, and 11
  * iPad Pro
  * MacBook Pro

 
No errors presented themselves at time of testing using the above browsers.

Using [Amiresponsive](http://ami.responsivedesign.is/?url=https%3A%2F%2Finscribe-wm.herokuapp.com%2F) the responsiveness across various viewports
can be seen below.

<div>
    <img src="static/assets/img/readme/amiresp.png" alt="Am I Responsive">
</div>
