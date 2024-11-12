def get_company_from_mail(email): 


    dictionary = {

        'AirSeaLogistics' : {
            "msolis@airsealog.com": { 
                "rol" : "CustomerService",
                "name" : "Mária Solis"
                
                },
            "Alfa VlueIO <alfa.vlueio@gmail.com>" :{

                "rol" : "CustomerService",
                "name" : "Mária Solis"
            }


        }

    }

    return next( (company for company, data in dictionary.items() if email in data), None )

  