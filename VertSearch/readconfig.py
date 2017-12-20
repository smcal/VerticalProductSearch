import configparser

"""
Read configuration data
"""
class ProcessConfig:
    def __init__(self):
        self.apiConfig = configparser.RawConfigParser()
        configFilePath = r'api-config.cfg'
        self.apiConfig.read( configFilePath )
        self.keyList = []

    def get_apikey( self, sitename ):
        # Clear list for multiple calls
        self.keyList.clear()
        if sitename == "amazon":
            acckey = self.apiConfig.get( sitename, 'accessKey' )
            seckey = self.apiConfig.get( sitename, 'secretKey' )
            assoctag = self.apiConfig.get( sitename, 'assocTag' )
            self.keyList.append( ( acckey, seckey, assoctag ) )
        else:
            self.keyList.append( ( self.apiConfig.get( sitename, 'apikey'), ) )
        return self.keyList
