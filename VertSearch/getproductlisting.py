import getebaylistings
from getebaylistings import Ebaylisting
from getwalmartlistings import Walmartlisting
from getamazonlistings import AmazonListing
from readconfig import ProcessConfig

class GetProducts:
    def __init__(self):
        self.config = ProcessConfig()
        self.EbayListOfProducts = []
        self.WalmartListOfProducts = []
        self.AmazonListOfProducts = []

    """ Main call for getting product listing.  Will call each supported
        api for the product listing.  The specific getter for each api Will
        populate the product dictionary and will return that in order to be
        processed for ranking
    """
    def get_products( self, query ):
        return self.get_EbayListings( query ) + self.get_WalmartListings( query ) + self.get_AmazonListings( query )

    def get_EbayListings( self, query ):
        # Get Ebay product listings
        self.EbayListOfProducts.append( \
        Ebaylisting.ProcessQueryEbay( \
        self.config.get_apikey('ebay')[0][0], query ) )
        return self.EbayListOfProducts

    def get_WalmartListings( self, query ):
        # Get Walmart product listings
        self.WalmartListOfProducts.append( \
        Walmartlisting.ProcessQueryWalmart( \
        self.config.get_apikey('walmart')[0][0], query ) )
        return self.WalmartListOfProducts

    def get_AmazonListings( self, query ):
        # Get Amnazon product listings
        self.AmazonListOfProducts.append( \
        AmazonListing.ProcessQueryAmazon( \
        self.config.get_apikey('amazon'), query ) )
        return self.AmazonListOfProducts
