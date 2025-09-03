import pandas as pd
import pandas_datareader as pdr
import datetime
import streamlit as st

## Sidebar for user input
st.sidebar.header("Select Timeframe")
start_date = st.sidebar.date_input("Start date", datetime.date(2000, 5, 1))
end_date = st.sidebar.date_input("End date", datetime.date(2025, 6, 1))

##Time-Based Data Retrieval
start = datetime.datetime.combine(start_date, datetime.time.min)
end = datetime.datetime.combine(end_date, datetime.time.min)

# Pull Data
#Staffing Levels
unemploy_pop_df = pdr.DataReader('UNEMPLOY', 'fred', start, end) #Unemployed Level - Monthly
open_positions_df = pdr.DataReader('JTSJOL', 'fred', start, end) #Open Positions - Monthly
unemploy_pop_df=unemploy_pop_df.reset_index()
open_positions_df=open_positions_df.reset_index()
staffing_level_df = pd.merge(unemploy_pop_df,open_positions_df,on="DATE",how="outer")
staffing_level_df = staffing_level_df.rename(columns={"UNEMPLOY":"Unemployed Americans","JTSJOL":"Open Positions","DATE":"Month"})
staffing_level_df.plot(x="Month", y=["Unemployed Americans","Open Positions"],ylabel="Americans")
staffing_ratio_health = "Stable"

staffing_ratio_last = staffing_level_df["Open Positions"].iloc[-2] / staffing_level_df["Unemployed Americans"].iloc[-2]
if staffing_ratio_last > 1.50:
    staffing_ratio_health = "Employee Market"
elif staffing_ratio_last < .75:
    staffing_ratio_health = "Employer Market"

#Labor Force Participation Rate
labor_force_df = pdr.DataReader('CIVPART', 'fred', start, end) #Labor Force Participation Rate - Monthly
labor_force_df.rename(columns={"CIVPART":"Labor Force Participation Rate"}, inplace=True)
labor_force_last = labor_force_df.iloc[-1]["Labor Force Participation Rate"]
labor_force_1yr_ago = labor_force_df.iloc[-12]["Labor Force Participation Rate"]
labor_force_change = labor_force_last - labor_force_1yr_ago
labor_force_df = labor_force_df.reset_index()

labor_force_stability = "Stable"
if labor_force_change > 0.5:
    labor_force_stability = "Increasing"
elif labor_force_change < -0.5:
    labor_force_stability = "Decreasing"

#Inflation Data
cpi_df = pdr.DataReader('CPIAUCNS', 'fred', start, end) #Consumer Price Index - Monthly
cpi_df.rename(columns={"CPIAUCNS":"CPI"}, inplace=True)
cpi_df = cpi_df.reset_index()

cpi_last = cpi_df.iloc[-1]["CPI"]
cpi_last_year = cpi_df.iloc[-12]["CPI"]
cpi_change = ((cpi_last - cpi_last_year) / cpi_last_year) * 100
inflation_level = "low"

if cpi_change > 5:
    inflation_level = "Very High"
elif cpi_change > 3:
    inflation_level = "High"
elif cpi_change > 2:
    inflation_level = "Medium"
elif cpi_change > 1:
    inflation_level = "Low"
elif cpi_change < 1:
    inflation_level = "Very Low"
elif cpi_change < 0:
    inflation_level = "Deflation"

ppi_df = pdr.DataReader('PPIACO', 'fred', start, end) #Producer Price Index - Monthly
ppi_df.rename(columns={"PPIACO":"PPI"}, inplace=True)
ppi_df = ppi_df.reset_index()

ppi_last = ppi_df.iloc[-1]["PPI"]
ppi_last_year = ppi_df.iloc[-12]["PPI"]
ppi_change = ((ppi_last - ppi_last_year) / ppi_last_year) * 100

ppi_inflation_level = "Low"

if ppi_change > 5:
    ppi_inflation_level = "Very High"
elif ppi_change > 3:
    ppi_inflation_level = "High"
elif ppi_change > 2:
    ppi_inflation_level = "Medium"
elif ppi_change > 1:
    ppi_inflation_level= "Low"
elif ppi_change < 1:
    ppi_inflation_level = "Very Low"
elif ppi_change < 0:
    ppi_inflation_level= "Deflation"


#GDP Data
gdp_df = pdr.DataReader('GDP', 'fred', start, end) #Gross Domestic Product - Quarterly
gdp_df = gdp_df.reset_index()
qtr_last = gdp_df.iloc[-1]["GDP"]
qtr_2nd_last = gdp_df.iloc[-2]["GDP"]
change_qtr = ((qtr_last - qtr_2nd_last) / qtr_2nd_last) * 100
qtr_3rd_last = gdp_df.iloc[-3]["GDP"]
change_qtr_2 = ((qtr_last - qtr_3rd_last) / qtr_3rd_last) * 100
recession_risk = "Low"

if change_qtr and change_qtr_2 < 0:
    recession_risk = "High"
elif change_qtr < 0 or change_qtr_2 < 0:
    recession_risk = "Medium"

#National Debt
debt_df = pdr.DataReader('FYFSD', 'fred', start, end) #Gross Domestic Product - Quarterly
debt_df.rename(columns={"FYFSD":"National Debt or Surplus"}, inplace=True)
debt_df = debt_df.reset_index()
debt_last = debt_df.iloc[-1]["National Debt or Surplus"]
debt_last_year = debt_df.iloc[-2]["National Debt or Surplus"]
debt_change = ((debt_last - debt_last_year) / debt_last_year) * 100
defecit_spending = "Increasing"

if debt_change < 0:
    defecit_spending = "Decreasing"

#Gini Index
gini_df = pdr.DataReader('SIPOVGINIUSA', 'fred', start, end) #Gini Index - Annual
gini_df.rename(columns={"SIPOVGINIUSA":"Gini Index"}, inplace=True)
gini_df = gini_df.reset_index()
gini_last = gini_df.iloc[-1]["Gini Index"]
gini_last_year = gini_df.iloc[-2]["Gini Index"]
gini_change = gini_last - gini_last_year

gini_stablity = "Stable"
if gini_change > 0.5:
    gini_stablity = "Increasing"
elif gini_change < -0.5:
    gini_stablity = "Decreasing"

#Fertility Rate
fertility_df = pdr.DataReader('SPDYNTFRTINUSA', 'fred', start, end) #Fertility Rate - Annual
fertility_df.rename(columns={"SPDYNTFRTINUSA":"Fertility Rate"}, inplace=True)
fertility_df = fertility_df.reset_index()
fertility_last = fertility_df.iloc[-1]["Fertility Rate"]
fertility_last_year = fertility_df.iloc[-2]["Fertility Rate"]
fertility_change = fertility_last - fertility_last_year

if fertility_last < 1.7:
    fertility_trend = "Below Replacement"
elif fertility_last < 2.1:
    fertility_trend = "At Replacement"
else:
    fertility_trend = "Above Replacement"


#Visualizations

st.header("Welcome to the OpenEcon Dashboard")
st.write("This uses public data to provide unbiased insights into the US economy.")
info_table = pd.DataFrame({
    "Indicator": [
        "Staffing Ratio",
        "Labor Force Stability",
        "Inflation Level",
        "Income Inequality",
        "Recession Risk",
        "Deficit Spending",
        "Fertility Trend"
    ],
    "Value": [
        staffing_ratio_health,
        labor_force_stability,
        inflation_level,
        gini_stablity,
        recession_risk,
        defecit_spending,
        fertility_trend
    ]
})
## Summary Table
st.subheader("Summary Table")
st.dataframe(info_table, use_container_width=True)

## Workforce Insights
st.subheader("Workforce Insights",divider=True)
st.subheader("Open Positions and Unemployed Americans")
st.write("Source: FRED (Federal Reserve Economic Data)")
st.write("Quick overview of the current job market in the US, showing the number of open positions and unemployed Americans over time. 1:1 ratio is considered a healthy job market.")
col1, col2 = st.columns(2)
col1.metric("Current Open Positions", f'{staffing_level_df["Open Positions"].iloc[-2]/1000:.2f}M',help="The number of open positions in the US labor market.")
col2.metric("Current Unemployed Americans", f'{staffing_level_df["Unemployed Americans"].iloc[-1]/1000:.2f}M',help="The number of unemployed individuals in the US labor market.")
st.line_chart(staffing_level_df,x="Month",y=["Open Positions","Unemployed Americans"],y_label="Americans (Thousands)")
st.subheader("Staffing Ratio")
st.write("Source: FRED (Federal Reserve Economic Data)")
st.write("How many jobs are available per unemployed American. A ratio above 1 indicates more open positions than unemployed individuals, suggesting a tight labor market. A ratio below 1 indicates more unemployed individuals than open positions, suggesting a loose labor market.")
staffing_ratio_df=staffing_level_df
staffing_ratio_df["Staffing Ratio"] = staffing_ratio_df["Open Positions"]/staffing_ratio_df["Unemployed Americans"]
col1, col2 = st.columns(2)
col1.metric("Current Staffing Ratio", f"{staffing_ratio_last:.2f}")
col2.metric("Staffing Ratio Health", staffing_ratio_health,help="Indicates whether the job market is favorable for employees or employers based on the staffing ratio.")
st.line_chart(staffing_ratio_df,x="Month",y="Staffing Ratio")
st.subheader("Labor Force Participation Rate")
st.write("Source: FRED (Federal Reserve Economic Data)")
st.write("The labor force participation rate measures the percentage of the working-age population that is either employed or actively seeking employment. It provides insights into the overall engagement of the population in the labor market.")
col1, col2 = st.columns(2)
st.line_chart(labor_force_df,x="DATE",y="Labor Force Participation Rate",y_label="Labor Force Participation Rate (%)")
col1.metric("Current Labor Force Participation Rate", f"{labor_force_last:.2f}%",help=f"The current percentage of the working-age population that is either employed or actively seeking employment. The labor force participation rate is currently {labor_force_stability}.")
col2.metric("Labor Force Stablity",f'{labor_force_stability}',help="Indicates whether the labor force participation rate is increasing, decreasing, or stable based on the change over the last year.")

## Inflation Insights
st.subheader("Inflation Insights",divider=True)
st.subheader("Consumer Price Index (CPI)")
st.write("Source: FRED (Federal Reserve Economic Data)")
st.write("The Consumer Price Index (CPI) measures the average change over time in the prices paid by urban consumers for a market basket of consumer goods and services. It is a key indicator of inflation.")
col1, col2 = st.columns(2)
col1.metric("Annualized Inflation", f"{cpi_change:.2f}%")
col2.metric("Current Inflation Level", inflation_level,help="Inflation level based on the annualized change in CPI over the last year. Very High (>5%), High (3-5%), Medium (2-3%), Low (1-2%), Very Low (<1%), Deflation (<0%).")
st.line_chart(cpi_df,x="DATE",y="CPI")

st.subheader("Producer Price Index (PPI)")
st.write("Source: FRED (Federal Reserve Economic Data)")
st.write("The Producer Price Index (PPI) measures the average change over time in the selling prices received by domestic producers for their output. It is an important indicator of inflation at the wholesale level.")
col1, col2 = st.columns(2)
col1.metric("Annualized PPI Inflation", f"{ppi_change:.2f}%")
col2.metric("PPI Inflation Level", ppi_inflation_level,help="PPI inflation level based on the annualized change in PPI over the last year. Very High (>5%), High (3-5%), Medium (2-3%), Low (1-2%), Very Low (<1%), Deflation (<0%).")
st.line_chart(ppi_df,x="DATE",y="PPI")

## Income Inequality Insights
st.subheader("Gini Index")
st.write("Source: FRED (Federal Reserve Economic Data)")
st.write("The Gini Index measures income inequality within a population, ranging from 0 (perfect equality) to 100 (perfect inequality). It provides insights into the distribution of income and wealth in the US.")
col1, col2 = st.columns(2)
col1.metric("Current Gini Index", f"{gini_last:.2f}")
col2.metric("Income Inequality", gini_stablity,help="Indicates whether income inequality is increasing, decreasing, or stable based on the change in the Gini Index over the last year.")
st.line_chart(gini_df,x="DATE",y="Gini Index")


## Economic Growth Insights
st.subheader("Economic Growth Insights",divider=True)
st.subheader("Gross Domestic Product (GDP)")
st.write("Source: FRED (Federal Reserve Economic Data)")
st.write("Gross Domestic Product (GDP) is the total value of all goods and services produced in the US. It is a broad measure of economic activity and an important indicator of economic health.")
col1, col2, col3= st.columns(3)
col1.metric("Last Quarter", f"{change_qtr:.2f}%")
col2.metric("Two Quarters Ago", f"{change_qtr_2:.2f}%")
col3.metric("Recession Risk", recession_risk,help="Risk of recession based on GDP changes over the last two quarters.")
st.line_chart(gdp_df,x="DATE",y="GDP")
st.subheader("National Debt Insights")
st.write("Source: FRED (Federal Reserve Economic Data)")
st.write("The national debt is the total amount of money that the US government owes to creditors. It is an important indicator of the country's fiscal health and can impact economic growth and stability.")
col1, col2 = st.columns(2)
col1.metric("Annual Change in National Debt Spending", f"{debt_change:.2f}%")
col2.metric("Deficit Spending", defecit_spending,help="Indicates whether the national debt is increasing or decreasing based on the change in national debt over the last year.")
st.line_chart(debt_df,x="DATE",y="National Debt or Surplus",y_label="National Surpluss (or Debt) in Millions")

#Population Insights
st.subheader("Population Insights",divider=True)
st.subheader("Fertility Rate")
st.write("Source: FRED (Federal Reserve Economic Data)")
st.write("The fertility rate measures the average number of children born per Couple. It provides insights into population growth and demographic trends in the US.")
col1, col2, col3 = st.columns(3)
col1.metric("Current Fertility Rate", f"{fertility_last:.2f}",help="The average number of children born per Couple in the US.")
col2.metric("Fertility Rate Change", f"{fertility_change:.2f}",help="Change in the fertility rate over the last year.")
col3.metric("Fertility Trend", fertility_trend,help="Indicates whether the fertility rate is below, at, or above the replacement level of 2.1 births per couple.")
st.line_chart(fertility_df,x="DATE",y="Fertility Rate",y_label="Fertility Rate (Births per Couple)")     