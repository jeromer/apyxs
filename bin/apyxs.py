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
        return name

    def getConfiguration(self):
        apacheModuleConfigurationDirective = ApacheModuleConfigurationDirective(self.descriptionTree)
        directiveList = apacheModuleConfigurationDirective.getDirectiveList()
        return directiveList

    def getHooks(self):
        apacheModuleHook = ApacheModuleHook(self.descriptionTree)
        hookList = apacheModuleHook.getHookList()
        return hookList

    def generateModuleSkeleton(self):
        name                       = self.getName()
        configurationDirectiveList = self.getConfiguration()
        hookList                   = self.getHooks()

class ApacheModuleName:
    def __init__(self, descriptionTree):
        self.descriptionTree = descriptionTree

    def getName(self):
        return self.descriptionTree.find('/name').text

class ApacheModuleConfigurationDirective:
    def __init__(self, descriptionTree):
        self.descriptionTree = descriptionTree

    def getDirectiveList(self):
        configurationTag = self.descriptionTree.find('/configuration')

        directiveList = configurationTag.getiterator('directive')
        directives = []
        for configurationDirective in directiveList:
            directives.append(self.getDirective(configurationDirective))

        return directives

    def getDirective(self, configurationDirective):
        name = configurationDirective.find('name').text
        type = configurationDirective.find('type').text

        scope = "RSRC_CONF"

        if configurationDirective.find('scope') != None:
            scope = configurationDirective.find('scope').text
            
        valueList = configurationDirective.getiterator('value')
        values = []
        for value in valueList:
            values.append(value.text)
        
        return {'name'  : name,
                'type'  : type,
                'scope' : scope,
                'values': values}

class ApacheModuleHook:
    def __init__(self, descriptionTree):
        self.descriptionTree = descriptionTree

    def getHookList(self):
        hooksTag = self.descriptionTree.find('/hooks')

        if hooksTag != None:
            hookList = hooksTag.getiterator('hook')
            hooks = []
            for hook in hookList:
                hooks.append(self.getHook(hook))

            return hooks
        else:
            return []

    def getHook(self, hook):
        name = hook.find('name').text
        type = hook.find('type').text

        predecessor = "NULL"
        successor   = "NULL"
        position    = "MIDDLE"

        if hook.find('predecessor') != None:
            predecessor = hook.find('predecessor').text

        if hook.find('successor') != None:
            successor = hook.find('successor').text

        if hook.find('position') != None:
            position = hook.find('position').text

        return {'name':name,
                'type':type,
                'predecessor':predecessor,
                'successor':successor,
                'position':position}

if __name__ == "__main__":
    main()