from ast import Dict
import sys
import os
import xml.etree.ElementTree as ET

#버전 2024.08.14
#pubfallout88@gmail.com

def TXT2TXT_E1(txt_file, write_file_path):

    eng_string_array = []
    kor_string_array = []
    
    with open(txt_file, 'r', encoding='utf-8-sig') as file:
        count = 0
        step = 0
        empty_string = ''
        eng_string = ''
        kor_string = ''
        linecount = 0
        for line in file:
            input_string = line.strip()
            output_string = input_string;
            if step==0:
                eng_string = output_string;
            if step==1:
                kor_string = output_string;
            if step==2:
                empty_string = output_string;
                if len(empty_string)>0:
                    print(empty_string)
                    
            count=count + 1
            step = step + 1
            if step==3:
                step = 0
                eng_string_array.append(eng_string)
                kor_string_array.append(kor_string)

    write_file = open(write_file_path,"w+",encoding='utf-8-sig')

    for i in range(len(eng_string_array)):
        write_file.write("TeamWaldo")
        write_file.write('\n')
        write_file.write(eng_string_array[i])
        write_file.write('\n')
        write_file.write(kor_string_array[i])
        write_file.write('\n')
        write_file.write('\n')
    write_file.close()
        

def TXT2XMLString(txt_file, xml_file, out_xmlfile, multi):

    # 여기서부터는 텍스트 파일

    DictionaryList = {}
    
    with open(txt_file, 'r', encoding='utf-8-sig') as file:
        count = 0
        step = 0
        empty_string = ''
        tag_string = ''
        eng_string = ''
        kor_string = ''
        linecount = 0
        for line in file:
            input_string = line.strip()
            output_string = input_string;
            if step==0:
                tag_string = output_string;
            if step==1:
                eng_string = output_string;
            if step==2:
                kor_string = output_string;
            if step==3:
                empty_string = output_string;
                if len(empty_string)>0:
                    print(empty_string)
                    
            count=count + 1
            step = step + 1
            if step==4:
                step = 0
                eng_string = eng_string.replace("<CR><LF>","\n").strip()
                eng_string = eng_string.replace("<CR>","\x0D").replace("<LF>","\x0A").strip()
                kor_string = kor_string.replace("<CR>","\x0D").replace("<LF>","\x0A").strip()
                DictionaryList[eng_string] = kor_string

    # 여기서부터는 XML
    SourceList = []
    DestList = []
    
    with open(xml_file, 'rb') as file:
        raw_data = file.read()

    # 원본 XML 문자열로 변환
    xml_data = raw_data.decode('utf-8')
    # XML 파싱
    root = ET.fromstring(xml_data)
    #tree = ET.parse(xml_file)
    #root = tree.getroot()
    Params = root.find('Params')
    Params_Addon = Params.find('Addon').text
    Params_Source = Params.find('Source').text
    Params_Dest = Params.find('Dest').text
    Params_Version = Params.find('Version').text

    Content = root.find('Content')
    for item in Content.findall('String'):
        rec = item.find('REC').text
        Source = item.find('Source').text
        Dest = item.find('Dest').text
        SourceStrip = Source.strip()
        
        # 입력받은 텍스트 파일에서 String에서 텍스트 치환
        # 현재 폴런던 1.01 버전에서 REFR:FULL에 해당하는 지명을 번역하면 이동이 안되는 버그가 있어서 REFR:FULL은 제외시킴
        # 범용적으로 쓰려면 아래 조건문 제거 필요

        if rec!="REFR:FULL" and rec!="WRLD:FULL":
            if SourceStrip in DictionaryList:
                if multi==0:
                    Dest = DictionaryList[SourceStrip]
                else:
                    Dest = DictionaryList[SourceStrip] + " (" + SourceStrip + ")"
        
        SourceList.append(Source)
        DestList.append(Dest)


    for i in range(len(SourceList)):
        Source = SourceList[i]
        Source = Source.replace("&","[_and_]")
        Source = Source.replace("'","&apos;")
        Source = Source.replace("<","&lt;")
        Source = Source.replace(">","&gt;")
        Source = Source.replace("\"","&quot;")
        Source = Source.replace("[_and_]","&amp;")
        SourceList[i] = Source
        
        Dest = DestList[i]
        Dest = Dest.replace("&","[_and_]")
        Dest = Dest.replace("'","&apos;")
        Dest = Dest.replace("<","&lt;")
        Dest = Dest.replace(">","&gt;")
        Dest = Dest.replace("\"","&quot;")
        Dest = Dest.replace("[_and_]","&amp;")
        DestList[i] = Dest
        
    write_file = open(out_xmlfile,"w+",encoding='utf-8-sig')

    write_file.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<SSTXMLRessources>\n')
    write_file.write('  <Params>\n')
    write_file.write(f'    <Addon>{Params_Addon}</Addon>\n')
    write_file.write(f'    <Source>{Params_Source}</Source>\n')
    write_file.write(f'    <Dest>{Params_Dest}</Dest>\n')
    write_file.write(f'    <Version>{Params_Version}</Version>\n')
    write_file.write('  </Params>\n')
    write_file.write('  <Content>\n')
    
    index = 0
    for item in Content.findall('String'):
        Partial = item.get('Partial')
        List = item.get('List')
        edid = item.find('EDID').text
        rec = item.find('REC').text
        recid = item.find('REC').get('id')
        recidMax = item.find('REC').get('idMax')
        
        write_file.write('    <String')
        if List!=None:
            write_file.write(f' List="{List}"')
        if Partial!=None:
            write_file.write(f' Partial="{Partial}"')
        write_file.write('>\n')
        
        write_file.write(f'      <EDID>{edid}</EDID>\n')
        
        write_file.write(f'      <REC')
        if recid!=None:
            write_file.write(f' id="{recid}"')
        if recidMax!=None:
            write_file.write(f' idMax="{recidMax}"')
        write_file.write(f'>{rec}</REC>\n')
        
        write_file.write(f'      <Source>{SourceList[index]}</Source>\n')
        write_file.write(f'      <Dest>{DestList[index]}</Dest>\n')
        
        write_file.write('    </String>\n')
        index = index + 1
        
    write_file.write('  </Content>\n')
    write_file.write('</SSTXMLRessources>')
    write_file.close()
        


def CheckXMLFinal(xml_file,write_file_path):

    SourceList = []
    DestList = []
    
    tree = ET.parse(xml_file)
    root = tree.getroot()
    Params = root.find('Params')
    Params_Addon = Params.find('Addon').text
    Params_Source = Params.find('Source').text
    Params_Dest = Params.find('Dest').text
    Params_Version = Params.find('Version').text

    Content = root.find('Content')
    for item in Content.findall('String'):
        Source = item.find('Source').text
        Dest = item.find('Dest').text
        SourceList.append(Source)
        DestList.append(Dest)

    for i in range(len(SourceList)):
        Source = SourceList[i]
        Source = Source.replace("&","[_and_]")
        Source = Source.replace("'","&apos;")
        Source = Source.replace("<","&lt;")
        Source = Source.replace(">","&gt;")
        Source = Source.replace("\"","&quot;")
        Source = Source.replace("[_and_]","&amp;")
        SourceList[i] = Source
        
        Dest = DestList[i]
        Dest = Dest.replace("&","[_and_]")
        Dest = Dest.replace("'","&apos;")
        Dest = Dest.replace("<","&lt;")
        Dest = Dest.replace(">","&gt;")
        Dest = Dest.replace("\"","&quot;")
        Dest = Dest.replace("[_and_]","&amp;")
        DestList[i] = Dest
        
    index = 0
    
    write_file = open(write_file_path,"w+",encoding='utf-8-sig')
    
    for item in Content.findall('String'):
        Partial = item.get('Partial')
        List = item.get('List')
        edid = item.find('EDID').text
        rec = item.find('REC').text
        recid = item.find('REC').get('id')
        recidMax = item.find('REC').get('idMax')
  
        if SourceList[index]==DestList[index]:
            Text = SourceList[index].replace("\x0D", "<CR>").replace("\x0A", "<LF>")
            write_file.write(Text)
            write_file.write('\n')
        index = index + 1
    write_file.close()    

def XML2TextUnique(target,xml_file, out_txtfile):
    
    UniqueTextList = set()
    
    tree = ET.parse(xml_file)
    root = tree.getroot()
    Params = root.find('Params')
    Params_Addon = Params.find('Addon').text
    Params_Source = Params.find('Source').text
    Params_Dest = Params.find('Dest').text
    Params_Version = Params.find('Version').text

    Content = root.find('Content')
    for item in Content.findall('String'):
        if target==0:
            Text = item.find('Source').text
        else:
            Text = item.find('Dest').text
        
        Text = Text.replace("\x0D", "<CR>").replace("\x0A", "<LF>")

        if Text not in UniqueTextList:
            UniqueTextList.add(Text)
    
    write_file = open(out_txtfile,"w+",encoding='utf-8-sig')
    for item in UniqueTextList:
        write_file.write(item)
        write_file.write("\n")
        
    write_file.close()
    print(f"total {len(UniqueTextList)}")        



def TwoFile2OneFile(tag, eng_file_path, kor_file_path, write_file_path):
    
    eng_string_array = []
    kor_string_array = []
   
    if not os.path.exists(eng_file_path):
        print(f"{eng_file_path} is not exists.")
        return
    
    if not os.path.exists(kor_file_path):
        print(f"{kor_file_path} is not exists.")
        return
    
    with open(eng_file_path, 'r', encoding='utf-8-sig') as file:
        for line in file:
            input_string = line.strip()
            eng_string_array.append(input_string)

    with open(kor_file_path, 'r', encoding='utf-8-sig') as file:
        for line in file:
            input_string = line.strip()
            kor_string_array.append(input_string)
    
    if len(eng_string_array)!=len(kor_string_array):
        print("두개의 파일이 서로 라인수가 일치하지 않음")
        return
    
    write_file = open(write_file_path,"w+",encoding='utf-8-sig')

    for i in range(len(eng_string_array)):
        write_file.write(tag)
        write_file.write('\n')
        write_file.write(eng_string_array[i])
        write_file.write('\n')
        write_file.write(kor_string_array[i])
        write_file.write('\n')
        write_file.write('\n')
    write_file.close()
    
def Patch(file_path, replace_path, write_file_path):
    
    tag_string_array = []
    eng_string_array = []
    kor_string_array = []
    replace_tag_string_array = []
    replace_eng_string_array = []
    replace_kor_string_array = []
    
    count = 0
    
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        step = 0
        empty_string = ''
        tag_string = ''
        eng_string = ''
        kor_string = ''
        for line in file:
            input_string = line.strip()
            #input_string = input_string.replace('<LF>', '\x0A').replace('<CR>', '\x0D')
            output_string = input_string;

            if step==0:
                tag_string = output_string;
            if step==1:
                eng_string = output_string;
            if step==2:
                kor_string = output_string;
            if step==3:
                empty_string = output_string;
                if len(empty_string)>0:
                    print(empty_string)
            
            step = step + 1
            if step==4:
                step = 0
                tag_string_array.append(tag_string)
                eng_string_array.append(eng_string)
                kor_string_array.append(kor_string)
                count = count + 1
                #print(eng_string)  

    # 3줄까지 숫자/영어/한글/공백~
    with open(replace_path, 'r', encoding='utf-8-sig') as file:
        step = 0
        empty_string = ''
        tag_string = ''
        eng_string = ''
        kor_string = ''
        for line in file:
            input_string = line.strip()
            output_string = input_string;

            if step==0:
                tag_string = output_string;
            if step==1:
                eng_string = output_string;
            if step==2:
                kor_string = output_string;
            if step==3:
                empty_string = output_string;
                if len(empty_string)>0:
                    print(empty_string)
            
            step = step + 1
            if step==4:
                step = 0
                replace_tag_string_array.append(tag_string)
                replace_eng_string_array.append(eng_string)
                replace_kor_string_array.append(kor_string)
                count = count + 1
                #print(eng_string)  
    
    for i in range(len(replace_eng_string_array)):
       
        TargetIndex=-1
        ReplaceString = ''
        TagString = ''
        for n in range(len(eng_string_array)):
            if eng_string_array[n] == replace_eng_string_array[i]:
                TargetIndex = n;
                ReplaceString = replace_kor_string_array[i]
                TagString = replace_tag_string_array[i]
        
        if TargetIndex>=0:
            kor_string_array[TargetIndex]=ReplaceString
            tag_string_array[TargetIndex]=TagString
            print('patched')
            print(replace_eng_string_array[i])
            print(ReplaceString)
            print("\n")
        else:
            print('.')
                
    write_file = open(write_file_path,"w+",encoding='utf-8-sig')

    for i in range(len(eng_string_array)):
        write_file.write(tag_string_array[i])
        write_file.write('\n')
        write_file.write(eng_string_array[i])
        write_file.write('\n')
        write_file.write(kor_string_array[i])
        write_file.write('\n')
        write_file.write('\n')
    write_file.close()


def main():
    
    argument=''

    if len(sys.argv)>1:
        argument = sys.argv[1]
    
    if argument == '--extract_source':
        if len(sys.argv) < 4:
            print("Usage: python script.py <argument>")
            sys.exit(1)
        XML2TextUnique(0,sys.argv[2],sys.argv[3])
        
    elif argument == '--extract_dest':
        if len(sys.argv) < 4:
            print("Usage: python script.py <argument>")
            sys.exit(1)
        XML2TextUnique(1,sys.argv[2],sys.argv[3])
        
    elif argument == '--combine_tag_source_dest':
        if len(sys.argv) < 6:
            print("Usage: python script.py <argument>")
            sys.exit(1)
        TwoFile2OneFile(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])     
        
    elif argument == '--patch':
        if len(sys.argv) < 5:
            print("Usage: python script.py <argument>")
            sys.exit(1)
        Patch(sys.argv[2],sys.argv[3],sys.argv[4])     
        
    elif argument == '--replace_dest_string':
        if len(sys.argv) < 5:
            print("Usage: python script.py <argument>")
            sys.exit(1)
        TXT2XMLString(sys.argv[2],sys.argv[3],sys.argv[4],0)
        
    elif argument == '--replace_dest_string_multi':
        if len(sys.argv) < 5:
            print("Usage: python script.py <argument>")
            sys.exit(1)
        TXT2XMLString(sys.argv[2],sys.argv[3],sys.argv[4],1)
        
    elif argument == '--check_unchanged_string':
        if len(sys.argv) < 4:
            print("Usage: python script.py <argument>")
            sys.exit(1)
        CheckXMLFinal(sys.argv[2],sys.argv[3])            
    else:

        #XML2TextUnique(0,"LondonWorldSpace_1.01_org_en_en.xml","out.txt")
        #TwoFile2OneFile("DeepL","번역기용문장.txt","번역된문장.txt","메인텍스트.txt")
        
        TXT2XMLString("메인소스_팀왈도폴아웃4.txt", "LondonWorldSpace_1.01_org.xml", "LondonWorldSpace_1.01_org_out.xml", 0)
        TXT2XMLString("메인소스_폴런던기계번역문장.txt", "LondonWorldSpace_1.01_org_out.xml", "LondonWorldSpace_1.01_org_xTranslator입력용.xml", 1)
        
        #Patch("메인소스_폴런던기계번역문장.txt","메인소스_손번역패치.txt","메인소스_폴런던기계번역문장2.txt")
        #CheckXMLFinal("LondonWorldSpace_1.01_org_xTranslator입력용.xml","번역안하는스트링(확인용).txt")

        #TXT2XMLString("메인소스_폴런던기계번역문장0801004 - 테스트용.txt", "LondonWorldSpace_1.01_org_en_en_out_테스트용.xml", "LondonWorldSpace_1.01_org_en_en_out_테스트용2.xml", 1)

    
if __name__ == "__main__":
    main()
  
