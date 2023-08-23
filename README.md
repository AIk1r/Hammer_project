# Hammer_project
Simple referral system

register: This endpoint accepts a POST request with the user's phone number as a parameter. If a user with such a phone number already exists, it generates a new code, saves it in the cache and session, then redirects the user to the verification page. If such a user does not exist, it creates a new user, generates a code, and also redirects to the verification page. If the request method is not POST, it simply renders the registration page.

verify: This endpoint accepts a POST request with the user's phone number and the code that was sent to the user. If the entered code matches the generated code, it creates a session for the user and redirects them to the profile page. If the codes do not match, it returns an error message. If the request method is not POST, it simply renders the verification page.

profile: This endpoint accepts a POST request with an invite code. If an invite code is provided, it is saved for the current user. This endpoint also generates an invite code for the user if it does not yet exist, and checks if the user has been invited by another user. If the request method is not POST, it simply renders the profile page.
