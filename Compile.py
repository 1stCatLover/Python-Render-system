import os

base_folder = "Python-Render-system-MultiFile"
FileList = []
FullScript = ""
imports = []
from_imports = []
ChangeImport = []
Test = []
DefsToChange = []
for current_path, folder_names, file_names in os.walk(base_folder): #go through all subfolderws
    for file in file_names: #go through each file
        if file.endswith(".py"): #find file that is python file
            full_path = os.path.join(current_path, file)
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
            found_import = False
            ChangeImportOld = []
            ChangeImportNew = []
            FullScript += f"class {file[:-3]}:\n"
            new_lines = []
            VarsToChange = []

            for line in lines:
                stripped = line.strip()
                RStrip = line.rstrip()
                if stripped.startswith("import "):
                    parts = stripped.replace("import", "").strip().split(",")
                    for i in parts:
                        i = i.strip()
                        if i and i not in imports:
                            sp2 = i.split("as")
                            if len(sp2) > 1:
                                if sp2[0] not in ChangeImport:
                                    ChangeImport.append([sp2[0],sp2[1]])
                                else:
                                    ChangeImportOld.append(sp2[1])
                                    ChangeImportNew.append(sp2[0])
                                ChangeImportOld.append(sp2[1])
                                ChangeImportNew.append(f"{sp2[0]}.{sp2[1]}")
                            else:
                                imports.append(i)
                    found_import = True
                elif stripped.startswith("from "):
                    parts = stripped.split()
                    if len(parts) > 1:
                        module = parts[1]
                        if module not in from_imports:
                            from_imports.append(module)
                    found_import = True
                elif stripped.startswith("global "):
                    found_import = True
                else:
                    if stripped.startswith("def "):
                        defName = stripped.split("def ")[1].split("(")
                        if len(defName[1].split(")")) == (1 or 2):
                            defName = defName[0]
                            ChangeImportOld.append(defName)
                            ChangeImportNew.append(f"{file[:-3]}.{defName}")
                            DefsToChange.append([defName,f"{file[:-3]}.{defName}"])
                       
                    SpStr = RStrip.split("=")
                    if len(SpStr) == 2:
                        if SpStr[0][0] != " ":
                            if SpStr[0] not in VarsToChange:
                                VarsToChange.append(SpStr[0].replace(" ",""))

                    new_lines.append(RStrip)
            for i in ChangeImportNew:
                i = i.replace(" ","")
            for i in new_lines:
                end = i
                for Change in VarsToChange:
                    if end.startswith(" "):
                        end = end.replace(Change, f"{file[:-3]}.{Change}")
                        #end = end.replace(Change, f"{file[:-3]}.{Change}")
                   
                for Numb in range(len(ChangeImportOld)):
                    if len(end.split("def ")) == 1:
                        sp = end.split(ChangeImportOld[Numb])[0]
                        if len(sp) > 0:
                            if sp[-1] == " ":
                                end = end.replace(ChangeImportOld[Numb]," "+ChangeImportNew[Numb])
                        else:
                            end = end.replace(ChangeImportOld[Numb]," "+ChangeImportNew[Numb])
                FullScript += f"\n    {end}"
            FullScript += "\n\n"
            end = end.replace(" .", ".")
            end = end.replace(". ", ".")
            if found_import:
                FileList.append(os.path.splitext(os.path.basename(full_path))[0])


MainScript = "import "
HandleLater = []
for i in imports[:]:
    Split = i.split("as")
    if len(Split) > 1:
        imports.remove(i)
        HandleLater.append(i)
for i in imports:
    MainScript +=  i+", "
MainScript = MainScript[:-2]
FullScript = f"{MainScript}\n{FullScript}"
List = []
for i in DefsToChange:
    i[0] = i[0].replace(" ","")
    i[1] = i[1].replace(" ","")
for Line in FullScript.splitlines():
    for i in DefsToChange:
        split = Line.split(i[0])
        if len(split) > 0:
            if split[-1] == " ":
                Line = Line.replace(i[0],i[1])
    for i in ChangeImport:
        split = Line.split(i[0])
        if len(split) > 0:
            if split[-1] == " ":
                Line = Line.replace(i[0],i[1])
    List.append(Line)
with open("output.py", "w", encoding="utf-8") as f:
    f.write(FullScript)
print("EEEEEEEEEEEE")
print(VarsToChange)
print(ChangeImportNew,ChangeImportOld)
print(DefsToChange)

