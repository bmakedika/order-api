import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt


st.set_page_config(page_title='Dashboard', layout='wide')

placeholder = st.empty()

while True:
    with placeholder.container():
        st.title('Order API Live Monitoring Dashboard')
        df = pd.read_csv('audit_log.csv')
        df['requested_at'] = pd.to_datetime(df['requested_at'])

        col1, col2, col3 = st.columns(3)

        with col1:
            total_req = len(df)
            st.metric(label='Total Requests', value=total_req)

        with col2:
            error_count = len(df[df['status_code'] >= 500])
            error_rate = (error_count / total_req) * 100 if total_req else 0
            if error_rate > 10:
                st.metric('System Status', f'{error_rate:.1f}%', delta='CRITICAL', delta_color='inverse')
            else:
                st.metric('System Status', f'{error_rate:.1f}%', delta='STABLE', delta_color='normal')

        with col3:
            avg_lat = round(df['duration_ms'].mean(), 2) if total_req else 0
            st.metric('Average Latency (ms)', f'{avg_lat} ms')

        st.subheader('API Activity')
        st.dataframe(
            df[['requested_at', 'endpoint_name', 'duration_ms', 'status_code']],
            use_container_width=True,
        )

        st.subheader('Latest events')
        st.dataframe(df.tail(10), use_container_width=True)

        # Bar chart: endpoint vs latency
        st.subheader('Performance by Endpoint')
        fig, ax = plt.subplots()
        ax.bar(df['endpoint_name'], df['duration_ms'])
        ax.set_xlabel('Endpoint')
        ax.set_ylabel('Duration (ms)')
        ax.set_title('Performance by Endpoint')
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

        # Pie chart: success/error distribution
        st.subheader('Reliability')
        success_count = len(df[df['status_code'] < 400])
        client_error_count = len(df[(df['status_code'] >= 400) & (df['status_code'] < 500)])
        server_error_count = len(df[df['status_code'] >= 500])

        fig, ax = plt.subplots()
        ax.pie(
            [success_count, client_error_count, server_error_count],
            labels=['Success', 'Client Errors', 'Server Errors'],
            autopct='%1.1f%%',
        )
        ax.set_title('Reliability')
        st.pyplot(fig)

        # Activity over time
        st.subheader('API Activity Over Time')
        df_time = df.copy()
        df_time['requested_at'] = pd.to_datetime(df_time['requested_at'])
        df_time.set_index('requested_at', inplace=True)

        activity_over_time = df_time.resample('1T').size()
        fig, ax = plt.subplots()
        ax.plot(activity_over_time.index, activity_over_time.values)
        ax.set_title('API Activity Over Time')
        ax.set_xlabel('Time')
        ax.set_ylabel('Number of Requests')
        st.pyplot(fig)

        time.sleep(5)