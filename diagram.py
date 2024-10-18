from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.network import Nginx
from diagrams.programming.language import NodeJS, Go, Swift
from diagrams.onprem.database import MongoDB
from diagrams.onprem.container import Docker
from diagrams.firebase.grow import Messaging
from diagrams.programming.framework import React

with Diagram("Electric Application Architecture", show=False):
    with Cluster('Client platforms'):
        with Cluster('iOS'):
            ios = Swift('Sthor')
        with Cluster('web'):
            react = React('Rthor')
        
    with Cluster('AWS EC2'):            
        nginx = Nginx("Nginx")
        # Database
        with Cluster('Database/Collections'):
            auth_db = MongoDB("Auth")
            user_db = MongoDB("User")
            device_token_db = MongoDB("Device Tokens")

        # Firebase Cloud Messaging 
        with Cluster('Firebase'):
            fcm = Messaging("Cloud Messaging")
        # Define services                     
        with Cluster('API Gateway'):
            api_gateway = NodeJS("Doctor Strange")
        with Cluster('Backend services'):
            auth = Go("Auth service")             
            user = Go("User service")
            electric = Go("Electric service")
            notifications = Go("Notifications service")
            
    # Architecture
    ios >> nginx 
    react >> nginx
    nginx >> Edge(color="darkgreen") << api_gateway 
    
    api_gateway >> Edge(color="darkgreen") << auth >> auth_db
    api_gateway >> Edge(color="darkgreen") << user >> user_db
    api_gateway >> Edge(color="darkgreen") << electric >> user_db
    api_gateway >> Edge(color="darkgreen") << notifications 
    
    electric >> Edge(color="brown") << notifications
    notifications >> device_token_db
    notifications >> fcm >> Edge(label="get device token") >> ios
        
        