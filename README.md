# vk_search_people
This code allows you to search for people using subscriptions to VKontakte communities. After entering the link to the community, the code saves the ID of all subscribers to the community and finds intersections when entering the next community. The code can be useful if you do not know the name of the person (or his nickname), or for targeted advertising.
1) Before starting work, you need to get an API developer token from the social network "VKontakte" 
2) insert the token into the VKTOKEN variable in the auth_data file
3) run vk_api_search_people.py file
4) write down the number of communities you are going to scan as an integer
5) enter the name of the community. For example:
      the link looks like "vk.com/public_name"
      must be entered into the program - public_name
