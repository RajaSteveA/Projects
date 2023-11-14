import streamlit as st
import mysql.connector as sql
import pandas as pd
import numpy as np
import re
import speech_recognition as sr
from pydub import AudioSegment

st.set_page_config(page_title="PULSE-PDS",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   )

# QUESTION LIST
question_list = [
    "1. I want to buy Sugar.",
    "2. I want to buy Wheat.",
    "3. I want to buy Oil.",
    "4. I want to buy Blackgram.",
    "5. I want to buy Rice.",
    "6. I want to buy Sugar and Wheat.",
    "7. I want to buy Sugar and Oil.",
    "8. I want to buy Sugar and Blackgram.",
    "9. I want to buy Sugar and Rice.",
    "10. I want to buy Wheat and Oil.",
    "11. I want to buy Wheat and Blackgram.",
    "12. I want to buy Wheat and Rice.",
    "13. I want to buy Oil and Blackgram.",
    "14. I want to buy Oil and Rice.",
    "15. I want to buy Blackgram and Rice.",
    "16. I want to buy Sugar, Wheat, and Oil.",
    "17. I want to buy Sugar, Wheat, and Blackgram.",
    "18. I want to buy Sugar, Wheat, and Rice.",
    "19. I want to buy Sugar, Oil, and Blackgram.",
    "20. I want to buy Sugar, Oil, and Rice.",
    "21. I want to buy Sugar, Blackgram, and Rice.",
    "22. I want to buy Wheat, Oil, and Blackgram.",
    "23. I want to buy Wheat, Oil, and Rice.",
    "24. I want to buy Wheat, Blackgram, and Rice.",
    "25. I want to buy Oil, Blackgram, and Rice.",
    "26. I want to buy Sugar, Wheat, Oil, and Blackgram.",
    "27. I want to buy Sugar, Wheat, Oil, and Rice.",
    "28. I want to buy Sugar, Wheat, Blackgram, and Rice.",
    "29. I want to buy Sugar, Oil, Blackgram, and Rice.",
    "30. I want to buy Wheat, Oil, Blackgram, and Rice.",
    "31. I want to buy all the commodities."
]



def speech(random_number):
    speech_mapping = {
        0: "speech1.wav",
        1: "speech2.wav",
        2: "speech3.wav",
        3: "speech4.wav",
        4: "speech5.wav",
        5: "speech6.wav",
        6: "speech7.wav",
        7: "speech8.wav",
        8: "speech9.wav",
        9: "speech10.wav",
        10: "speech11.wav",
        11: "speech12.wav",
        12: "speech13.wav",
        13: "speech14.wav",
        14: "speech15.wav",
        15: "speech16.wav",
        16: "speech17.wav",
        17: "speech18.wav",
        18: "speech19.wav",
        19: "speech20.wav",
        20: "speech21.wav",
        21: "speech22.wav",
        22: "speech23.wav",
        23: "speech24.wav",
        24: "speech25.wav",
        25: "speech26.wav",
        26: "speech27.wav",
        27: "speech28.wav",
        28: "speech29.wav",
        29: "speech30.wav",
        30: "speech31.wav"
    }

    if random_number in speech_mapping:
        speech = speech_mapping[random_number]
    else:
        speech = "Error Occurred"  # Default if the random_number is not in the mapping

    return speech


    

# SETTING PAGE CONFIGURATIONS
st.header('PULSE-PDS', divider='rainbow')
st.subheader('Public Utility Logistics System Enhancement with Generative AI for Public Distribution System')
st.markdown("Empowering the fight against hunger with Generative AI: Our non-profit project takes aim at eradicating hunger by optimizing the public distribution system using generative artificial intelligence. We prioritize the welfare of those in need, working towards a world without hunger.", unsafe_allow_html=True)



#connecting to MySQL

mydb = sql.connect(host="localhost",
                   user="root",
                   password="root@123",
                   database= "beneficiary"
                  )
mycursor = mydb.cursor(buffered=True)



# TABLE CREATION
mycursor.execute(" CREATE TABLE IF NOT EXISTS biometric_data ( ID INT AUTO_INCREMENT PRIMARY KEY, black_gram INT, rice INT, oil INT, sugar INT, wheat INT)")


    



# SELECTING MENU
selected_menu = st.sidebar.radio("Select an option", ("Transaction","Report"))

################Creating Transaction##################
if selected_menu == "Transaction":
    st.markdown("# Creating Transaction")
    
    mycursor.execute("SELECT * FROM card_data")
    data = mycursor.fetchall()
    columns = ["ID", "card_holder_name", "card_type", "black_gram", "rice", "oil", "sugar", "wheat"]
    data_frame = pd.DataFrame(data, columns=columns)
    #st.write(data_frame)

############ Time Analysis

    st.subheader("TimeDelay")
    st.caption("Can you please provide information about today's ration shop entry delay!")
    
    Dtime=st.number_input("Enter the Delayed time in Minutes" , min_value=0 )
    st.write(f"Today's Delayed time in minutes: {Dtime}")
    if st.button("Save Delayed Time"):
          insert_query = "INSERT INTO time_delay (delayed_time_in_minutes) VALUES (%s)"
          Data = (Dtime,)  # Wrap Dtime in a single-item tuple
          mycursor.execute(insert_query, Data)
          mydb.commit()
          st.success("Time saved successfully!")
          
  

############Biometric Analysis
    
    st.subheader('Biometric Transaction')
    beneficiary=9
    col1, col2 = st.columns(2)
    with col1:
        id = st.number_input("Enter the ID of the Beneficiary ", min_value=1 , max_value=25)
        beneficiary=int(id)
        black_gram = st.number_input("Enter the black_gram quantity in Kg")
        rice = st.number_input("Enter the Rice quantity in Kg")
        
    with col2:
        oil = st.number_input("Enter the oil quantity in Kg")
        sugar = st.number_input("Enter the sugar quantity in Kg")
        wheat = st.number_input("Enter the wheat quantity in Kg")


    if st.button("Save Transaction"):
        #update_query = "INSERT Report_data SET ID=%s , card_holder_name=%s ,card_type=%s , black_gram=%s, rice=%s, oil=%s, sugar=%s, wheat=%s WHERE ID=%s"
        # Define the values to be updated.
     #   update_values = (id ,black_gram, Rice, oil, sugar, wheat, id)
        # Execute the update query with the values.
        insert_query = "INSERT INTO biometric_data (id, black_gram, rice, oil, sugar ,wheat) VALUES (%s, %s, %s, %s, %s , %s)"
        data = (id, black_gram, rice, oil, sugar,wheat)
        mycursor.execute(insert_query, data)
        # Commit the changes to the database.
        mydb.commit()
        # Display a success message.
        st.success("Transaction saved successfully!")
       



####### Speech to text Generation
    
    st.subheader('Speech to Text')
    
    questions = st.selectbox('Questions', question_list)
    
    question_index = question_list.index(questions)
    st.write(questions)
    if st.button("Play Audio"):
        st.write("Audio playing")
        q=speech(question_index)
        speech=q
        audio_file = open(speech, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/ogg')
        sample_rate = 44100  # 44100 samples per second
        seconds = 2  # Note duration of 2 seconds
        frequency_la = 440  # Our played note will be 440 Hz
    random_selection_expander = st.expander("Will I select a question randomly?")
    with random_selection_expander:
        if st.button("Random Selection"):
            random_number = np.random.randint(0, len(question_list))
            st.write(random_number + 1)
            question_index = random_number
            selected_question = question_list[question_index]
            st.write(selected_question)
    uploaded_audio = st.file_uploader("Upload an audio file", type=["wav", "mp3", "ogg"])

    if uploaded_audio is not None:
        # Initialize the recognizer
        r = sr.Recognizer()

        # Check the file format and convert to WAV if necessary
        if uploaded_audio.name.split('.')[-1] not in ["wav", "mp3", "ogg"]:
            st.error("Unsupported audio format. Please upload a WAV, MP3, or OGG file.")
            

        audio_data = sr.AudioFile(uploaded_audio)
        try:
            with audio_data as source:
                audio_text = r.record(source)

            text = r.recognize_google(audio_text)
            st.subheader("Converted Text:")
            st.write(text)
        except sr.UnknownValueError:
            st.error("Google Web Speech API could not understand the audio")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Web Speech API: {e}")

    # ... (previous code)
    if st.button("Create Transaction"):
        st.write(f"ID associated with this transaction: {beneficiary}")
        mycursor.execute("SELECT * FROM card_data")
        data = mycursor.fetchall()
        columns = ["ID", "card_holder_name", "card_type", "black_gram", "rice", "oil", "sugar", "wheat"]
        data_frame = pd.DataFrame(data, columns=columns)

        st.write("concerned ID's Card Data")
        if beneficiary in data_frame['ID'].values:
            concerned_data = data_frame[data_frame['ID'] == beneficiary]
            st.write(concerned_data)
            #st.write(data_frame)


            
        st.write("Concerned Commodities for which tranaction is made")
        search_string = text
        commodity_pattern = r'(sugar|rice|wheat|oil|blackgram|black gram)'
        matches = re.findall(commodity_pattern, search_string, flags=re.IGNORECASE)

        st.write(matches)



        st.caption("If you wish to perform additional transactions, you can continue using the different ID. However, if you're finished with your transactions, you have the option to navigate to the report page, where you can generate and review transaction reports.")


    

##################### Generating Report##############
if selected_menu == "Report":
    st.markdown("### Generating Report")
    if st.button('Generate Report', type="primary"):
        st.write('Generating Report')
        import time
        with st.status("Generating data..."):
            st.write("Collecting data...")
            time.sleep(2)
            st.write("Applying Query...")
            time.sleep(1)
            st.write("Getting Dataframe...")
            time.sleep(1)




###TIME
        st.subheader("1. Delayed_Time")
        column_name = "delayed_time_in_minutes"
        table_name = "time_delay"
        query = f"SELECT SUM({column_name}) FROM {table_name}"
        mycursor.execute(query)
        result = mycursor.fetchone()
        #st.write("Total Dlayed Minutes" , result)
        total_delayed_minutes = int(result[0])  # Extract the integer value
        st.write("Total Delayed Minutes:", total_delayed_minutes)

        total_minutes_reference = 7200  # Total minutes for 100%
        delay_percentage = (total_delayed_minutes / total_minutes_reference) * 100
        st.write(f"Delay Percentage: {delay_percentage:.2f}%")

###STOCK
        
        st.subheader("2. Stock Balance")
        query = """
        SELECT
            (logistic_data.black_gram - biometric_data.black_gram_sum) AS Balance_Black_gram,
            (logistic_data.rice - biometric_data.rice_sum) AS Balance_Rice,
            (logistic_data.oil - biometric_data.oil_sum) AS Balance_Oil,
            (logistic_data.sugar - biometric_data.sugar_sum) AS Balance_Sugar,
            (logistic_data.wheat - biometric_data.wheat_sum) AS Balance_Wheat
        FROM
            logistic_data,
            (SELECT 
                SUM(black_gram) AS black_gram_sum,
                SUM(rice) AS rice_sum,
                SUM(oil) AS oil_sum,
                SUM(sugar) AS sugar_sum,
                SUM(wheat) AS wheat_sum
            FROM biometric_data) AS biometric_data;
        """
        stock_df= pd.read_sql_query(query, mydb)
        st.write("Stock Balance:")
        st.write(stock_df)
        
        
#Biometric_stock
        st.write("Biometrically issued stock:")
        query = """
        SELECT
            SUM(sum_black_gram) AS total_black_gram,
            SUM(sum_rice) AS total_rice,
            SUM(sum_oil) AS total_oil,
            SUM(sum_sugar) AS total_sugar,
            SUM(sum_wheat) AS total_wheat
        FROM (
            SELECT
                SUM(black_gram) AS sum_black_gram,
                SUM(rice) AS sum_rice,
                SUM(oil) AS sum_oil,
                SUM(sugar) AS sum_sugar,
                SUM(wheat) AS sum_wheat
            FROM biometric_data
        ) AS subquery
        """
        result = pd.read_sql(query, mydb)
        st.write(result)

#logistic_stock
        st.write("Logistic stock:")
        mycursor.execute("SELECT black_gram , rice , oil ,sugar ,wheat FROM logistic_data")
        data = mycursor.fetchall()
        columns = ["black_gram", "rice", "oil", "sugar", "wheat"]
        data_frame = pd.DataFrame(data, columns=columns)
        st.write(data_frame)

        sum_logistic = data_frame.iloc[0]
        sum_log = sum_logistic.sum()
        #st.write(sum_log)


        sum_biometric = result.iloc[0]
        sum_bio = sum_biometric.sum()
        #st.write(sum_bio)

        
        stock_balance = (sum_log - sum_bio )
        st.write(f"stock balance in Kg: {stock_balance}")
        stock_balance_percentage = (stock_balance / sum_log) * 100
        
        st.write(f"stock_balance_percentage: {stock_balance_percentage:.2f}%")



        
        

###PR

        
    


