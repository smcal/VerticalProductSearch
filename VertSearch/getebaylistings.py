import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
from static_constants import CStaticConsts

"""
Main EBay product listing getter.
"""
class Ebaylisting:
    @staticmethod
    def ProcessQueryEbay( apikey, query ):
        try:
            tempList = []
            api = Connection( appid = apikey, config_file=None )
            response = api.execute( 'findItemsAdvanced', { 'keywords': query } )

            if hasattr( response.reply.searchResult, 'item' ):
                for item in response.reply.searchResult.item:
                    tempDict = {}
                    tempDict[ CStaticConsts.siteName ] = CStaticConsts.Ebay
                    tempDict[ CStaticConsts.title ] = item.title
                    tempDict[ CStaticConsts.currencyType ] = item.sellingStatus.currentPrice._currencyId
                    tempDict[ CStaticConsts.itemPrice ] = item.sellingStatus.currentPrice.value
                    tempDict[ CStaticConsts.productUrl ] = item.viewItemURL

                    tempList.append( tempDict )

                return tempList

        except ConnectionError as e:
            print( e )
            print( e.response.dict() )
        except Exception as e:
            print( 'Error: getebaylistings threw exception. Message: ', e )
