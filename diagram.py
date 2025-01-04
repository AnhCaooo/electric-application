from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.network import Nginx
from diagrams.programming.language import NodeJS, Go, Swift
from diagrams.onprem.database import MongoDB
from diagrams.firebase.grow import Messaging
from diagrams.programming.framework import React, FastAPI
from diagrams.custom import Custom

with Diagram("Electric Application Architecture", show=True):
    # Client services 
    with Cluster('Client platforms'):
        with Cluster('iOS'):
            ios = Swift('Sthor')
        with Cluster('web'):
            react = React('Rthor')

    # Firebase Cloud Messaging 
    fcm = Messaging("Cloud Messaging")   
    # Supabase 
    supabase = Custom("Supabase Auth", "./assets/supabase.png")

    with Cluster('AWS EC2'):   
        nginx = Nginx("Web Server")
        api_gateway = NodeJS('API Gateway')
        with Cluster('Services'):
            auth = FastAPI('Auth service')
            rabbitMQ = Custom("Message Broker", "./assets/rabbit.png")
            electric = Go('Electric service')
            notifications = Go('Notifications service')
        
        with Cluster('Database'):
            user_db = MongoDB("User")
            device_token_db = MongoDB("Device Tokens")

    # Architecture
    ios >> nginx 
    react >> nginx
    nginx >>  api_gateway 
    api_gateway >> Edge(color="brown") >> auth 
    
    auth >> Edge(color="darkgreen") << supabase 
    auth >> Edge(label="producer") >> rabbitMQ
    rabbitMQ >> Edge(label="consumer/producer") << electric
    electric >> user_db
    
    rabbitMQ << Edge(label="consumer") << notifications
    notifications >> device_token_db 
    notifications >> Edge(label="send notifications to fcm") >> fcm
    fcm >> Edge(label="push notifications", color="orange") >> ios
    
    
        