##############
About project
##############

I enjoyed coding this project very much, especially geo-spatial querys. Although I was running out of time
becouse of them :)
Never the less I willl try to explane here what and how it was done.

There is rest api as well as the web_app for testing. Web app is pure django / html but
it communicate wiht API.


Worklist...
===================

* You can use any oAuth grant type. Password grant is allowed as well. DONE
* There must be a default view for non-logged in users. This would show a list of entities that are public or say, for guest users DONE
* A user in the system would typically be the admin for an entity and on logging in, could edit that entity DONE
* You should enable geo-spatial queries (eg: give me all restaurants near Street Lietzenburger strasse). DONE
* Implement a cache TODO: if there is better solution or @method_decorator(cache_page(60*60*2))
* Your solution must be dockerized WILL DO if there time
* You should implement a test-suite (both unit-tests and api-tests) DONE


Database
===================
In this project I am using POSTGRES database with PostGis extension