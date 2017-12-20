from amazon.api import AmazonAPI
from static_constants import CStaticConsts
import urllib

"""
Main Amazon product listing getter.
"""
class AmazonListing:
    @staticmethod
    def ProcessQueryAmazon( keys, query ):
        try:
            amazon = AmazonAPI( keys[0][0], keys[0][1], keys[0][2] )
            products = amazon.search_n( 100, Keywords = query, SearchIndex = 'All' )

            tempList = []
            if products is not None:
                for item in products:
                    tempDict = {}
                    tempDict[ CStaticConsts.siteName ] = CStaticConsts.Amazon
                    tempDict[ CStaticConsts.title ] = item.title

                    # Some of the amazon price/currency are null
                    # so just populate the field with NA
                    if not item.price_and_currency[1]:
                        tempDict[ CStaticConsts.currencyType ] = 'NA'
                    else:
                        tempDict[ CStaticConsts.currencyType ] = item.price_and_currency[1]
                    if not item.price_and_currency[0]:
                        tempDict[ CStaticConsts.itemPrice ] = 'NA'
                    else:
                        tempDict[ CStaticConsts.itemPrice ] = item.price_and_currency[0]
                    tempDict[ CStaticConsts.productUrl ] = item.offer_url

                    tempList.append( tempDict )

            return tempList

        except urllib.error.HTTPError as e:
            print('Error getamazonlistings: ', e)
        except Exception as e:
            print('Error: getamazonlistings threw exception. Message: ', e)
