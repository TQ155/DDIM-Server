from django.db import models

import os

def generate_path_process(instance, filename):
    return os.path.join(str(instance.printJob.id), str(instance.layerNumber), filename)

class UploadedFiles(models.Model):
    filename = models.CharField(max_length=40)
    filedescription = models.CharField(max_length=150)
    entityname = models.CharField(max_length=150)
    fileraw = models.FileField(upload_to = "dimm_static")
    uploadtime = models.DateTimeField(auto_now_add=True, blank=True)

class FileMetadata(models.Model):
    filename = models.ForeignKey('UploadedFiles', on_delete=models.CASCADE)
    columnname = models.CharField(max_length=150)

class CreateRule(models.Model):

    EQ = "equalto"
    CON = "contains"
    CONT = "contained"
    ISA = "ISA"
    HAS = "HAS"
    
    RELATIONSHIPTYPES = [
        (EQ, "equalto"),
        (CON, "contains"),
        (CONT, "contained"),
        (ISA, "ISA"),
        (HAS, "HAS")
    ]

    relationship = models.CharField(choices=RELATIONSHIPTYPES, default=EQ, max_length=10)
    filename1 = models.ForeignKey('UploadedFiles', on_delete=models.CASCADE, related_name="file1")
    joincolumnname1 = models.CharField(max_length=150)
    filename2 = models.ForeignKey('UploadedFiles', on_delete=models.CASCADE, related_name="file2")
    joincolumnname2 = models.CharField(max_length=150)
