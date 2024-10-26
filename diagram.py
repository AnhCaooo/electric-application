from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.network import Nginx
from diagrams.programming.language import NodeJS, Go, Swift
from diagrams.onprem.database import MongoDB, PostgreSQL
from diagrams.onprem.container import Docker
from diagrams.firebase.grow import Messaging
from diagrams.programming.framework import React
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
    
    with Cluster('AWS EC2'):   
        with Cluster('Web Server & Reverse proxy'):         
            nginx = Nginx("Nginx")
        with Cluster("IAM service"):
            # define keycloak data 
            keycloak = Custom("Keycloak", "./assets/keycloak.png")

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
            
        keycloak_db = PostgreSQL("Keycloak")
        
            
    # Architecture
    ios >> nginx 
    react >> nginx
    nginx >> Edge(color="darkgreen") << keycloak 
    keycloak >> keycloak_db
    keycloak >> Edge(color="darkgreen", label="If authenticate successful") >> api_gateway 
    
    api_gateway >> electric >> user_db
    api_gateway >> notifications 
    
    # electric >> Edge(color="brown") << notifications
    notifications >> device_token_db
    notifications >> fcm >> Edge(label="get device token") >> ios
        
        