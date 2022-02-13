import streamlit as st
from streamlit_option_menu import option_menu
from Scrape import *
if __name__ == '__main__':
    
   
    
    st.set_page_config(page_title="City And License Plate Code",initial_sidebar_state='auto',page_icon='chart_with_upwards_trend',layout='wide')
    page = option_menu(None, ["Home", 'Get Data',"Search","About Me"],icons=['house','app' ,'search','person'],menu_icon="cast", default_index=0, orientation="horizontal")
    
    if page == "Home":
        col1, col2 ,col3 = st.columns(3)
        with col2:
            st.markdown("## WELCOME  :wave:")
            st.markdown("Hello, it's **City And License Plate Code**. I want to talk about my project.")
            st.markdown("* The data is scraped ' **https://www.ilimiz.net/il-plaka-kodlari.html** ' ")
            st.markdown("* License Plate code and city names of all cities in Turkey are obtained from our website.And csv file is downloadable.")
            st.markdown("* In the 'Search' section, we can search both by city name and license plate code.")
            st.markdown("* That is all. Enjoy :smile:")
    
    elif page == 'Get Data':
        col1, col2, col3,col4,col5,col6 = st.columns(6)
        with col2:
            if st.button('Start'):
                with st.spinner('Wait for it...'):
                    response_web = get_requests()
                    data = get_data(response_web)
                    pure_df = data_preprocessing(data)        
                    csv = convert_df_to_csv(pure_df)
                    df_to_db(pure_df)
                    with col3:
                        st.dataframe(pure_df)    
                    with col4:
                        st.download_button(
                            label="Download",
                            data=csv,
                            file_name='License Plate Code CSV',
                            mime='text/csv',
                        )
                    
        
    elif page == 'Search':
        col1 ,col2 = st.columns(2)
        with col1 :
            with st.form("my_form"):
                city = st.text_input('Enter City Name :')
                submitted = st.form_submit_button("Submit")
                if submitted:
                    with st.spinner('Wait for it...'):
                        con = sqlite3.connect('my_database.db') # We Connect to Database
                        cr = con.cursor() 
                        cr.execute("SELECT plate_code FROM CityPlateCode WHERE city_name like '" +str(city)+"'") 
                        dataresults = cr.fetchone() 
                        if dataresults is None:
                            st.error('Please check the entered city name !!')
                        else:
                            st.success(dataresults[0])
        
        with col2:    
            with st.form("my_form2"):
                plate = st.text_input('Enter License Plate Code :')
                submitted = st.form_submit_button("Submit")
                if submitted:
                    with st.spinner('Wait for it...'):
                        if int(plate)<82 and int(plate)>0:    
                            vt = sqlite3.connect('my_database.db') # We Connect to Database
                            cur = vt.cursor()
                            cur.execute('''SELECT city_name FROM CityPlateCode where plate_code=?''', (plate,))
                            results = cur.fetchall()               
                            st.success(results[0][0])
                        else :
                            st.error(plate+' Plate Codes Are Not Available! Please Enter A Valid License Plate Code')        
                              
    elif page == 'About Me':
        col1, col2 ,col3 = st.columns(3)
        with col2:
            st.markdown("## Hello, I'm Berkay :bar_chart:")
            st.markdown("#### I'm 21 years old. I am a 3rd year Computer Engineering student.  I work to improve myself in the fields of data scraping, data analysis, data visualization, machine learning, object detection.")
            st.markdown("## 🔗 Contact Me and Feedback")
            st.markdown("[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/berkay-c)")
            st.markdown("[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/berkay-c/)")
            st.markdown("[![Gmail](https://img.shields.io/badge/gmail-%23D14836.svg?&style=for-the-badge&logo=gmail&logoColor=white)](mailto:berkayyasinciftci@gmail.com?subject=Hola%20Jiji)")