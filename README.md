# Photo Studio

To launch, install Docker and run the following command:

	docker-compose up

If you need to remove any and all containers that were created, run clean.sh.

# To Do List

## Website
 
 * Add email field **[ DONE ]**
 * Add terms and conditions checkbox
 * Add first/last name field **[ DONE ]**
 * Set number of pictures to take field **[ DONE ]**
 * Show photos when done **[ DONE ]**
 * Create button that will take a picture on camera **[ DONE ]**

## Countdown-Website

 * Create a countdown website skeleton **[ DONE ]**
 * Create a countdown timer **[ DONE ]**

## Camera-Controller

 * Bring up redis service **[ DONE ]**
 * Place photo in directory with email address **[ DONE ]**
 * Add int to photo name so they're not replaced **[ DONE ]**
 * Determine if camera is present
 * Copy photo to mounted volume **[ DONE ]**
 * Copy photo right to dest, no /tmp dir **[ DONE ]**

## Photo-Mod

 * Bring up redis service **[ DONE ]**
 * Port logo placement algorithm **[ DONE ]**
 * Git ignore logo name **[ DONE ]**

## Email

 * Port email code **[ DONE ]**
 * Add HTML to email **[ DONE ]**
 * Include multiple attachments in case multiple photos were taken

## All Categories

 * Find a way to send requests/results between containers **[ DONE ]**
 * Get project to work with docker-compose on a raspberry pi **[ DONE ]**
