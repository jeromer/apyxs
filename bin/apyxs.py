#!/usr/bin/env python

# Copyright 2009 Jerome Renard
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# 
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License. 

from optparse import OptionParser
from xml.etree.ElementTree import ElementTree

def main():
    parser = OptionParser()

    parser.add_option("-f",
                      "--file",
                      action="store",
                      type="string",
                      dest="filename",
                      help="write report to FILE",
                      metavar="FILE")

    (options, args) = parser.parse_args()

    if not options.filename:
        print("Please specify a filename for your module description")
        exit(2)
    else:
        print("Using file {0}".format(options.filename))

        tree = ElementTree()
        tree.parse(options.filename)
        apacheModule = ApacheModule(tree)
        apacheModule.generateModuleSkeleton()

#        try:
#            tree.parse(options.filename)
#            apacheModule = ApacheModule(tree)
#            apacheModule.generateModuleSkeleton()
#         except Exception:
#             print("Error opening {0} not an XML file" . format(options.filename))
#             exit(1)
   
# Module handling -------------

class ApacheModule:
    def __init__(self, descriptionTree):
        self.descriptionTree = descriptionTree

    def getName(self):
        apacheModuleName = ApacheModuleName(self.descriptionTree)
        name = apacheModuleName.getName()
        print("[DEBUG] Module name is : {0}" . format(name))
        return name

    def getConfiguration(self):
        apacheModuleConfigurationDirective = ApacheModuleConfigurationDirective(self.descriptionTree)
        directiveList = apacheModuleConfigurationDirective.getDirectiveList()
        print("[DEBUG] Configuration directives are : {0}" . format(directiveList))
        return directiveList

    def getHooks(self):
        print("getHooks")

    def generateModuleSkeleton(self):
        print("Generating module skeleton")
        self.getName()
        self.getConfiguration()

class ApacheModuleName:
    def __init__(self, descriptionTree):
        self.descriptionTree = descriptionTree

    def getName(self):
        return self.descriptionTree.find('/name').text

class ApacheModuleConfigurationDirective:

    def __init__(self, descriptionTree):
        self.descriptionTree = descriptionTree
        self.directiveList   = []

    def getDirectiveList(self):
        configuration = self.descriptionTree.find('/configuration')

        directiveList = configuration.getiterator('directive')
        for configurationDirective in directiveList:
            self.directiveList.append(self.getDirective(configurationDirective))

    def getDirective(self, configurationDirective):
        name = configurationDirective.find('name').text
        type = configurationDirective.find('type').text

        valueList = configurationDirective.getiterator('value')
        values = []
        for value in valueList:
            values.append(value.text)
        
        directive = {'name'  : name,
                     'type'  : type,
                     'values': values}

        return directive

if __name__ == "__main__":
    main()