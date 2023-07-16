

import csv
import shutil
from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
import os
import pandas as pd
import pymysql

from neo4j import GraphDatabase

from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from DDIM_Graph import settings

from .models import UploadedFiles
from .models import FileMetadata
from .models import CreateRule

from .serializers import UploadedFilesSerializer
from .serializers import FileMetadataSerializer
from .serializers import CreateRuleSerializer

class UploadedFilesList(APIView):

    def get(self, request, format=None):
        uploadedfiles = UploadedFiles.objects.all()
        serializer = UploadedFilesSerializer(uploadedfiles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
       
        serializer = UploadedFilesSerializer(data=request.data)
        if serializer.is_valid():
            uploadedfile = serializer.save()

            driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j01;"))

            #pathname = os.path.join("dimm_static",uploadedfile.fileraw.name)
            pathname = uploadedfile.fileraw.name
            print(pathname)
            pathpart = pathname.split("/")
            shutil.copyfile(pathname, "/Users/teaching/Library/Application Support/Neo4j Desktop/Application/relate-data/dbmss/dbms-b5bd5dd6-b4e2-4124-b020-060da8d42b4d/import/" + pathpart[1])

            

            neocommanda = "LOAD CSV WITH HEADERS FROM 'file:///" + pathpart[1] + "' AS line CREATE (:" + uploadedfile.entityname

            neocommandb = " {"
            with open(pathname) as csv_file:
                df = pd.read_csv(pathname) #TODO: is there a cleaner way
                list_of_column_names = list(df.columns)

                count = 0
                while count < len(list_of_column_names):
                    filemetadata = FileMetadata.objects.create(filename=uploadedfile, columnname=list_of_column_names[count])
                    filemetadata.save()

                    if count + 1 < len(list_of_column_names):
                        #neocommandb = neocommandb + list_of_column_names[count] + ": line[" + str(count) + "], "
                        neocommandb = neocommandb + list_of_column_names[count] + ": line." + list_of_column_names[count] + ","
                    else:
                        #neocommandb = neocommandb + list_of_column_names[count] + ": line[" + str(count) + "]})"
                        neocommandb = neocommandb + list_of_column_names[count] + ": line." + list_of_column_names[count] + "})"
                    count += 1
            try:
                neocommand = neocommanda + neocommandb
                print(neocommand)
                #driver = GraphDatabase.driver(settings.uri, auth=(settings.neouser, settings.neopassword))
                #session = driver.session(database=settings.dbname)
                session = driver.session(database="neo4j")
                response = list(session.run(neocommand)) 

            except Exception as e:
                print("Query failed:", e)
            finally: 
                if session is not None:
                    session.close()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UploadedFilesObj(APIView):       

    def get_object(self, pk):
        try:
            return UploadedFiles.objects.get(pk=pk)
        except UploadedFiles.DoesNotExist:
            raise Http404

    def get(self, request, pk, Format=None):
        uploadedfile = self.get_object(pk)
        serializer = UploadedFilesSerializer(uploadedfile)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        #TODO: Delete model, measurement with tag and assoicated files
        pass

class FileMetadataList(APIView):

    def get(self, request, format=None):
        filemetadata = FileMetadataSerializer.objects.all()
        serializer = FileMetadataSerializer(filemetadata, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileMetadataObj(APIView):       

    def get_object(self, pk):
        try:
            return FileMetadata.objects.get(pk=pk)
        except FileMetadata.DoesNotExist:
            raise Http404

    def get(self, request, pk, Format=None):
        filemetadata = self.get_object(pk)
        serializer = FileMetadataSerializer(filemetadata)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        #TODO: Delete model, measurement with tag and assoicated files
        pass

class CreateRuleList(APIView):    
    def get(self, request, format=None):
        createrule = CreateRule.objects.all()
        serializer = CreateRuleSerializer(createrule, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        serializer = CreateRuleSerializer(data=request.data)
        if serializer.is_valid():
            createrule = serializer.save()

            neocommand = ("MATCH (a:%s),(b:%s) WHERE a.%s = b.%s " % (
                createrule.filename1.entityname, 
                createrule.filename2.entityname,
                createrule.joincolumnname1,
                createrule.joincolumnname2
            ))

            if createrule.relationship == 'equalto':    
                neocommand =  neocommand + "CREATE (a)-[r:equalto]->(b)"
            elif createrule.relationship == 'contains':
                neocommand = neocommand + "CREATE (a)-[r:contains]->(b)"
            elif createrule.relationship == 'ISA':
                neocommand = neocommand + "CREATE (a)-[r:isa]->(b)"
            else:
                neocommand = neocommand + "CREATE (a)-[r:has]->(b)"
            
            neocommand = neocommand + " RETURN type(r)"
            print(neocommand)

            try:
                driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j01;"))
                session = driver.session(database="neo4j")
                #driver = GraphDatabase.driver(settings.neouri, auth=(settings.neouser, settings.neopassword))
                #session = driver.session(database=settings.neodbname)
                response = list(session.run(neocommand)) 
            except Exception as e:
                print("Query failed:", e)
            finally: 
                if session is not None:
                    session.close()

            driver.close()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateRuleObj(APIView):    
    
    def get_object(self, pk):
        try:
            return CreateRule.objects.get(pk=pk)
        except CreateRule.DoesNotExist:
            raise Http404

    def get(self, request, pk, Format=None):
        createrule = self.get_object(pk)
        serializer = CreateRuleSerializer(createrule)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        #TODO: Delete model, measurement with tag and assoicated files
        pass