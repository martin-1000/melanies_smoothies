# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Example Smoothie App :cup_with_straw:")
st.write(
    """Make custom smoothie here:
    """
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your smoothie will be', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 items:',
    my_dataframe,
    max_selections=5
    )

if ingredients_list:

    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
    #st.write(ingredients_list) 
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" +name_on_order+"""')"""
    
    #st.write(my_insert_stmt)
    #st.success('Thanks for your order'+name_on_order, icon="✅")
    #st.stop()
    
    time_to_insert = st.button('Submit')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        #st.write(my_insert_stmt)
        st.success('Thanks for your order '+name_on_order, icon="✅")

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())
