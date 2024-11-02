from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.network import Nginx
from diagrams.programming.language import NodeJS, Go, Swift
from diagrams.onprem.database import MongoDB
from diagrams.firebase.grow import Messaging
from diagrams.programming.framework import React, FastAPI
from diagrams.custom import Custom

with Diagram("Electric Application Architecture", show=False):
    # Client services 
    with Cluster('Client platforms'):
        with Cluster('iOS'):
            ios = Swift('Sthor')
        with Cluster('web'):
            react = React('Rthor')


    # Firebase Cloud Messaging 
    with Cluster('Firebase'):
        fcm = Messaging("Cloud Messaging")   

    # Supabase 
    with Cluster("Supabase"):
        supabase = Custom("Supabase Auth", "./assets/supabase.png")

    with Cluster('AWS EC2'):   
        with Cluster('Nginx'):         
            nginx = Nginx("Web Server")

        # Database
        with Cluster('Mongodb'):
            user_db = MongoDB("User")
            device_token_db = MongoDB("Device Tokens")
        
        # Define services                     
        with Cluster('API Gateway'):
            api_gateway = NodeJS("Doctor Strange")
        with Cluster('Backend services'):
            electric = Go("Electric service")
            notifications = Go("Notifications service")
            auth = FastAPI("Auth service")


    # Architecture
    ios >> nginx 
    react >> nginx
    nginx >>  api_gateway 
    
    api_gateway >> auth 
    auth >> supabase
    
    api_gateway >> electric >> user_db
    api_gateway >> notifications 
    
    # electric >> Edge(color="brown") << notifications
    notifications >> device_token_db
    notifications >> fcm >> Edge(label="get device token") >> ios
        
        