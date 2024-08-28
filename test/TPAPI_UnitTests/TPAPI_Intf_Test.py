'''
Created on 2 Oct 2012

@author: ebrifol
'''
import unittest
import os
import TPAPI
import pickle
import re


path = os.getcwd()
path = re.sub('\\TPAPI_UnitTests$', '\\TestInputs', path )

class TPAPI_IntfVersion_Test(unittest.TestCase):
    
    #def setUp(self):
        #print path


    def tearDown(self):
        self.recursiveDelete(Dirpath=path)
                    
    def recursiveDelete(self, Dirpath):
        for file in os.listdir(Dirpath):
            if not file.endswith(".tpi") and not file.endswith(".pickle") and not file.endswith(".xml"):
                try:
                    if os.path.isdir(Dirpath+"\\"+file):
                        Dirpath = Dirpath+"\\"+file
                        self.recursiveDelete(Dirpath)
                        os.removedirs(Dirpath)
                    else:
                        os.remove(Dirpath+"\\"+file)
                except:
                    pass

    def testInitialization(self):
        interface = TPAPI.InterfaceVersion()
        self.assertEqual(interface.intfVersionID, 'UNINITIALISED:0')
        
        interface = TPAPI.InterfaceVersion(intfName="InterFaceName",intfVersion="1234")
        self.assertEqual(interface.intfVersionID, 'InterFaceName:1234')
        
        self.assertRaises(TypeError, lambda: TPAPI.InterfaceVersion(intfName="InterFaceName"))
        
        self.assertRaises(TypeError, lambda: TPAPI.InterfaceVersion(intfVersion="InterFaceName"))
        
    def testGettingPropertiesFromTpi(self):
        interface = TPAPI.InterfaceVersion()
        interface.getPropertiesFromTPI(filename=path+"\\INTF_DC_E_TEST_R1A_b1.tpi")
        #pickleout = open( path+"\\INTF_DC_E_TEST_R1A_b1.pickle", "wb" )
        #pickle.dump(interface, pickleout)
        #pickleout.close()
        pickleInterface = pickle.load(open( path+"\\INTF_DC_E_TEST_R1A_b1.pickle", "rb" ))

        dummyFlag,deltaObj,deltaTPV = interface._difference(intfVerObject=pickleInterface)
        self.assertEqual(deltaObj.getNumChanges(), 0, "No differences")
        


class TPAPI_Intf_Test(unittest.TestCase):

    def testInitialization(self):
        interface = TPAPI.Interface(intfName="Name")
        self.assertEqual(interface.name, 'Name')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()