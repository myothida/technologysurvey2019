#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from jupyter_dash import JupyterDash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from wordcloud import WordCloud, STOPWORDS
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2


# ## Current Technology Usage 

# In[2]:


def current_tech(survey_data):
    language_df = survey_data[['Respondent', 'LanguageWorkedWith']]
    language_df = language_df.dropna(axis=0)
    language_df = language_df.groupby(['LanguageWorkedWith']).count()
    language_df.reset_index(inplace = True)
    topten_lan_df = language_df.sort_values(['Respondent'], ascending=False)
    topten_lan_df = topten_lan_df.iloc[0:10, :]    

    db_df = survey_data[['Respondent', 'DatabaseWorkedWith']]
    db_df = db_df.dropna(axis=0)
    db_df = db_df.groupby(['DatabaseWorkedWith']).count()
    db_df.reset_index(inplace = True)
    topten_db_df = db_df.sort_values(['Respondent'], ascending=False)
    topten_db_df = topten_db_df.iloc[0:10, :]    
    
    platform_df = survey_data[['Respondent', 'PlatformWorkedWith']]
    platform_df = platform_df.dropna(axis=0)
    platform_df = platform_df.groupby(['PlatformWorkedWith']).count()
    platform_df.reset_index(inplace = True)  
    
    dwf_df = survey_data[['Respondent', 'WebFrameWorkedWith']]
    dwf_df = dwf_df.dropna(axis=0)
    dwf_df = dwf_df.groupby(['WebFrameWorkedWith']).count()
    dwf_df.reset_index(inplace = True)
    topten_dwf_df = dwf_df.sort_values(['Respondent'], ascending=False)
    topten_dwf_df = topten_dwf_df.iloc[0:10, :]  
    
    
    return topten_lan_df,topten_db_df,platform_df,topten_dwf_df


# In[3]:


def plot_wordcloud(platform_df): 
    data = platform_df['PlatformWorkedWith'].to_string()
    wc = WordCloud(background_color='black', width=840, height=360).generate(data)    
    return wc.to_image()


# In[4]:


survey_data =  pd.read_csv('m5_survey_data_technologies_normalised.csv')
survey_data.info()


# In[5]:


survey_data =  pd.read_csv('m5_survey_data_technologies_normalised.csv')
topten_lan_df,topten_db_df,platform_df,topten_dwf_df = current_tech(survey_data)
topten_lan_df.reset_index(inplace=True)
topten_lan_df.rename(columns = {'Respondent':'Num1'},inplace = True)
topten_db_df.reset_index(inplace=True)
topten_db_df.rename(columns = {'Respondent':'Num2'},inplace = True)
topten_dwf_df.reset_index(inplace =True)
topten_dwf_df.rename(columns = {'Respondent':'Num3'},inplace = True)
current_tech_df = pd.concat([topten_lan_df, topten_db_df, topten_dwf_df], axis = 1)

current_tech_df.to_csv('Current_Tech.csv')
platform_df.to_csv('Current_platform.csv')


# ## Future Technology Trend 

# In[6]:


def future_tech(survey_data):
    f_lang_df = survey_data[['Respondent', 'LanguageDesireNextYear']]
    f_lang_df = f_lang_df.dropna(axis=0)
    f_lang_df = f_lang_df.groupby(['LanguageDesireNextYear']).count()
    f_lang_df.reset_index(inplace = True)
    topten_future_lan_df = f_lang_df.sort_values(['Respondent'], ascending=False)
    topten_future_lan_df = topten_future_lan_df.iloc[0:10, :]

    f_db_df = survey_data[['Respondent', 'DatabaseDesireNextYear']]
    f_db_df = f_db_df.dropna(axis=0)
    f_db_df = f_db_df.groupby(['DatabaseDesireNextYear']).count()
    f_db_df.reset_index(inplace = True)
    topten_fut_db_df = f_db_df.sort_values(['Respondent'], ascending=False)
    topten_fut_db_df = topten_fut_db_df.iloc[0:10, :]

    f_platform_df = survey_data[['Respondent', 'PlatformDesireNextYear']]
    f_platform_df = f_platform_df.dropna(axis=0)
    f_platform_df = f_platform_df.groupby(['PlatformDesireNextYear']).count()
    f_platform_df.reset_index(inplace = True)

    f_dwf_df = survey_data[['Respondent', 'WebFrameDesireNextYear']]
    f_dwf_df = f_dwf_df.dropna(axis=0)
    f_dwf_df = f_dwf_df.groupby(['WebFrameDesireNextYear']).count()
    f_dwf_df.reset_index(inplace = True)
    topten_f_wf_df = f_dwf_df.sort_values(['Respondent'], ascending=False)
    topten_f_wf_df = topten_f_wf_df.iloc[0:10, :]
    
    return topten_future_lan_df,topten_fut_db_df,f_platform_df,topten_f_wf_df


# In[7]:


topten_future_lan_df,topten_fut_db_df,f_platform_df,topten_f_wf_df = future_tech(survey_data)
topten_future_lan_df.reset_index(inplace=True)
topten_future_lan_df.rename(columns = {'Respondent':'Num1'},inplace = True)

topten_fut_db_df.reset_index(inplace=True)
topten_fut_db_df.rename(columns = {'Respondent':'Num2'},inplace = True)

topten_f_wf_df.reset_index(inplace =True)
topten_f_wf_df.rename(columns = {'Respondent':'Num3'},inplace = True)

future_tech_df = pd.concat([topten_future_lan_df,topten_fut_db_df,topten_f_wf_df], axis = 1)

future_tech_df.to_csv('Future_Tech.csv')
f_platform_df.to_csv('Futre_platform.csv')


# ## Demographics

# In[8]:


def demographics(demo_data):
    gender_df = demo_data[['Respondent', 'Gender']]
    gender_df1 = gender_df[(gender_df['Gender']=='Man')|(gender_df['Gender']=='Woman')]
    gender_df1 = gender_df1.groupby(['Gender']).count()
    gender_df1.reset_index(inplace=True)

    country_df = demo_data[['Respondent', 'Country']]
    country_df = country_df.groupby(['Country']).count()
    country_df.reset_index(inplace=True)

    age_df = demo_data[['Respondent', 'Age']]
    age_df.isnull().sum()
    avg_age = age_df['Age'].median()
    age_df = age_df.fillna(value = {'Age':avg_age})
    age_df = age_df.groupby(['Age']).count()
    age_df.reset_index(inplace = True)

    edu_df = demo_data[['Respondent', 'Gender','EdLevel']]
    edu_df = edu_df[(edu_df['Gender']=='Man')|(edu_df['Gender']=='Woman')]
    edu_df = edu_df.groupby(['EdLevel', 'Gender']).count()
    edu_df.reset_index(inplace = True)
    edu_df['EdLevel'] = edu_df['EdLevel'].str.split('(', expand=True)

    return gender_df1,country_df,age_df, edu_df


# In[9]:


demo_data =  pd.read_csv('m5_survey_data_demographics.csv')
gender_df1,country_df,age_df, edu_df = demographics(demo_data)
gender_df1.to_csv('Survey_gender.csv')
country_df.to_csv('Survey_country.csv')
age_df.to_csv('Survey_age.csv')
edu_df.to_csv('Survey_eduLevel.csv')


# In[10]:


#function to convert to alpah2 country codes and continents
def get_continent(col):
    try:
        cn_a2_code =  country_name_to_country_alpha2(col)
    except:
        cn_a2_code = 'Unknown' 
    try:
        cn_continent = country_alpha2_to_continent_code(cn_a2_code)
    except:
        cn_continent = 'Unknown' 
    return (cn_a2_code, cn_continent)


# In[11]:


def country_code(country_df):
    country_df1 = country_df['Country'].str.split(",", expand=True)
    country_df1 = country_df1[0].str.split('(', expand=True)
    country_df1.rename(columns = {0:'Country'}, inplace = True)
    country_df1.drop(1, axis=1, inplace = True)
    country_df1 = country_df1.apply(lambda x: x.str.strip())
    country_df1['Country'] = country_df1['Country'].replace('Libyan Arab Jamahiriya', 'Libya')
    country_df1[['Country_code', 'Continent']] = [get_continent(cn) for cn in country_df1.Country]
    country_df1['Respondent'] = country_df['Respondent']
    country_df1
    return country_df1


# ## Dashboard

# In[12]:


app = JupyterDash(__name__)


# In[13]:


app.layout = html.Div([            
        
        html.H1('Technologies Trend Survey - Data Analsyis',
                 style={'textAlign': 'center', 'color': '#503D36','font-size': 40}),
                    
        #first division for report type
        html.Div([
            # write header            
            html.H2('Report Type:', style={'margin-right': '2em'}),
            # create drop down            
            
            dcc.Dropdown(id='input-type',
                options=[
                    {'label': 'Current Technology Usage', 'value': 'current'},
                    {'label': 'Future Technology Usage', 'value': 'future'},
                    {'label': 'Demographics of Respondents', 'value': 'respond'}
                ],
                placeholder='Select report type...',
                style={'width': '60%', 'padding': '3px', 'textAlign': 'left', 'font-size': 20}),            
        
        ], style = {'display': 'flex'}),                        
 
                    
        #2nd Division 
        html.Div([
                 html.Div(dcc.Graph(id='plot1')),
                 html.Div(dcc.Graph(id='plot2'))
                ], style={'display': 'flex'}),
    
        #3rd Division 
        html.Div([
                 html.Div(dcc.Graph(id='plot3')),
                 html.Div(dcc.Graph(id='plot4'))
                ], style={'display': 'flex'}),
   
])


# In[14]:


@app.callback([               
               Output(component_id='plot1', component_property='figure'),
               Output(component_id='plot2', component_property='figure'),
               Output(component_id='plot3', component_property='figure'),
               Output(component_id='plot4', component_property='figure')               
            ],
            Input(component_id='input-type', component_property='value'),             
            )


def draw_graph(report_type):
    
    if report_type is None:
        raise PreventUpdate
    else:
        survey_data =  pd.read_csv('m5_survey_data_technologies_normalised.csv')
        if (report_type == 'current'):
            topten_lan_df,topten_db_df,platform_df,topten_dwf_df = current_tech(survey_data)
            fig1 = px.bar(topten_lan_df, x = 'LanguageWorkedWith', 
                        y = 'Respondent', color = 'Respondent',
                        title = 'Current Top Ten Language')
            fig2 = px.bar(topten_db_df, y = 'DatabaseWorkedWith', 
                        x = 'Respondent', color = 'Respondent', 
                        orientation = 'h',title = 'Current Top Ten Database')
            
            fig3 = px.treemap(platform_df, path = ['PlatformWorkedWith','Respondent'], 
                              values = 'Respondent', hover_data=['PlatformWorkedWith'],
                             title = 'Current Top Ten Platform')
            fig3.update_traces(root_color="lightgrey")
            fig3.update_layout(margin = dict(t=50, l=25, r=25, b=25))
          
            
            fig4 = px.scatter(topten_dwf_df, x = 'WebFrameWorkedWith',
                            y = 'Respondent', color = 'Respondent', 
                            size = 'Respondent', orientation = 'h',
                            title = 'Current Top Ten Web Frame')
            
            return[fig1,fig2,fig3,fig4]

        elif(report_type =='future'):
            topten_future_lan_df,topten_fut_db_df,f_platform_df,topten_f_wf_df = future_tech(survey_data)
            fig5 = px.bar(topten_future_lan_df, x = 'LanguageDesireNextYear', 
               y = 'Respondent', color = 'Respondent',
             title = 'Future Top Ten Language')

            fig6 = px.bar(topten_fut_db_df, y = 'DatabaseDesireNextYear', 
                          x = 'Respondent', color = 'Respondent', 
                          orientation = 'h',title = 'Future Top Ten Database')

            fig7 = px.treemap(f_platform_df, path = ['PlatformDesireNextYear','Respondent'], 
                              values = 'Respondent', hover_data=['PlatformDesireNextYear'],
                             title = 'Future Top Ten Platform')
            fig7.update_traces(root_color="lightgrey")
            fig7.update_layout(margin = dict(t=50, l=25, r=25, b=25))

            fig8= px.scatter(topten_f_wf_df, x = 'WebFrameDesireNextYear', 
                              y = 'Respondent', color = 'Respondent', 
                              size = 'Respondent', orientation = 'h',
                             title = 'Future Top Ten Web Frame')


            return[fig5,fig6,fig7,fig8]

        else:
            demo_data =  pd.read_csv('m5_survey_data_demographics.csv')
            gender_df1,country_df,age_df, edu_df = demographics(demo_data)
            fig9 = px.pie(gender_df1, values = 'Respondent', names = 'Gender',
                          title = 'Respondent classified by Gender', color = 'Gender',
                          color_discrete_map={'Man':'darkblue', 'Woman': 'red'})

            country_df1 = country_code(country_df)
            fig10 = px.choropleth(country_df1,
                              locations='Country_code',
                              color='Respondent',
                              hover_name='Country',
                              locationmode='country names',
                              #animation_frame='Respondent'
                               )

            fig10.update_layout(
            title_text = 'Number of Respondents by Countries',
            title_x=0.5,
            geo_scope='north america',
            geo=dict(showframe=False,
                    showcoastlines = False))

            fig11 = px.line(age_df, x = 'Age', y = 'Respondent',
                           title =  'Respondent Count by Age')

            fig12 = px.bar(edu_df, x='EdLevel', y = 'Respondent', color= 'Gender',
                          title = 'Respondent Count by Gender, classified by Formal Education Level')
            
            return[fig9,fig10,fig11,fig12]   
    


# In[15]:


app.run_server(mode="external")


# In[ ]:




