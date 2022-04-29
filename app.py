import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas_datareader as web
import plotly.graph_objects as go







returns_methods = ["Mean Returns", "Log Returns"]
risk_methods = ["Covariance"]
risk_free_rates = ["No Risk Rree Rate", "4 Week Treasury Bill", "3 Month Treasury Bill", "6 Month Treasury Bill", "1 Year Treasury Bill", "Manual Input"]
function_list = [ 'Asset Reports', 'Portfolio Risk Analysis (Coming Soon)']

st.header("R-WISE")
with st.expander('Why'):
    st.write(" We want to give investors a glimspe into some of the variable we take into consideration but also...\
             Solrise needs more Fund Managers, hopefully this inspires  \
            someone to start a new Solrise Fund or just become more active on the platform\
                ")


today = dt.date.today()

before = today - dt.timedelta(days=365)
start_date = st.sidebar.date_input('Start date', before)
end_date = st.sidebar.date_input('End date', today)

if start_date < end_date:
    st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.sidebar.error('Error: End date must fall after start date.')                     

sidebar_function = st.sidebar.selectbox("Select Page", function_list)       
if sidebar_function == "Asset Reports":
    
        def relativeret (df):
            rel =df.pct_change()
            cumret = (1+rel).cumprod()-1
            cumret = cumret.dropna()
            return cumret


        # Project Details

        st.header("Solrise Asset Report")
        
        
        st.subheader('Big Three Relative Preformance')
        dropdown = ['ETH-USD', 'BTC-USD', 'SOL-USD']

 

        rwise = (relativeret(yf.download(dropdown, start_date, end_date)['Close'])+1)*100
        st.line_chart(rwise)
        rwise['Date'] = rwise.index



        st.subheader('Relative Preformance')
        options1 = st.multiselect(
            '',
            ['ETH-USD',   'BTC-USD', 'SOL-USD', 'FTT-USD', 'AVAX-USD', 'BNB-USD', 'LUNA1-USD', 'LINK-USD', 'RAY-USD', 'SRM-USD', 'UNI-USD', 'ATLAS-USD', 'POLIS-USD'],
            ['LUNA1-USD', 'FTT-USD', 'AVAX-USD'])



        price_data = web.get_data_yahoo(options1, start_date, end_date)
        
        
        
        tenb = (relativeret(yf.download(options1, start_date, end_date)['Close'])+1)*100

        st.line_chart(tenb)






        close_px = yf.download(options1, start_date, end_date)['Close']
        mavg = close_px.rolling(window=30).mean() # moving average 



        rets = close_px / close_px.shift(1) - 1
        st.subheader('Daily Returns')
        st.line_chart(rets)


        df = price_data.Close
      
        
        df = df.index
        returns=price_data.pct_change()

        corr_df1 = price_data.Close.corr(method='pearson')
        #reset symbol as index (rather than 0-X)
        corr_df1.head().reset_index()
        #del corr_df.index.name
        plt.figure(figsize=(13, 8))



        # title='Relative Return of Assets - 10B <'

        df2 = yf.download(options1, start_date, end_date)[['Close']]

        df2.index.name= 'timestamp'

        df2 = df2.Close.pct_change()

        df2=df2.fillna(0)

        std = df2.std(ddof=0)

        volatility = std**2


        semi_std_pos = df2[df2>0].std(ddof=0)

        semi_std_neg = df2[df2<0].std(ddof=0)
        comparison = pd.concat([semi_std_pos, semi_std_neg], axis=1)

        st.subheader('Volatility ')
   
        
       
      
        
        vol = pd.DataFrame()
        vol['Negative Daily Return Deviation'] = semi_std_neg
        vol['Positive Daily Return Deviation'] = semi_std_pos
        st.bar_chart(vol)
        
        trending = semi_std_pos-semi_std_neg
        trending = trending.sort_values(ascending = True)


        st.subheader('Covariance')
        st.dataframe(corr_df1)
        #Asset Charts



        ratios = yf.download(options1, start_date, end_date)[['Close']]
        ratios.index.name= 'timestamp'
        ratios = ratios.pct_change().dropna()
        ratios['Port'] = ratios.mean(axis=1) # 20% apple, ... , 20% facebook
        # (ratios+1).cumprod().plot()
        # (ratios+1).cumprod()[-1:]
        # 
        def sharpe_ratio(return_series, N, rf):
            mean = return_series.mean() * N -rf
            sigma = return_series.std() * np.sqrt(N)
            return mean / sigma
        N = 365 #255 trading days in a year
        rf =0.01 #1% risk free rate
        sharpes = ratios.apply(sharpe_ratio, args=(N,rf,),axis=0)


        def sortino_ratio(series, N,rf):
            mean = series.mean() * N -rf
            std_neg = series[series<0].std()*np.sqrt(N)
            return mean/std_neg
        sortinos = ratios.apply(sortino_ratio, args=(N,rf,), axis=0 )


        def max_drawdown(return_series):
            comp_ret = (return_series+1).cumprod()
            peak = comp_ret.expanding(min_periods=1).max()
            dd = (comp_ret/peak)-1
            return dd.min()
        max_drawdowns = ratios.apply(max_drawdown,axis=0)

        calmars = ratios.mean()*255/abs(max_drawdowns)


        sharpes = sharpes.Close
        calmars = calmars.Close
        sortinos = sortinos.Close
        max_drawdowns = max_drawdowns.Close
        st.subheader('Max Drawdowns')
        st.bar_chart(max_drawdowns, )

        btstats = pd.DataFrame()
        btstats['Sortino Ratio'] = sortinos
        btstats['Sharpe Ratio'] = sharpes
        btstats['Calmar Ratio'] = calmars

        st.subheader('Ratios')
        st.bar_chart(btstats)
        st.dataframe(btstats)


          
# if sidebar_function == "Portfolio Risk Analysis"
#         #  Hello 
