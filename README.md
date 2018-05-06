# Photo Studio

To launch, install Docker and run the following command:

	docker-compose up

If you need to remove any and all containers that were created, run clean.sh.

# To Do List

## Website
 
 * Add email field
 * Add allow multiple email addresses
 * Add terms and conditions checkbox
 * Add first/last name field
 * Set number of pictures to take field
 * Show photos when done
 * Create button that will take a picture on camera **[ DONE ]**

## Countdown-Website

 * Consider creating a countdown timer

## Camera-Controller

 * Bring up redis service **[ DONE ]**
 * Place photo in directory with email address
 * Add int to photo name so they're not replaced
 * Determine if camera is present
 * Copy photo to mounted volume **[ DONE ]**
 * Copy photo right to dest, no /tmp dir

## Photo-Mod

 * Bring up redis service **[ DONE ]**
 * Port logo placement algorithm
 * Git ignore logo name

## Email

 * Port email code
 * Add HTML to email
 * Include multiple attachments in case multiple photos were taken

## All Categories

 * Find a way to send requests/results between containers **[ DONE ]**
 * Get project to work with docker-compose on a raspberry pi **[ DONE ]**
