# The 147 Club
 
 
## About
<hr>
This is a website for a Snooker and Pool hall built using django. The aim of this site is for users to be able to create an account and be able to reserve a snooker or pool table for a given time in the future. The user also had CRUD functionality to manage their bookings and delete/edit if they are unable to make the booked time. 
 
## Features
<hr>

### Existing Features

#### Booking System
- Create Booking 
- View Booking
- Delete Booking
- Edit Booking

Users are able to create, read, update and delete their bookings. 

#### Collapsable Navbar
- The navbar is set to become collapsable when viewed on medium size screens and below. This is beneficial as when the viewport width is smaller the navbar may become squashed. Having the navbar dropdown like this improves the UI and is intuitive the user.

#### Auto Scrolling Images
- The home page contains an auto scrolling carousel. The carousel contains images of the three cue sports available at the club. This immediately shows the user what the club has to offer. It also offers a 'Book Now!' button making it easy for the user to quickly get to the booking form page. 

#### Overflow Boxes
- The testimonial section includes a scrolling overflow box. This means that the size of the testimonial section will still remain a consistent size despite the amount of testimonials it contains. 

#### User Input Validation
- No double bookings (same time, same table)
- No booking two tables at one time for a user. 
- Start time < End time
- Start time can only be between 11am and 10pm
- End time can only be between 12am and 11pm
- Date cannot be in the past

If any of the above conditions are met. The user will be shown an error message corresponding to the given error. They will be asked to change the part that was causing and issue. For example, if there was a table already booked by another user 

#### Testimonials
- Users have the ability to submit testimonials. 
- The admin has the ability to toggle an approved boolean so they can manage what testimonials are shown on the page. This could be to prevent bad language or accidentally submitted testimonials from being shown to the user. 

#### Google Maps API
- The home page includes a Google Maps API to show the user the location of the club. This is useful to the user as they can see exactly where the club is and how to get there. It gives the user a more visual representation of the club's location. 

#### Cloudinary
- Cloudinary is used to store the images for the booking app. The Admin has a cloudinary field in the GameTable model where they can add an image to correspond with the the table they are uploading. This is easily updated or changed in the admin pannel

#### Close tables for maintenance
- The admin has the ability to give the tables in the GameTable model a status of 'Working' or 'Maintenance'. Doing this makes the table unable to be booked while the table has a status of 'Maintenance'. 


#### Past and Future bookings
- The 'My Bookings' page includes tabs for past and Future bookings. 
- The bookings are ordered by date. This makes it easy for a user to see the next booking they have and also keep track of their previous bookings.

 
### Future Features
- Implement email confirmation of a booking to the user
- Remind user of booking 1hr before time slot 
- Payment/deposit
- Suggest an alternative table if the user picks one that is unavailable
- Email verification
- login with social media / Google account 
- Store user's first name and last name in built in django app


## Data Model
<hr>

 
## Testing
<hr>

### Manual Testing 

### Automated Testing
 
### Bugs
#### Solved Bugs

#### Remaining Bugs
- No bugs remaining
### Validator Testing
- PEP8

- HTML Validator 

- CSS Validator
 
 
## Deployment
<hr>

Steps for deployment:

 
 
You can find the live link here: 
 
## Credits
<hr>
