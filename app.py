import  streamlit as st
from serpapi import GoogleSearch
import pandas as pd
import matplotlib.pyplot as plt

def compare(med_name):
    params = {
        'engine': "google_shopping",
        'q': med_name,
        'hl': "en",
        'gl': "in",
        'api_key': "319fad98190b305adf242ba826d3baa9f7c9f3a154c54b3969dbfe3c410f6c58"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    shopping_results = results['shopping_results']

    return shopping_results


col1 , col2 = st.columns(2)
col1.image('e_pharmacy.png',width = 200)
col2.header("E-pharmacy price comparision system")

st.sidebar.title("Enter the name of medicine: ")
med_name = st.sidebar.text_input("Enter Name here 👇: ")
number = st.sidebar.text_input("Enter number of options  here 👇: ")
product_comp=[]
product_price =[]
if med_name is not None :

    if st.sidebar.button("price compare"):
        shopping_results = compare(med_name)

        first_price = shopping_results[0].get('price')

        clean_price = first_price.replace('₹', '').replace(',', '').strip()
        lowest_price = float(clean_price)
        print(lowest_price)
        lowest_price_index = 0

        st.sidebar.image(shopping_results[0].get('thumbnail'))
        for i in range(int(number)):

            price_str = shopping_results[i].get('price')

            try:
                price_clean = price_str.replace('₹', '').replace(',', '').strip()
                current_price = float(price_clean)
            except:
                current_price = None  # or 0

            product_comp.append(shopping_results[i].get('source'))

            if current_price is not None:
                product_price.append(current_price)
            else:
                product_price.append(0)

            st.title(f"option{i+1}")

            col1,col2=st.columns(2)

            col1.write('Company')
            col2.write(shopping_results[i].get('source'))

            col1.write('Title')
            col2.write(shopping_results[i].get('title'))

            col1.write('Price')
            col2.write(shopping_results[i].get('price'))

            url=shopping_results[i].get('product_id')
            col1.write('Buy Link')
            col2.write("[Link](%s)"%url)
            """--------------------------------------------------------"""
            if (current_price < lowest_price):
                lowest_price = current_price
                lowest_price_index = i

        # For finding best option
        st.title("Best option")

        col1, col2 = st.columns(2)

        col1.write('Company')
        col2.write(shopping_results[lowest_price_index].get('source'))

        col1.write('Title')
        col2.write(shopping_results[lowest_price_index].get('title'))

        col1.write('Price')
        col2.write(shopping_results[lowest_price_index].get('price'))

        url = shopping_results[lowest_price_index].get('product_id')
        col1.write('Buy Link')
        col2.write("[Link](%s)" % url)


        """____________________________________________________________________________"""
        # Graph comparision
        df = pd.DataFrame(product_price,product_comp,)
        st.title("Chart Comparision")
        st.bar_chart(df)

        fig,ax = plt.subplots()
        ax.pie(product_price,labels=product_comp,shadow=True)
        (ax.set_aspect("equal"))
        st.pyplot(fig)