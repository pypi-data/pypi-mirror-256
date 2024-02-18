#!/usr/bin/python3
## \date 2023
## \author Tom Robinson
## \email thomas.robinson@noaa.gov
## \description 

import os
import targetfre

class container():
## \brief Opens the Dockerfile for writing
## \param self The dockerfile object
## \param base the docker base image to start from
## \param exp The experiment name
## \param RUNenv The commands that have to be run at the beginning of a RUN in the dockerfile
## to set up the environment
 def __init__(self,base,exp,RUNenv,target):
     self.base=base
     self.e = exp
     self.src = "/apps/"+self.e+"/src"
     self.bld = "/apps/"+self.e+"/exec"
     self.mkmf = True
     self.target = target
     self.template = "/apps/mkmf/templates/hpcme-intel21.mk"
     if RUNenv == "":
           self.setup = ["RUN \\ \n"]
     else:
           self.setup = ["RUN "+RUNenv[0]+" \\ \n"]
     self.setup
     for env in RUNenv[1:]:
           self.setup.append(" && "+env+" \\ \n")
     self.mkmfclone=["RUN cd /apps \\ \n",
                    " && git clone --recursive https://github.com/NOAA-GFDL/mkmf \\ \n",
                    " && cp mkmf/bin/* /usr/local/bin \n"]
     self.bldsetup=["RUN bld_dir="+self.bld+" \\ \n", 
                    " && src_dir="+self.src+" \\ \n",
                    " && mkmf_template="+self.template+ " \\ \n"]
     self.d=open("Dockerfile","w")
     self.d.writelines("FROM "+self.base+" \n")
## \brief writes to the checkout part of the Dockerfile and sets up the compile
## \param self The dockerfile object
## \param cScriptName The name of the checkout script in the container
## \param cOnDisk The relative path to the checkout script on disk
 def writeDockerfileCheckout(self, cScriptName, cOnDisk):
     self.checkoutPath = "/apps/"+self.e+"/src/"+ cScriptName
     self.d.write("COPY " + cOnDisk +" "+ self.checkoutPath  +" \n")
     self.d.write("RUN chmod 744 /apps/"+self.e+"/src/checkout.sh \n")
     self.d.writelines(self.setup)
     self.d.write(" && /apps/"+self.e+"/src/checkout.sh \n")
# Clone mkmf
     self.d.writelines(self.mkmfclone)
## Copies the Makefile into the bldDir in the dockerfile
## \param self The dockerfile object
## \param makefileOnDiskPath The path to Makefile on the local disk 
 def writeDockerfileMakefile(self, makefileOnDiskPath):
     # Set up the bldDir
     self.bldCreate=["RUN mkdir -p "+self.bld+" \n",
                     "COPY "+ makefileOnDiskPath  +" "+self.bld+"/Makefile \n"]
     self.d.writelines(self.bldCreate)
## \brief Adds components to the build part of the Dockerfile
## \param self The dockerfile object
## \param c Component from the compile yaml
 def writeDockerfileMkmf(self, c):
# Set up the compile variables
     self.d.writelines(self.bldsetup)
# Shorthand for component
     comp = c["component"]
# Make the component directory
     self.d.write(" && mkdir -p $bld_dir/"+comp+" \\ \n")
# Get the paths needed for compiling
     pstring = ""
     for paths in c["paths"]:
          pstring = pstring+"$src_dir/"+paths+" "
# Run list_paths
     self.d.write(" && list_paths -l -o $bld_dir/"+comp+"/pathnames_"+comp+" "+pstring+" \\ \n")
     self.d.write(" && cd $bld_dir/"+comp+" \\ \n")
# Create the mkmf line
     if c["requires"] == [] and c["doF90Cpp"]: # If this lib doesnt have any code dependencies and it requires the preprocessor (no -o and yes --use-cpp)
          self.d.write(" && mkmf -m Makefile -a $src_dir -b $bld_dir -p lib"+comp+".a -t $mkmf_template --use-cpp -c \""+c["cppdefs"]+"\" "+c["otherFlags"]+" $bld_dir/"+comp+"/pathnames_"+comp+" \n")
     elif c["requires"] == []: # If this lib doesnt have any code dependencies (no -o)
          self.d.write(" && mkmf -m Makefile -a $src_dir -b $bld_dir -p lib"+comp+".a -t $mkmf_template -c \""+c["cppdefs"]+"\" "+c["otherFlags"]+" $bld_dir/"+comp+"/pathnames_"+comp+" \n")
     else: #Has requirements
#Set up the requirements as a string to inclue after the -o
          reqstring = ""
          for r in c["requires"]:
               reqstring = reqstring+"-I$bld_dir/"+r+" "
#Figure out if we need the preprocessor
          if c["doF90Cpp"]:
               self.d.write(" && mkmf -m Makefile -a $src_dir -b $bld_dir -p lib"+comp+".a -t $mkmf_template --use-cpp -c \""+c["cppdefs"]+"\" -o \""+reqstring+"\" "+c["otherFlags"]+" $bld_dir/"+comp+"/pathnames_"+comp+" \n")
          else:
               self.d.write(" && mkmf -m Makefile -a $src_dir -b $bld_dir -p lib"+comp+".a -t $mkmf_template -c \""+c["cppdefs"]+"\" -o \""+reqstring+"\" "+c["otherFlags"]+" $bld_dir/"+comp+"/pathnames_"+comp+" \n")
## Builds the container image for the model
## \param self The dockerfile object
 def build(self):
     self.d.writelines(self.setup)
     self.d.write(" && cd "+self.bld+" && make -j 4 "+self.target.getmakeline_add()+"\n")
     self.d.write('ENTRYPOINT ["/bin/bash"]')
     self.d.close()
     os.system("podman build -f Dockerfile -t "+self.e+":"+self.target.gettargetName())
     os.system("rm -f "+self.e+".tar "+self.e+".sif")
     os.system("podman save -o "+self.e+"-"+self.target.gettargetName()+".tar localhost/"+self.e+":"+self.target.gettargetName())
     os.system("apptainer build --disable-cache "+self.e+"-"+self.target.gettargetName()+".sif docker-archive://"+self.e+"-"+self.target.gettargetName()+".tar")
