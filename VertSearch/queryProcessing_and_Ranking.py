from getproductlisting import GetProducts
from static_constants import CStaticConsts
import metapy
import os
import shutil

"""
Process the query to remove stopwords and process the remaining
to get the root word (stemming)
This query will be used to get the data from the product APIs
and this data will be ranked to get a relevant ordered listing
"""

class QueryProcessing():
    def __init__(self):
        """
        Since the data changes with each search we have to clear the inverted
        index since metapy does not have a way of doing it.  We also have to clear
        out the files that represent the returned data.  We are searching for products
        so if we keep all the search data for future searches it may become stale.  We
        want to provide the user with relevant current data.
        """
        self.tempfileDir = 'tempfiles'
        self.tempUrlDir = 'tempUrlDir'
        self.directory = 'ProductList/' + self.tempfileDir
        self.urlDir = 'ProductList/' + self.tempUrlDir
        self.rootProductDir = 'ProductList/'
        self.inv_index = 'indx'
        self.filenameRoot = 'product'
        self.filename = self.filenameRoot + '{}{}.txt'
        self.full_filename = self.directory + '/' + self.filename
        self.full_url_filename = self.urlDir + '/' + self.filename
        self.full_corpus = self.filenameRoot + '-full-corpus.txt'
        self.ProductList = []

        if os.path.exists( self.directory ):
            shutil.rmtree( self.directory )
        if os.path.exists( self.urlDir ):
            shutil.rmtree( self.urlDir )
        if os.path.exists( self.inv_index ):
            shutil.rmtree( self.inv_index )
        if os.path.exists( self.rootProductDir + '/' + self.full_corpus ):
            os.remove( self.rootProductDir + '/' + self.full_corpus )

    """ Main call to start the process of getting the product list
        I'm processing the query to remove the stopwords and to apply stemming.
        This allows for better results from the call to the various apis.

        I'm also checking if query is surrounded by quotes and if so do not process
        for stopwords and stemming.  For some products stopwords are part of the title so
        we would be elliminating many products.
    """
    def getDataFromQuery( self, original_query ):
        if original_query:
            if original_query[ 0 ] != '"' and original_query[ len( original_query ) - 1 ] != '"':
                query = metapy.index.Document()
                query.content( original_query )
                tok = metapy.analyzers.ICUTokenizer( suppress_tags=True )
                tok.set_content( query.content() )
                tok = metapy.analyzers.LowercaseFilter( tok )
                tok = metapy.analyzers.ListFilter( tok, "lemur-stopwords.txt", metapy.analyzers.ListFilter.Type.Reject )
                tok = metapy.analyzers.Porter2Filter( tok )
                processed_Query = ' '.join( [token for token in tok] )
            else:
                processed_Query = original_query

            self.getDataFromAPIs( processed_Query, original_query )
        return self.ProductList

    # Get the actual products and process the data for ranking
    def getDataFromAPIs( self, query, orig_query ):
        products = GetProducts()
        prodlist = products.get_products( query )
        self.ProcessDatatoFiles( prodlist )
        self.GetRankedList( orig_query )

    """ Take the list of products and create the tempfiles for the ranker to
        process.  I'm using a file corpus since that allows me to have as much
        data as I wish in the file.
    """
    def ProcessDatatoFiles( self, prodList ):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        if not os.path.exists(self.urlDir):
            os.makedirs(self.urlDir)

        for sitecount, list in enumerate( prodList ):
            if list is not None:
                for num, item in enumerate( list ):
                    with open( self.full_filename.format( sitecount, num ), 'w' ) as f:
                        f.write( item[ CStaticConsts.title ] + '\n')
                        temp = ''
                        try:
                            temp = float( item[ CStaticConsts.itemPrice ] )
                            temp = '{0:.2f}'.format( float( item[ CStaticConsts.itemPrice ] ) )
                        except ValueError:
                            temp = item[ CStaticConsts.itemPrice ]
                        f.write( item[ CStaticConsts.currencyType ] + ' ' + temp + '\n'  )
                        f.write( item[ CStaticConsts.siteName ] )
                    with open( self.full_url_filename.format( sitecount, num ), 'w' ) as g:
                        g.write( item[ CStaticConsts.productUrl ] )

                        # Add filename to full-corpus
                        with open( self.rootProductDir + '/' + self.full_corpus, 'a' ) as h:
                            h.write( '[none]' + ' ' + self.tempfileDir + '/' + self.filename.format( sitecount, num ) + '\n' )

    """ From the class and the online tutorials OkapiBM25 seems to be the better
        ranking algorithm so that is what I'm using here.
        After the ranking is done I'm retrieving the ranked documents as a list
        of tuples that flask uses to display the data
        Also moved the urls to a different folder outside of the ranking algorithm
        with the same filename as the ranked docs since I did not want those to affect the score
    """
    def GetRankedList( self, origquery ):
        indx = metapy.index.make_inverted_index('config.toml')
        ranker = metapy.index.OkapiBM25()
        rank_query = metapy.index.Document()
        rank_query.content( origquery )
        top = ranker.score( indx, rank_query, num_results = 200 )
        for num, (id, _) in enumerate(top):
            filepath = indx.metadata(id).get('path')
            with open( filepath, 'r') as f:
                temptuple = ( f.readline(), f.readline(), f.readline() )
                #get urls
                urlpath = self.urlDir + '/' + filepath.split('/')[3]
                with open( urlpath, 'r' ) as g:
                    temptuple = temptuple + ( g.readline(), )
                    self.ProductList.append( temptuple )
