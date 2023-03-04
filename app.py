import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date , ForeignKey
from sqlalchemy.ext.declarative import declarative_base

def main():
    st.set_page_config(page_title="app", layout="wide")

    engine = create_engine('sqlite:///grocery_store.db')

    Session = sessionmaker(bind=engine)
    session = Session()

    Base= declarative_base()

    class Product(Base):
        __tablename__ = 'product'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        quantity = Column(Integer)

    class Order(Base):
        __tablename__ = 'order'
        id = Column(Integer, primary_key=True)
        name = Column(String, ForeignKey('product.name'))
        quantity = Column(Integer)
        date = Column(Date)
        place = Column(String)

    Base.metadata.create_all(engine)

    st.title('Meridian Express')

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Products", "Orders"))

    if page == "Products":
        st.title('Add a new product')

        name = st.text_input('Product name:')
        quantity = st.number_input('Product quantity:', value=1, min_value=1, key="uniku2")

        if st.button('Add product'):
            product = session.query(Product).filter_by(name=name).first()
            if product is not None:
                st.error(f'Product {name} already exists in the database.')
            else:
                product = Product(name=name, quantity=quantity)
                session.add(product)
                session.commit()
                st.success(f'Product {name} added to the database with quantity {quantity}.')

        st.title('Read products')

        if st.button('Read Products'):
            products = session.query(Product).all()

            for product in products:
                st.write(f"Name: {product.name}, Quantity: {product.quantity}")

        st.title('Update product quantity')

        products = session.query(Product).all()
        product_names = [product.name for product in products]
        selected_product = st.selectbox('Select a product:', product_names, key="unique_key_one")


        product = session.query(Product).filter_by(name=selected_product).first()
        if product is None:
            quantity = 1
        else:
            quantity = product.quantity
        quantity = st.number_input('Product quantity:', value=quantity, min_value=1, key="uniku3")

        if st.button('Update product quantity'):
            if product is None:
                st.error(f'Product {selected_product} does not exist in the database.')
            else:
                product.quantity = quantity
                session.commit()
                st.success(f'Quantity of product {selected_product} updated to {quantity}.')

        st.title('Delete product')

        products = session.query(Product).all()
        product_names_d = [product.name for product in products]
        selected_product_d = st.selectbox('Select a product:', product_names_d, key="unique_key_two")


        if st.button('Delete product'):
            product = session.query(Product).filter_by(name=selected_product_d).first()
            session.delete(product)
            session.commit()
            st.success(f'Product {selected_product_d} deleted from the database.')
    elif page == "Orders":
        st.title('Orders') 

        orders = Order.__table__

        with st.form(key='insert_form'):
            name = st.text_input(label='Enter the name of the product')
            quantity = st.number_input(label='Enter the quantity', value=1, min_value=1, key="uniku1")
            date = st.date_input(label='Enter the date')
            place_options = ['Prishtine', 'Peje', 'Prizren']
            place = st.selectbox('Select a place:', place_options, key="unique_key_three")
            insert_button = st.form_submit_button(label='Insert')

        if insert_button and name and quantity and date and place:
            
            order = Order(name=name, quantity=quantity, date=date, place=place)
            session.add(order)
            session.commit()
            st.success(f'Successfully inserted {name}, {quantity}, {date}, {place} into Orders table.')

        if st.button('Show all Orders'):
            orders = session.query(Order).all()
            for order in orders:
                st.write(f"Name: {order.name}, Quantity: {order.quantity}, Date: {order.date}, Place: {order.place}")

        order = session.query(Order).all()
        order_name = [order.name for order in order]
        selected_order = st.selectbox('Select a order:', order_name, key="unique_key_oone")
        
        order = session.query(Order).filter_by(name=selected_order).first()
        if order is None:
            quantity = 1
        else:
            quantity = order.quantity
            quantity = st.number_input('Order quantity:', value=quantity, min_value=1, key="uniku5")

        if st.button('Update Order quantity'):
            if order is None:
                st.error(f'Order {selected_order} does not exist in the database.')
            else:
                order.quantity = quantity
                session.commit()
                st.success(f'Quantity of orders {selected_order} updated to {quantity}.')

        orders = session.query(Order).all()
        order_names_d = [order.name for order in orders]
        selected_order_d = st.selectbox('Select a order:', order_names_d, key="unique_key_twwo")


        if st.button('Delete Order'):
            order = session.query(Order).filter_by(name=selected_order_d).first()
            session.delete(order)
            session.commit()
            st.success(f'Order {selected_order_d} deleted from the database.')
        

if __name__ == "__main__":
    main()