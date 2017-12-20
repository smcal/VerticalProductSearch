from wapy.api import Wapy
from static_constants import CStaticConsts

"""
Main Walmart product listing getter.
"""
class Walmartlisting:
    @staticmethod
    def ProcessQueryWalmart( apikey, query ):
        try:
            wapy = Wapy( apikey )
            products = wapy.search( query )

            tempList = []
            if products is not None:
                for item in products:
                    tempDict = {}
                    tempDict[ CStaticConsts.siteName ] = CStaticConsts.Walmart
                    tempDict[ CStaticConsts.title ] = item.name
                    # Walmart only returns prices in USD
                    tempDict[ CStaticConsts.currencyType ] = CStaticConsts.currencyUSD
                    tempDict[ CStaticConsts.itemPrice ] = item.sale_price
                    tempDict[ CStaticConsts.productUrl ] = item.product_url

                    tempList.append( tempDict )

            return tempList
        except Exception as e:
            print('Error: getwalmartlistings threw exception. Message: ', e )
