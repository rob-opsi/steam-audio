#
# Copyright (c) Valve Corporation. All rights reserved.
#

import argparse
import os
import sys
import shutil
import zipfile


###############################################################################
# HELPER FUNCTIONS
###############################################################################


#
# Helper function to copy files from src to dst.
#
def copy(src, dst):
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    shutil.copyfile(src, dst)


#
# Deploys the Steam Audio Unity integration.
#
def deploy_integration_unity(configuration):
    print "Deploying: Steam Audio Unity Integration"

    deploy_path = os.path.abspath(os.path.join(os.getcwd(), "products"))

    os.makedirs(deploy_path + "\\steamaudio_unity")
    os.makedirs(deploy_path + "\\steamaudio_unity\\bin")
    os.makedirs(deploy_path + "\\steamaudio_unity\\bin\\unity")
    os.makedirs(deploy_path + "\\steamaudio_unity\\doc")

    copy(os.path.join(deploy_path, "..\\..\\bin\\SteamAudio.unitypackage"),
         deploy_path + "\\steamaudio_unity\\bin\\unity")
    copy(os.path.join(deploy_path, "..\\..\\doc\\phonon_unity.html"),
         deploy_path + "\\steamaudio_unity\\doc")

    zip_output = os.path.abspath(os.path.join(deploy_path, "steamaudio_unity.zip"))

    deploy_directory = os.getcwd()
    products_directory = deploy_directory + "\\products"
    os.chdir(products_directory)
    with zipfile.ZipFile(zip_output, "w", zipfile.ZIP_DEFLATED) as unity_zip:
        for directory, subdirectories, files in os.walk("steamaudio_unity"):
            for file in files:
                file_name = os.path.join(directory, file)
                print "Adding " + file_name + "..."
                unity_zip.write(file_name)
    os.chdir(deploy_directory)


#
# Main deployment routine: deploys all products.
#
def deploy(configuration):
    print "Deploying: Steam Audio using " + configuration + " configuration"

    deploy_path = os.path.abspath(os.path.join(os.getcwd(), "products"))

    if os.path.exists(deploy_path):
        shutil.rmtree(deploy_path)

    os.makedirs(deploy_path)

    try:
        deploy_integration_unity(configuration)
    except Exception as e:
        print "Exception encountered during deployment."
        print e
        sys.exit(1)


###############################################################################
# MAIN SCRIPT
###############################################################################


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configuration", help="Build configuration.", choices=["debug", "development", "release"],
                    type=str.lower)
args = parser.parse_args()

deploy(args.configuration)
