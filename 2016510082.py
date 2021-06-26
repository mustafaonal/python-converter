# -*- coding: utf-8 -*-
from lxml import etree #for xml validation
from io import StringIO
import xml.etree.ElementTree as ET #for convert xml to other file types
import sys #for command line arguments
import json #json file oparation
import codecs #for utf-8 file read
import xml.dom.minidom #only for prity print xml file

#there are 7 diffirent function to convert file one to another or xsd validation for xml
#this function take 2 paramaters, first one is source file, second one is destination file
#we convert data source file to destination file properly

def Csv_To_Xml(inpFile, outFile):
    #in this function convert csv file to xml, traditional file write
    outputFile = open(outFile, "w+") #open destination file
    #write root---------
    outputFile.write("<"); 
    outputFile.write(inpFile[:len(inpFile)-4].lower()) #take input file name, except extension part
    outputFile.write(">\n")

    with open(inpFile, "r") as inputFile: #open input file for reading data
        line = inputFile.readline() #pass first line, because it's header and we already knows names
        count = 0 #this is just for not pass first line
        university_name = ""
        while True:
            count += 1
            line = inputFile.readline() #new line in every loop
            
            if not line: #if eof break to loop
                break
            if count > 1: #if it's not first line, keep university name to compare
                university_name = split_line[1] #bir önceki satırın üniversite adını tutuyor
            split_line = line.split(';') #split data
            if(university_name != split_line[1]): #if it's different from previous data, it's new university
                if count > 1: #close previous university tag
                    outputFile.write("      </university>\n")
                outputFile.write("      <university name=\"") #open new one
                outputFile.write(split_line[1])
                outputFile.write("\" uType=\"")
                outputFile.write(split_line[0])
                outputFile.write("\">\n")
            outputFile.write("            <item id=\"")
            outputFile.write(split_line[3])
            outputFile.write("\" faculty=\"")
            outputFile.write(split_line[2])
            outputFile.write("\">\n                  <name lang=\"")
            if split_line[5] == "İngilizce":
                outputFile.write("en\" second=\"")
            else:
                outputFile.write("tr\" second=\"")
            if split_line[6] == "İkinci Öğretim":
                outputFile.write("Yes\">")
            else:
                outputFile.write("No\">")
            outputFile.write(split_line[4])
            outputFile.write("</name>\n                  <period>")
            outputFile.write(split_line[8])
            outputFile.write("</period>\n                  <quota spec=\"")
            if split_line[11] == "":
                outputFile.write("")
            else:
                outputFile.write(split_line[11])
            outputFile.write("\">")
            outputFile.write(split_line[10])
            outputFile.write("</quota>\n                  <field>")
            outputFile.write(split_line[9])
            outputFile.write("</field>\n                  <last_min_score order=\"")
            outputFile.write(split_line[12])
            #last_min_score is last data in line and /r/n characters inside in last_min_score, to pass that characters, use [:len(split_line[13])-2] code
            if split_line[13][:len(split_line[13])-2] == "" or split_line[13][:len(split_line[13])-2] == "-": #if it's '-' character, it's must be empty
                outputFile.write("\"/>\n")
            else:
                outputFile.write("\">")
                outputFile.write(split_line[13][:len(split_line[13])-2])
                outputFile.write("</last_min_score>\n")
            if split_line[7] == "":
                outputFile.write("                  <grant/>\n")
            else:
                outputFile.write("                  <grant>")
                outputFile.write(split_line[7])
                outputFile.write("</grant>\n")
            outputFile.write("            </item>")
            outputFile.write("\n");
    outputFile.write("      </university>\n")
    outputFile.write("</")
    outputFile.write(inpFile[:len(inpFile)-4].lower())
    outputFile.write(">")
    outputFile.close()

def Xml_To_Csv(inpFile, outFile):
    outputFile = open(outFile, "w+") #open destination file
    outputFile.write("ÜNİVERSİTE_TÜRÜ;ÜNİVERSİTE;FAKÜLTE;PROGRAM_KODU;PROGRAM;DİL;ÖĞRENİM_TÜRÜ;BURS;ÖĞRENİM_SÜRESİ;PUAN_TÜRÜ;KONTENJAN;OKUL_BİRİNCİSİ_KONTENJANI;GEÇEN_YIL_MİN_SIRALAMA;GEÇEN_YIL_MİN_PUAN\n") #first line, header line

    with open(inpFile, "r") as inputFile: #open source file
        tree = ET.parse(inputFile) #parse xml file
        root = tree.getroot()
        for university in root: #it's turn every university change
            for item in university: #it's turn every department change
                outputFile.write(university.get('uType').encode('utf-8'))
                outputFile.write(";")
                outputFile.write(university.get('name').encode('utf-8'))
                outputFile.write(";")
                outputFile.write(item.get('faculty').encode('utf-8'))
                outputFile.write(";")
                outputFile.write(item.get('id'))
                outputFile.write(";")
                outputFile.write(item.find('name').text.encode('utf-8'))
                outputFile.write(";")
                if item.find('name').get('lang') == "en":
                    outputFile.write("İngilizce;")
                else:
                    outputFile.write(";")
                if item.find('name').get('second') == "No":
                    outputFile.write(";")
                else:
                    outputFile.write("İkinci Öğretim;")
                if item.find('grant').text == None:
                    outputFile.write(";")
                else:
                    outputFile.write(item.find('grant').text)
                    outputFile.write(";")
                outputFile.write(item.find('period').text)
                outputFile.write(";")
                outputFile.write(item.find('field').text)
                outputFile.write(";")
                outputFile.write(item.find('quota').text)
                outputFile.write(";")
                if item.find('quota').get('spec') == "":
                    outputFile.write(";")
                else:
                    outputFile.write(item.find('quota').get('spec'))
                    outputFile.write(";")
                if item.find('last_min_score').get('order') == "":
                    outputFile.write(";")
                else:
                    outputFile.write(item.find('last_min_score').get('order'))
                    outputFile.write(";")
                if item.find('last_min_score').text != None:
                    outputFile.write(item.find('last_min_score').text)
                outputFile.write("\n")

def Xml_To_JSON(inpFile, outFile):
    with open(inpFile, "r") as inputFile:
        tree = ET.parse(inputFile) #parse xml file
        root = tree.getroot() #get root
        name = ""
        data = [] #store everything in there, create empty object
        count = 0 #counter for data array(university counter)
        for university in root: #turn every university change
            ++count
            count2 = 0 #faculty counter at the same university
            faculty = ""
            name = university.get('name')
            uType = university.get('uType')
            data2 = { #create university elements
                "university name": name,
                "uType": uType,
                "items": [],
            }
            data.append(data2) #append university
            for item in university: #turn every department
                if(faculty != item.get('faculty')): #if there is different faculties in
                    faculty = item.get('faculty')   #same university
                    data[count-1]["items"].append({"faculty": faculty,
                    "department": []
                    })
                    ++count2
                #take every necessary data from file and append to data object
                faculty = item.get('faculty')
                data[count-1]["items"][count2-1]["department"].append({
                    "id": item.get('id'),
                    "name": item.find('name').text,
                    "lang": item.find('name').get('lang'),
                    "second": item.find('name').get('second'),
                    "period": item.find('period').text,
                    "spec": item.find('quota').get('spec'),
                    "quota": item.find('quota').text,
                    "field": item.find('field').text,
                    "last_min_score": item.find('last_min_score').text,
                    "last_min_order": item.find('last_min_score').get('order'),
                    "grant": item.find('grant').text,
                    })

    json_object = json.dumps(data, indent = 2, ensure_ascii=False,  sort_keys=True).encode('utf8') #convert json format data, utf-8 and sort key(alphabetical sort) open
    with open(outFile, 'w+') as outputFile: #open destination file and write
        outputFile.write(json_object)       #all data are true but ranking different from
                                            #source file

def JSON_To_Xml(inpFile, outFile): #this time I use etree library for write xml file
    outputFile = open(outFile, "wr+")
    with codecs.open(inpFile, "r", "utf-8") as inputFile: #codecs provide read utf-8 characters, I couldn't handle this file like others
        data = json.load(inputFile) #all data is here
        count = 0 #counter for university
        departments = ET.Element('departments')
        for p in data: #turn every university
            #create university object and store every data in there
            #create with etree library
            university = ET.SubElement(departments, 'university')
            university.set('name', data[count]["university name"])
            university.set('uType', data[count]["uType"])
            count2 = 0 #counter for item
            for a in data[count]["items"]: #turn every item
                faculty = data[count]["items"][count2]["faculty"]
                count3 = 0 # for department array
                for b in data[count]["items"][count2]["department"]: #turn every department
                    item = ET.SubElement(university, 'item')
                    item.set('id', data[count]["items"][count2]["department"][count3]["id"])
                    item.set('faculty', faculty)
                    name = ET.SubElement(item, 'name')
                    name.set('lang', data[count]["items"][count2]["department"][count3]["lang"])
                    name.set('second', data[count]["items"][count2]["department"][count3]["second"])
                    name.text = data[count]["items"][count2]["department"][count3]["name"]
                    period = ET.SubElement(item, 'period')
                    period.text = data[count]["items"][count2]["department"][count3]["period"]
                    quota = ET.SubElement(item, 'quota')
                    quota.set('spec', data[count]["items"][count2]["department"][count3]["spec"])
                    quota.text = data[count]["items"][count2]["department"][count3]["quota"]
                    field = ET.SubElement(item, 'field')
                    field.text = data[count]["items"][count2]["department"][count3]["field"]
                    last_min_score = ET.SubElement(item, 'last_min_score')
                    last_min_score.set('order', data[count]["items"][count2]["department"][count3]["last_min_order"])
                    last_min_score.text = data[count]["items"][count2]["department"][count3]["last_min_score"]
                    grant = ET.SubElement(item, 'grant')
                    grant.text = data[count]["items"][count2]["department"][count3]["grant"]
                    count3=count3+1
                count2=count2+1
            count=count+1
    ET.ElementTree(departments).write(outputFile,encoding="UTF-8",xml_declaration=True)
    outputFile.seek(0,0) #this code write all data in xml file without pretty print
    #bundan sonrası kısım pretty print için, opsiyonel, bu kısım olmadanda kod
    #çalışabilir ama pretty print olmadığı için okuması zor olur
    #xml.dom.minidom library used for pretty print
    pretty_parse = xml.dom.minidom.parse(outputFile)
    xml_pretty_str = pretty_parse.toprettyxml() #pretty print data stored in there
    outputFile.seek(0,0) #dosyanın başına gidiyor pretty olmayan tüm datayı silmek için
    outputFile.truncate(0) #her şeyi siliyor
    outputFile.seek(0,0) #tekrar dosyanın başına gidiyor
    outputFile.write(xml_pretty_str.encode("utf-8")) #pretty print data yı dosyaya yazıyor
    outputFile.close()

def JSON_To_Csv(inpFile, outFile):
    outputFile = open(outFile, "w+")
    outputFile.write("ÜNİVERSİTE_TÜRÜ;ÜNİVERSİTE;FAKÜLTE;PROGRAM_KODU;PROGRAM;DİL;ÖĞRENİM_TÜRÜ;BURS;ÖĞRENİM_SÜRESİ;PUAN_TÜRÜ;KONTENJAN;OKUL_BİRİNCİSİ_KONTENJANI;GEÇEN_YIL_MİN_SIRALAMA;GEÇEN_YIL_MİN_PUAN\n")
    with codecs.open(inpFile, 'r', "utf-8") as inputFile:
        data = json.load(inputFile)
        count = 0
        for p in data:
            count2 = 0
            university = data[count]["university name"]
            uType = data[count]["uType"]
            for a in data[count]["items"]:
                faculty = data[count]["items"][count2]["faculty"]
                count3 = 0
                for b in data[count]["items"][count2]["department"]:
                    id = data[count]["items"][count2]["department"][count3]["id"]
                    name = data[count]["items"][count2]["department"][count3]["name"]
                    lang = data[count]["items"][count2]["department"][count3]["lang"]
                    second = data[count]["items"][count2]["department"][count3]["second"]
                    period = data[count]["items"][count2]["department"][count3]["period"]
                    spec = data[count]["items"][count2]["department"][count3]["spec"]
                    quota = data[count]["items"][count2]["department"][count3]["quota"]
                    field = data[count]["items"][count2]["department"][count3]["field"]
                    last_min_score = data[count]["items"][count2]["department"][count3]["last_min_score"]
                    last_min_order = data[count]["items"][count2]["department"][count3]["last_min_order"]
                    grant = data[count]["items"][count2]["department"][count3]["grant"]

                    outputFile.write(uType.encode('utf-8'))
                    outputFile.write(";")
                    outputFile.write(university.encode('utf-8'))
                    outputFile.write(";")
                    outputFile.write(faculty.encode('utf-8'))
                    outputFile.write(";")
                    outputFile.write(id.encode('utf-8'))
                    outputFile.write(";")
                    outputFile.write(name.encode('utf-8'))
                    outputFile.write(";")
                    if(lang.encode('utf-8') == "en"):
                        outputFile.write("İngilizce")
                    outputFile.write(";")
                    if(second.encode('utf-8') == "Yes"):
                        outputFile.write("İkinci Öğretim")
                    outputFile.write(";")
                    if(grant != None):
                        outputFile.write(grant.encode('utf-8'))
                    outputFile.write(";")
                    outputFile.write(period.encode('utf-8'))
                    outputFile.write(";")
                    outputFile.write(field.encode('utf-8'))
                    outputFile.write(";")
                    outputFile.write(quota.encode('utf-8'))
                    outputFile.write(";")
                    if(spec != None):
                        outputFile.write(spec.encode('utf-8'))
                    outputFile.write(";")
                    if(last_min_order != None):
                        outputFile.write(last_min_order.encode('utf-8'))
                    outputFile.write(";")
                    if(last_min_score != None):
                        outputFile.write(last_min_score.encode('utf-8'))
                    outputFile.write("\n")
                    count3=count3+1
                count2=count2+1
            count=count+1

def Csv_To_JSON(inpFile, outFile):
    with open(inpFile, "r") as inputFile:
        line = inputFile.readline()
        count = 0
        university_name = ""
        data = []
        while True:
            line = inputFile.readline()
            if not line:
                break
            split_line = line.split(';')
            if(university_name != split_line[1]):
                faculty = split_line[2]
                count=count+1
                count2=0
                data2 = {
                    "university name": split_line[1],
                    "uType": split_line[0],
                    "items": [],
                    }
                data.append(data2)
                data[count-1]["items"].append({
                    "faculty": split_line[2],
                    "department": []
                    })
            if(faculty != split_line[2]):
                faculty = split_line[2]
                count2=count2+1
                data[count-1]["items"].append({
                    "faculty": split_line[2],
                    "department": []
                    })
            if(split_line[5] == "İngilizce"):
                language = "en"
            else:
                language = "tr"
            if(split_line[6] == "İkinci Öğretim"):
                second = "Yes"
            else:
                second = "No"
            if(split_line[11] == ""):
                spec = None
            else:
                spec = split_line[11]
            if(split_line[13][:len(split_line[13])-2] == "" or split_line[13][:len(split_line[13])-2] == "-"):
                last_min_score = None
            else:
                last_min_score = split_line[13][:len(split_line[13])-2]
            if(split_line[12] == ""):
                last_min_order = None
            else:
                last_min_order = split_line[12]
            data[count-1]["items"][count2-1]["department"].append({
                "id": split_line[3],
                "name": split_line[4],
                "lang": language,
                "second": second,
                "period": split_line[8],
                "spec": spec,
                "quota": split_line[10],
                "field": split_line[9],
                "last_min_score": last_min_score,
                "last_min_order": last_min_order,
                "grant": split_line[7],
                })
            
            university_name = split_line[1]

    json_object = json.dumps(data, indent = 2, ensure_ascii=False,  sort_keys=True) 
    with open(outFile, 'w+') as outputFile:
        outputFile.write(json_object)

def Xml_Validation(inpFile, Xsd_file):
    #xsd validation for xml file
    #open both file
    xml_file = open(inpFile, "r")
    xsd_file = open(Xsd_file, "r")
    doc = etree.parse(xml_file) #parse xml file
    root = doc.getroot() #get root
    #print(etree.tostring(root))
    xmlschema_doc = etree.parse(xsd_file) #parse xsd file
    xmlschema = etree.XMLSchema(xmlschema_doc)
    doc = etree.XML(etree.tostring(root))
    validation_result = xmlschema.validate(doc) #validation result store here, it's true or false
    print(validation_result)
    xmlschema.assert_(doc)
    xml_file .close()
    xsd_file.close()

if(sys.argv[3] == "1"):
    Csv_To_Xml(sys.argv[1], sys.argv[2])
elif(sys.argv[3] == "2"):
    Xml_To_Csv(sys.argv[1], sys.argv[2])
elif(sys.argv[3] == "3"):
    Xml_To_JSON(sys.argv[1], sys.argv[2])
elif(sys.argv[3] == "4"):
    JSON_To_Xml(sys.argv[1], sys.argv[2])
elif(sys.argv[3] == "5"):
    Csv_To_JSON(sys.argv[1], sys.argv[2])
elif(sys.argv[3] == "6"):
    JSON_To_Csv(sys.argv[1], sys.argv[2])
elif(sys.argv[3] == "7"):
    Xml_Validation(sys.argv[1], sys.argv[2])
