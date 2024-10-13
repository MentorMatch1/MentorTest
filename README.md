# MentorTest

The purpose of this application is to take Mentors and Mentees inside of a CSV File and use Matching parameters to help return a score of all the possible matches between all of the mentors and the mentees. An algorithm helps find the best matches for each of the mentees to their best mentor and returns that file back to the uploader to be saved as a seperate CSV.

## Instructions for Running Applicaiton.

1. Pull All the Files from the Github
2. Build the Dockerfile (Must have docker installed on computer)
3. Run the Docker Container for the Api

## Notes:
- This requires the MentorTestGui to run successfully. Requires Specifically formatted column CSV Files to use correctly as well.
- This is for viewing purpose simply. Showing a demo of the MentorMatching application that was later majorly updated before distributing to the Science Mentorship Program
- Data is specifically and only formatted to the Science Mentorship Program at University of Alberta. While this part of the Project is open Source it is an Unused Version
- FINAL DRAFT of Main Application is PRIVATE to protect Program Information. The Information Here does not reflect the Science Mentorship Program.
- This Applicatoion can simply be seen as template of what a Mentor Mentee Matchign system might look like before it gets tailored to a specific program.

  

## Commands:

1. docker build -t mentor_test_api .
2. docker run -p 5001:5001 mentor_test_api
