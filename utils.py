import clickhouse_connect
import pandas as pd
client = clickhouse_connect.get_client(host='dd8vv8kg7q.us-east-1.aws.clickhouse.cloud', port=8443, username='default', password='C4.Z.~~oGqX5p')
def gen_user_table():

    SQL = '''
    CREATE TABLE IF NOT EXISTS Users (
        id int,
        email String,
        password String,
        usertype String,
        manufacturer String,
        created_at DateTime('Asia/Kolkata') default now(),
        PRIMARY KEY (id)
        );

        

    '''
    sql1 = '''
    create table if not EXISTS Manufacturer  (
    Manufacturer String,
    createdAt TIMESTAMP DEFAULT now(),
        PRIMARY key(Manufacturer)
    );
     
       '''
    client.command(SQL)
    client.command(sql1)

gen_user_table()

def get_manufacture_from_email(email):
    SQL = f'''
    SELECT manufacturer FROM Users WHERE email='{email}'
    '''
    res = client.query(SQL)
    try:
        return res.result_rows[0][0]
    except:
        return None

def get_table_data(email):
    manuf = get_manufacture_from_email(email)
    SQL = f'''
    SELECT "Part Name" ,"Material Composition", "Age (years)","Condition","Potential Use Cases","Location" FROM airb where "Manufacturer"='{manuf}' limit 500
    '''
    res = client.query(SQL)
    cols = ["Part Name" ,"Material Composition", "Age (years)","Condition","Potential Use Cases","Location"]
    aws =[]
    for i in res.result_rows:
        de = {cols[0]:i[0],cols[1]:i[1],cols[2]:i[2],cols[3]:i[3],cols[4]:i[4],cols[5]:i[5]}
        aws.append(de)
    return aws


def insert_data(df):
    client.insert_df('airb', df)
    return True


def get_query_data(email,query,mat ,pote):
    manuf = get_manufacture_from_email(email)
    sql= f'''
    SELECT * FROM airb where "Manufacturer"='{manuf}' and "Part Name"='{query}' and "Material Composition" = '{mat}' and "Potential Use Cases" = '{pote}'
     
      order by "Age (years)" asc,"Condition" asc  limit 500
    '''

    try:
        res = client.query(sql)
        cols = res.column_names
        va = res.result_rows
        fin = []
        for i in range(len(va)):
            vf = {}
            for j in range(len(cols)):
                vf[cols[j]] = va[i][j]
            fin.append(vf)
        # print(fin)


        return fin
    except:
        return None


def get_parts(email):
    manuf = get_manufacture_from_email(email)
    SQL = f'''
    select distinct "Part Name","Material Composition","Potential Use Cases" from airb where "Manufacturer"='{manuf}' limit 500
    '''
    res = client.query(SQL)
    we = {}
    wf= {}
    for i in res.result_rows:
        if i[0] in we.keys():
            we[i[0]].add(i[1])
        else:
            we[i[0]] = set([i[1]])
        
        if i[0]+i[1] in wf.keys():
            wf[i[0]+i[1]].add(i[2])
        else:
            wf[i[0]+i[1]] = set([i[2]])
    for i in we.items():
        we[i[0]] = list(i[1])
    for i in wf.items():
        wf[i[0]] = list(i[1])
    return we,wf


    return res.result_rows

def get_manufacturer():
    SQL = '''
    SELECT Manufacturer FROM Manufacturer
    '''
    res = client.query(SQL)
    return res.result_rows

def get_email_password(email,password,usertype):
    SQL = f'''
    SELECT email,password,usertype FROM Users WHERE email='{email}' AND password='{password}' AND usertype='{usertype}'
    '''
    res = client.query(SQL)
    try:
        return res.result_rows[0]
    except:
        return None


import plotly.graph_objects as go
import plotly.express as px


def recycle_data():
    SQL = f'''
    SELECT * FROM airb where "Remanufacturing Potential (%)" > 90 limit 500
    '''
    res = client.query(SQL)
    cols = res.column_names
    va = res.result_rows
    fin = []
    for i in range(len(va)):
        vf = {}
        for j in range(len(cols)):
            vf[cols[j]] = va[i][j]
        fin.append(vf)
    return fin

def get_plot1(email):
    manuf = get_manufacture_from_email(email)

    f= client.query(f'''select distinct "Material Composition", count("Material Composition") from airb where "Manufacturer"='{manuf}' group by "Material Composition"  ''')
    x_axis = []
    y_axis = []
    for i in f.result_rows:
        x_axis.append(i[0])
        y_axis.append(i[1])

    fig = go.Figure(
        data=[go.Bar(x=x_axis, y=y_axis)],
        layout=go.Layout(
            title=go.layout.Title(text='Material Composition'),
            xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text='Material')),
            yaxis=go.layout.YAxis(title=go.layout.yaxis.Title(text='Count')),
            width=600, 
            height=400 
        )
    )
    return fig._repr_html_()

def get_plot2(email):
    manuf = get_manufacture_from_email(email)
    f= client.query(f'''select  "Material Composition", count("Recycling Rate (%)") from airb where "Manufacturer"='{manuf}' group by "Material Composition" ''')
    x_axis = []
    y_axis = []
    for i in f.result_rows:
        x_axis.append(i[0])
        y_axis.append(i[1])

    #grouped = df.groupby('Material Composition')['Recycling Rate (%)'].count()
    fig = px.pie( values=y_axis, names=x_axis,
                title='Recycling Rate by Material Composition')
    fig.update_layout(
        width=800,
        height=600,
        margin=dict(l=50, r=50, t=100, b=100),
    )
    return fig._repr_html_()


def get_plot3(email):
    manuf = get_manufacture_from_email(email)
    f= client.query(f'''select sum("New Parts Carbon Footprint (kg CO2e)")-sum("Recycled Parts Carbon Footprint (kg CO2e)") , sum("Water Usage - New Parts (liters)")-sum("Water Usage - Recycled Parts (liters)"),sum("Landfill Waste - New Parts (kg)")-sum("Landfill Waste - Recycled Parts (kg)") from airb where "Manufacturer"='{manuf}' ''')
    vals = f.result_rows[0]
    co2_reduction = vals[0]
    water_reduction = vals[1]
    waste_reduction = vals[2]
    fig = go.Figure(go.Bar(
        x=['CO2 Emissions', 'Water Usage', 'Landfill Waste'],
        y=[co2_reduction, water_reduction, waste_reduction],
        text=[f"{co2_reduction:.2f} kg", f"{water_reduction:.2f} liters", f"{waste_reduction:.2f} kg"],
        textposition='auto'
    ))
    fig.update_layout(
        title='Environmental Impact Metrics',
        yaxis_title='Reduction (kg or liters)',
        xaxis_title=None
    )
    fig.update_layout(
        title='Environmental Impact Metrics',
        yaxis_title='Reduction (kg or liters)',
        xaxis_title=None,
        height=400,
        width=600
    )
    return fig._repr_html_()



def get_plot4(email):
    manuf = get_manufacture_from_email(email)
    # grouped_data = df.groupby('Condition')[['Recycling Rate (%)', 'Renewable Material Content (%)', 'Carbon Footprint Saved (kg CO2e)', 'Landfill Waste Saved (kg)']].mean().reset_index()
    f = client.query(f'''select "Condition", avg("Recycling Rate (%)"), avg("Renewable Material Content (%)"), avg("Carbon Footprint Saved (kg CO2e)"), avg("Landfill Waste Saved (kg)") from airb where "Manufacturer"='{manuf}' group by "Condition"''')
    
    df = pd.DataFrame(f.result_rows, columns=['Condition' ,'Recycling Rate (%)', 'Renewable Material Content (%)', 'Carbon Footprint Saved (kg CO2e)', 'Landfill Waste Saved (kg)'])
    
    fig = px.bar(df,x='Condition', y=[ 'Recycling Rate (%)', 'Renewable Material Content (%)', 'Carbon Footprint Saved (kg CO2e)', 'Landfill Waste Saved (kg)'],
                title='Circular Economy Performance Metrics by Condition', 
                labels={'value': 'Mean Value', 'variable': 'Metrics', 'Condition': 'Condition'},
                barmode='group')

    fig.update_layout(
        legend_title='Metrics', 
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        width=800,
        height=400 
    )
    return fig._repr_html_()

    fig.show()
