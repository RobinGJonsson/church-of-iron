##Media

-   Hero image: https://unsplash.com/photos/COxd0Jbe7u8
-   Protein shake image: https://unsplash.com/photos/_PI1S9dHf1g
-   Gym1 images: https://nordicwellness.se/vara-klubbar/kavlinge/kavlinge-kvarngatan/
-   Gym2 images: https://nordicwellness.se/vara-klubbar/malmo/malmo-svagertorp/
-   Delivery package image: https://unsplash.com/photos/YiSD-1eJ_1g
-   Yoga image: https://unsplash.com/photos/Eszi6jZ0Pfk
-   Map image: https://unsplash.com/photos/5F4oYUg-WvM
-   Store top image: https://unsplash.com/photos/mTorQ9gFfOg

##Tools

-   TinyPNG
-   ColorSpace
-   Google Maps API
-   iloveimg: for resizing images

##Bugs

-   Closing the toats was not working, by removing the JS in the postloadjs on base.html and adding a show class to the toast element made it show and hide as expercted
-   Navbar on profile page acts as if the user is logged out: This was because in the profile view, the context contained a key called "user" which is a reseved keyword
-   When trying to upload an image from a form, it always failed to vaildate, the reason for this was first of all you need "enctype="multipart/form-data" in the form and secondly you need "request.POST" AND "request.FILES" in the when saving the form data in the view
