# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  "Choose the fruits you want in your custom smoothie! " 
)

name_on_order=st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

cnx=st.connection("snowflake")
session=cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list=st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
)

if len(ingredients_list) > 5:
    st.warning("You can only choose up to 5 ingredients. Remove an option first.")


if ingredients_list and name_on_order and len(ingredients_list) <= 5:
    ingredients_string = ', '.join(ingredients_list)

    submit = st.button('Submit Order')
    if submit:
        insert_stmt = f"""
            INSERT INTO smoothies.public.orders (name_on_order, ingredients)
            VALUES ('{name_on_order}', '{ingredients_string}')
        """
        session.sql(insert_stmt).collect()
        st.success(f"Your smoothie is ordered, {name_on_order}!")
