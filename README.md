In this guide, we're using Django Rest Framework (DRF) to create a simple Notes sharing app with an authentication system and elasticsearch to search through notes.

The API implements the following endpoints:

AUTHENTICATION ENDPOINTS
POST /api/auth/signup: create a new user account.
POST /api/auth/login: log in to an existing user account and receive an access token.

NOTES ENDPOINTS
GET /api/notes: get a list of all notes for the authenticated user.
POST /api/notes: create a new note for the authenticated user.
GET /api/notes/:id: get a note by ID for the authenticated user.
PUT /api/notes/:id: update an existing note by ID for the authenticated user.
DELETE /api/notes/:id: delete a note by ID for the authenticated user.
POST /api/notes/:id/share: share a note with another user for the authenticated user.

SEARCH ENDPOINT
GET /api/search?q=:query: search for notes based on keywords for the authenticated user.

WHY DJANGO?
    - Rapid Development
    - Django REST Framework (DRF)
    - Scalability
    - Security

