
# Airbus Hackathon

Hi Team This is team Mystic 

Problem Statement: Develop a platform or solution that connects aircraft manufacturers, airlines, and recycling facilities to facilitate the repurposing and recycling of end-of-life aircraft components.

Solution: Created a website where users(Aircraft manufacturers, Airlines, Recycling companies) can login/register, can buy/identify the components that are nearing the end of their lifecycle, and find the dashboard with analysis charts regarding part materials and sustainability

Personas: Aircraft Manufacturer, Airlines, Recycling companies, Admin


Scalability - Can be achieved using clickhouse paid version
Security - Implemented Authentication and Authorization (with encrypted passwords), can also add VPC Layers



## Proposed Architecture

![App Screenshot](https://github.com/Iamprashanth-1/airb/blob/main/images/parch.png)

## Actual Architecture

![App Screenshot](https://github.com/Iamprashanth-1/airb/blob/main/images/actp.png)

## Deployment Process

![App Screenshot](https://github.com/Iamprashanth-1/airb/blob/main/images/cicd.png)

## Flow

![App Screenshot](https://github.com/Iamprashanth-1/airb/blob/main/images/funcd.png)


## Tech Stack

**Client:** HTML, CSS, JS

**Server:** Python(Flask)

**Databse:** ClickHouse

**Data Visualization:** Apache Superset


## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  flask run or Python3 app.py
```

