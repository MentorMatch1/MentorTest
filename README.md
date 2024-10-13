# MentorTest

## The backend for the Science Mentorship Program Mentor / Mentee Matching

1. Pull All the Files from the Github
2. Build the Dockerfile (Must have docker installed on computer)
3. Run the Docker Container for the Api

## Notes:
- This requires the MentorTestGui to run
- Data is specifically and only formatted to the Science Mentorship Program at University of Alberta. While this part of the Project is open Source it is an Unused Version
- FINAL DRAFT of Main Application is PRIVATE to protect Program Information. The Information Here does not reflect the Science Mentorship Program.
- This Applicatoion can simply be seen as template of what a Mentor Mentee Matchign system might look like before it gets tailored to a specific program.

  

## Commands:

1. docker build -t mentor_test_api .
2. docker run -p 5001:5001 mentor_test_api
