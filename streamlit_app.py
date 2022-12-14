import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner');

streamlit.header('Breakfast Favorites')
streamlit.text('ð¥£ Omega 3 & Blueberry Oatmeal')
streamlit.text('ð¥ Kale, Sprinach & Rocket Smoothie')
streamlit.text('ð Hard-Boiled Free-Range Egg')
streamlit.text('ð¥ðAvocado Toast')

streamlit.header('ðð¥­ Build Your Own Fruit Smoothie ð¥ð')

# import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# New section to display fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

# import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
## streamlit.text(fruityvice_response.json()) --commented out by me
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# write your own comment -what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)

# streamlit.stop()
# import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load contains:")
streamlit.dataframe(my_data_rows)

fruit_to_add = streamlit.text_input('What fruit would you like to add?')
sql_text = "INSERT INTO FRUIT_LOAD_LIST VALUES ('" + fruit_to_add + "')"
streamlit.write(sql_text)

my_cur.execute(sql_text)  
streamlit.write('Added: ',fruit_to_add)  
