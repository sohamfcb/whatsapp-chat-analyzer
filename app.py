import streamlit as st
import preprocessor  # Assuming this is your custom preprocessing module
import helper  # Assuming this is your custom helper module
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import traceback  # Import traceback module for exception handling

# Function to create the Streamlit application
def main():
    # Set the title for the Streamlit sidebar
    st.sidebar.title('WhatsApp Chat Analyzer')

    # File uploader to upload WhatsApp chat data
    uploaded_file = st.sidebar.file_uploader('Choose a File')

    if uploaded_file is not None:
        # Read and decode the uploaded file data
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode('utf-8')

        try:
            # Preprocess the data using a custom function (prepocessor.preprocess assumed to be defined)
            df = preprocessor.preprocess(data)

            # Display the processed DataFrame (uncomment if needed for debugging)
            # st.dataframe(df)

            # Get unique users from the DataFrame
            user_list = df['user'].unique().tolist()
            user_list.sort()
            user_list.insert(0, 'Overall')

            # Select a user to show analysis for
            selected_user = st.sidebar.selectbox('Show Analysis w.r.t', user_list)

            # Button to trigger analysis
            if st.sidebar.button('Show Analysis'):
                # Fetch statistics based on selected user
                num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

                # Display top statistics
                st.title('Top Statistics')
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.header('Total Messages')
                    st.title(num_messages)

                with col2:
                    st.header('Total Words')
                    st.title(words)

                with col3:
                    st.header('Media Shared')
                    st.title(num_media_messages)

                with col4:
                    st.header('Links Shared')
                    st.title(num_links)

                # Display monthly timeline of messages
                st.title('Monthly Timeline')
                try:
                    timeline = helper.monthly_timeline(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.plot(timeline['time'], timeline['message'])
                    plt.xticks(rotation='vertical')
                    plt.tight_layout()
                    st.pyplot(fig)

                    # Display daily timeline of messages
                    st.title('Daily Timeline')
                    daily_timeline = helper.daily_timeline(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.plot(daily_timeline['date'], daily_timeline['message'], color='green')
                    plt.xticks(rotation='vertical')
                    plt.tight_layout()
                    st.pyplot(fig)

                    # Display activity map
                    st.title('Activity Map')
                    col1, col2 = st.columns(2)

                    with col1:
                        st.header('Most Busy Day')
                        busy_day = helper.week_activity_map(selected_user, df)
                        fig, ax = plt.subplots()
                        ax.bar(busy_day.index, busy_day.values, color='brown')
                        plt.tight_layout()
                        st.pyplot(fig)

                    with col2:
                        st.header('Most Busy Month')
                        busy_month = helper.monthly_activity_map(selected_user, df)
                        fig, ax = plt.subplots()
                        ax.bar(busy_month.index, busy_month.values, color='orange')
                        plt.xticks(rotation='vertical')
                        plt.tight_layout()
                        st.pyplot(fig)

                    # Display weekly activity heatmap
                    st.title('Weekly Activity Map')
                    user_heatmap = helper.activity_heatmap(selected_user, df)
                    fig, ax = plt.subplots()
                    sns.heatmap(user_heatmap, ax=ax)
                    plt.tight_layout()
                    st.pyplot(fig)

                    if selected_user == 'Overall':
                        # Display most active users if overall analysis is selected
                        st.title('Most Active Users')
                        x, new_df = helper.most_active_users(df)
                        fig, ax = plt.subplots()

                        col1, col2 = st.columns(2)

                        with col1:
                            colors = ['black', 'blue', 'brown', 'green', 'yellow']
                            ax.bar(x.index, x.values, color=colors)
                            plt.xticks(rotation='vertical')
                            st.pyplot(fig)

                        with col2:
                            st.dataframe(new_df)

                    # Display word cloud for selected user
                    st.title('WORDCLOUD')
                    df_wc = helper.create_wordcloud(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.imshow(df_wc)
                    st.pyplot(fig)

                    # Display most common words
                    most_common_df = helper.most_common_words(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.barh(most_common_df['Word'], most_common_df['Frequency'])
                    plt.xticks(rotation='vertical')
                    st.title('Most Common Words')
                    st.pyplot(fig)

                    st.dataframe(most_common_df)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    # Print traceback for debugging
                    traceback.print_exc()

        except Exception as e:
            st.error(f"Error during preprocessing: {e}")
            # Print traceback for debugging
            traceback.print_exc()

# Entry point of the application
if __name__ == "__main__":
    main()
