GENERAL IMPLEMENTATION DETAILS

1)The first step I took was to change my previous HWs mistakes.
2)To implement the requirements for this HW I have made 3 .js files. One for globalpage, profilepage, followerpage
3)The Globalpage needes to be updated every 5 seconds with any new post. My exact implementation has been further explained in globalpage.js
4)The globalpage.js also conists of a section that handles adding new comments with out refreshing the entier page. This has been implemented using
  the .on() method with event delegation.
5) both the profile.js and follower.js consists of javascript code only for adding new comments. The implementation is exactly similar to globalpage.js
6) I have also taken care that my application only sends and loads only new post since the last update. I have implemented this by filtering with id_gt at the server side
7) There are no hard coded parts to any django-generated components. But static components have absolute paths(This is allowed in the HW instruction)

I am commiting this code with 3 users in the data base. 

1)Username: parth, Password: 1, email: 1@gmail.com
2)Username: mona, Password: 1, email: 1@gmail.com
3)Username: vini, Password: 1, email: 1@gmail.com


References
1)https://docs.djangoproject.com/en/1.10/
2)https://learn.jquery.com/events/event-delegation/
3)http://www.w3schools.com/js/
4)http://api.jquery.com/on/
5)http://www.w3schools.com/jquery/
6)In class videos

