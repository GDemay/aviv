# Projet - Carte des prix à Paris

This is the list of functionnalities that I have implemented in this project:

- Adding pre-commit
- Adding black
- Adding isort
- Logger configuration
- Database class
- Designing the architecture
- The price of Paris arrondissement are displayed in the chart when the user clicks on the arrondissement

# API Architecture 

I decided to split the project in multiple packages:

- **core**: contains the core logic of the project
   - **config**: contains the configuration of the project
   - **logger**: contains the logger of the project
   - **parsing_listing**: contains the class that parses the listing from response

- **blueprints**: contains the endpoints of the project
  - **api**: contains the endpoints of the api
  - **listings**: contains the endpoints of the listings
  - **listing_history**: contains the endpoints of the listings_history

  - **crud**: contains the logic of the crud endpoints
    - **listing_history_crud**: contains the logic of the listing_history crud endpoints (create, read, update, delete)
    - **listings_crud**: contains the logic of the listings crud endpoints (create, read, update, delete)

  - **database** contains the database logic
    - **session**: contains the initialization of the database

  - **schema**: contains the schema of the database with Pydantic models
    - **listing_history_schema**: contains the schema of the listing_history table
    - **listings_schema**: contains the schema of the listings table

 ## Endpoints 

# Listings:
- GET - **/listing/{listing_id}**: returns the listing with the id
- GET - **/listing**: returns the listings
- PUT - **/listing/{listing_id}**: updates the listing with the id
- DELETE - **/listing/{listing_id}**: deletes the listing with the id
- DELETE - **/api/drop**: delete the table (for testing purposes, it should be used only in development)
- GET - **/listing/average/{place_id}**: returns the average price of the listing with the id

# Listing History:
- GET - **/listing_history/{history_id}**: returns the listing_history with the id
- POST - **/listing_history**: creates a new listing_history

# Api

- GET - **/geoms**: Get geoms and some geometry information
- GET - **/get_price/{cog}**: Return the volumes distribution for the given cog in storage format

## Database

In order to track the history price of a listing, I created a table listing with the following fields:
 
- listing_id: id of listing
- place_id : arrondissement of paris with an id (geom)
- price: price of the listing
- area: area of the listing
- room_count: number of rooms in the listing
- creation_date : date of creation of the listing
- deleted_at: date of deletion of the listing

In order to track the history of the listings, I created a table listing_history with the following fields:

- id: (primary key) id of the listing_history
- listing_id: (foreign key listings(listing_id)) id of the listing
- price: price of the listing
- date: area of the listing

Adding a listing adds automaticaly a row in history_listing
Updating a price of a listing adds a row in history_listing if the price is different from the previous one

# Improving the parsing

I noticed that some data were not parsed correctly. For example we have this one :
```
  {
    "title": "Appartement",
    "price": "Prix non communiqu\u00e9",
    "place": "Paris 16\u00e8me arrondissement",
    "listing_id": "1969971901"
  },
```
The previous parsing was not able to parse everything correctly.
If no price / area / room_count is found, values are set to None in the database.

I move the parsing from update_data to a a class named core/parsing_listing

Every parsing elements are separated in functions (get_room_count, get_price, get_area, get_place_id)


# Industrialisation of the code

## Requirements:

### Functional Requirements

- Sellers should be able to add, delete and modify apartments they want to sell
- The website should include a catalog of apartments 
- Buyers can search apartments by name, keyword or category. 
- Buyers can contact the buyer
- Non functional Requirements
- High availability
- High consistency
- Low latency
- Scale: 10 millions users


## Scale:

10 million d’annonces seloger.com
Around 2 pictures per annonce
5 MB per photo

10^7 * 4 * 5 MB
20^8 = 100 000 000 MB = 100 TB = 1.2 PB 



## Data Types:
Relation database (mysql / psql)

### User

- id Primary key serial | int
- name | string
- email | string
- phone_number | string
- type_acount #seller or buyer | string



Apartment

- id Primary key,serial |  int
- user_id Foreign key referencing user.id | int
- title | string
- description | string
- price | int
- size | int
- publish_date datestamp path_images string

# Architecture schema:

https://drive.google.com/file/d/1RTytqQSBxUYWrLC0W8U2x7qpz26vkuWx/view?usp=sharing