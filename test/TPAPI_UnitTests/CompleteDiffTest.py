'''
Created on 4 Dec 2012

@author: ebrifol
'''
import unittest
import os
import TPAPI
import pickle
import re
import traceback
import sys, stat


path = os.getcwd()
path = re.sub('\\TPAPI_UnitTests$', 'TestInputs', path )
server = "atclvm636.athtem.eei.ericsson.se"
baseTpiName="\\DC_E_TEST_R8B_b103.tpi"
upgradeTpiName="\\DC_E_TEST_R8C_b104.tpi"
baseServer = None
upgradeServer = None

class CompleteDiffTest(unittest.TestCase):
    
    def createPickleObject(self, fileName, difobject):
        pickleout = open( path+"\\"+fileName, "wb" )
        pickle.dump(difobject, pickleout)
        pickleout.close()
        
    def loadFromServer(self, VersionID):
        server = None
        try:
            server = TPAPI.TechPackVersion(VersionID)
            server.getPropertiesFromServer(server)
        except:
            print "Could not load "+VersionID+" from "+server
        return server
        
        
    def loadFromTpi(self, TpiPath):
        Tpi = None
        try:
            Tpi = TPAPI.TechPackVersion()
            Tpi.getPropertiesFromTPI(filename=TpiPath)
        except:
            print "Could not load from tpi: "+ TpiPath
        return Tpi
    

    def testDiff(self):
        #Load Techpacks from tpi
        print "Loading TPI's"
        baseTpi = self.loadFromTpi(path+baseTpiName)
        upgradeTpi = self.loadFromTpi(path+upgradeTpiName)
        
        #Load techpacks from server
        print "Loading from server"
        if baseTpi != None:
            baseServer = self.loadFromServer(baseTpi.versionID)
        else: 
            print "Unable to load from server. No versionID available"
            
        if upgradeTpi != None:
            upgradeServer = self.loadFromServer(upgradeTpi.versionID)
        else:
            print "Unable to load from server. No versionID available"
            
        
        print "Doing diff of tpi's"
        if baseTpi != None and upgradeTpi != None:
            fileName = "tpiDiffPickle"
            diffObject = baseTpi.difference(upgradeTpi)
            self.createPickleObject(fileName, diffObject)
            pickleDiff = pickle.load(open( path+"\\"+fileName+".pickle", "rb" ))
            self.assertEqual(pickleDiff.getNumChanges(), diffObject.getNumChanges())
        
        print "Doing diff of base tpi and base server"    
        if baseTpi != None and baseServer != None:
            diffObject = baseTpi.difference(baseServer)
            self.assertEqual(diffObject.getNumChanges(), 0)
        
        print "Doing diff of upgrade tpi and server"  
        if upgradeTpi != None and upgradeServer != None:
            diffObject = upgradeTpi.difference(upgradeServer)
            self.assertEqual(diffObject.getNumChanges(), 0)
        
        print "Doing diff of base tpi and upgrade server"  
        if baseTpi != None and upgradeServer != None:
            fileName = "tpiToServerDiffPickle"
            diffObject = baseTpi.difference(upgradeServer)
            self.createPickleObject(fileName, diffObject)
            pickleDiff = pickle.load(open( path+"\\"+fileName+".pickle", "rb" ))
            self.assertEqual(pickleDiff.getNumChanges(), diffObject.getNumChanges())
        
        print "Doing diff of base server and upgrade tpi"   
        if upgradeTpi != None and baseServer != None:
            fileName = "serverToTpiDiffPickle"
            diffObject = baseServer.difference(upgradeTpi)
            self.createPickleObject(fileName, diffObject)
            pickleDiff = pickle.load(open( path+"\\"+fileName+".pickle", "rb" ))
            self.assertEqual(pickleDiff.getNumChanges(), diffObject.getNumChanges())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()