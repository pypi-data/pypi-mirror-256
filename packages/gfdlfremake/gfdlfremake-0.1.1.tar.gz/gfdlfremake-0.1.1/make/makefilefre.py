import os

class makefile():
## \brief Opens Makefile and sets the experiment and other common variables
## \param self The Makefile object
## \param exp Experiment name
## \param srcDir The path to the source directory
## \param bldDir The path to the build directory
## \param mkTemplate The path of the template .mk file for compiling
 def __init__(self,exp,srcDir,bldDir,mkTemplate):
     self.e = exp
     self.src = srcDir 
     self.bld =  bldDir
     self.template = mkTemplate
     self.c =[] #components
     self.r=[] #requires
     self.o=[] #overrides
     os.system("mkdir -p "+self.bld)
     self.filePath = self.bld # Needed so that the container and bare metal builds can
                              # use the same function to create the Makefile
## \brief Adds a component and corresponding requires to the list
## \param self The Makefile object
## \param c The component
## \param r The requires for that componenet
## \param o The overrides for that component
 def addComponent (self,c,r,o):
     self.c.append(c)
     self.r.append(r)
     self.o.append(o)
## \brief Sorts the component by how many requires there are for that component
## \param self The Makefile object
## \param c The component
## \param r The requires for that component
## \param o The overrides for that component
 def createLibstring (self,c,r,o):
     d=zip(self.c,self.r,self.o)
     return(sorted(d,key=lambda values:len(values[1]),reverse=True))
## \brief Writes the Makefile.  Should be called after all components are added
## \param self The Makefile object
 def writeMakefile (self):
# Get the list of all of the libraries
     sd=self.createLibstring(self.c,self.r,self.o)
     libstring=" "
     for i in sd:      
       lib=i[0]        
       libstring = libstring+lib+"/lib"+lib+".a "   
# Open the Makefile for Writing
     with open(self.filePath+"/Makefile","w") as fh:
# Write the header information for the Makefile
       fh.write("# Makefile for "+self.e+"\n")
       fh.write("SRCROOT = "+self.src+"/\n")
       fh.write("BUILDROOT = "+self.bld+"/\n")
       fh.write("MK_TEMPLATE = "+self.template+"\n") 
       fh.write("include $(MK_TEMPLATE)"+"\n")
# Write the main experiment compile 
       fh.write(self.e+".x: "+libstring+"\n")
       fh.write("\t$(LD) $^ $(LDFLAGS) -o $@ $(STATIC_LIBS)"+"\n")
# Write the individual component library compiles
       for (c,r,o) in sd:
            libstring = " "
            for lib in r:
                 libstring = libstring+lib+"/lib"+lib+".a "
            cstring = c+"/lib"+c+".a: "
            fh.write(cstring+libstring+" FORCE"+"\n")
            if o == "":
                 fh.write("\t$(MAKE) SRCROOT=$(SRCROOT) BUILDROOT=$(BUILDROOT) MK_TEMPLATE=$(MK_TEMPLATE) --directory="+c+" $(@F)\n")
            else:
                 fh.write("\t$(MAKE) SRCROOT=$(SRCROOT) BUILDROOT=$(BUILDROOT) MK_TEMPLATE=$(MK_TEMPLATE) "+o+" --directory="+c+" $(@F)\n")
       fh.write("FORCE:\n")
       fh.write("\n")
# Set up the clean
       fh.write("clean:\n")
       for c in self.c:
            fh.write("\t$(MAKE) --directory="+c+" clean\n")
# Set up localize
       fh.write("localize:\n")
       for c in self.c:
            fh.write("\t$(MAKE) -f $(BUILDROOT)"+c+" localize\n")
# Set up distclean
       fh.write("distclean:\n")
       for c in self.c:
            fh.write("\t$(RM) -r "+c+"\n")
       fh.write("\t$(RM) -r "+self.e+"\n")
       fh.write("\t$(RM) -r Makefile \n")

### This seems incomplete? ~ ejs
## The makefile class for a container.  It gets built into a temporary directory so it can be copied
## into the container.
## \param exp Experiment name
## \param srcDir The path to the source directory
## \param bldDir The path to the build directory
## \param mkTemplate The path of the template .mk file for compiling
## \param tmpDir A local path to temporarily store files build to be copied to the container
class makefileContainer(makefile):
  def __init__(self,exp,srcDir,bldDir,mkTemplate,tmpDir):
    self.e = exp
    self.src = srcDir 
    self.bld =  bldDir
    self.template = mkTemplate
    self.tmpDir = tmpDir
    self.c =[] #components
    self.r=[] #requires
    self.o=[] #overrides
    os.system("mkdir -p "+self.tmpDir)
    self.filePath = self.tmpDir # Needed so that the container and bare metal builds can
                                # use the same function to create the Makefile
## \return the tmpDir
## \param self The makefile object
  def getTmpDir(self):
    return self.tmpDir
