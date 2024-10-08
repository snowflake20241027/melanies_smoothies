# Import python packages
import pandas as pd
import requests
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")

name_on_order = st.text_input("Name on Smoothie:")
st.write(f"The name on your Smoothie will be: {name_on_order}")

st.write(
    "Choose the fruits you want "
    "in your custom Smoothie!"
)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = (
    session
    .table("smoothies.public.fruit_options")
    .select(col('FRUIT_NAME'), col('SEARCH_ON'))
)
# st.dataframe(
#     my_dataframe,
#     use_container_width=True
# )
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df.drop(columns=['SEARCH_ON']), use_container_width=True)


ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string = ''
    for i in ingredients_list:
        ingredients_string += f"{i} "
    # st.text(ingredients_string)

    my_insert_stmt = (
        "insert into smoothies.public.orders"
        "(ingredients, name_on_order) "
        f"values ('{ingredients_string}','{name_on_order}')"
    )
    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

    for fruit_chosen in ingredients_list:
        fruit_search_on = pd_df[pd_df.FRUIT_NAME == fruit_chosen].SEARCH_ON.unique()[0]
        st.write(f"The sarch value for {fruit_chosen} is {fruit_search_on}.")
        st.subheader(f"{fruit_search_on} Nutrion Information")
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_search_on}")
        fv_df =  st.dataframe(data=fruityvice_response.json(), use_container_width=True)








