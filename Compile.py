import os

base_folder = "Python-Render-system-MultiFile"
FileList = []
FullScript = ""
imports = []
from_imports = []
class ChangeImport:
    Main = []
    New = []
Test = []
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
                                if sp2[0] not in ChangeImport.Main:
                                    ChangeImport.Main.append(sp2[0])
                                    ChangeImport.New.append(sp2[1])
                                else:
                                    ChangeImportOld.append(sp2[1])
                                    ChangeImportNew.append(sp2[0])
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
                else:
                    SpStr = RStrip.split("=")
                    if len(SpStr) == 2:
                        if len(SpStr[0].split("def")) == 1:
                            if SpStr[0][0] != " ":
                                VarsToChange.append(SpStr[0].replace(" ",""))
                    new_lines.append(RStrip)
            for i in new_lines:
                end = i
                for Change in VarsToChange:
                    # Skip if this is the declaration line itself
                    if not end.strip().startswith(f"{Change} =") and not end.strip().startswith(f"{Change}="):
                        end = end.replace(Change, f"{file[:-3]}.{Change}")
                for Numb in range(len(ChangeImportOld)):
                    end = end.replace(ChangeImportOld[Numb],ChangeImportNew[Numb])
                FullScript += f"\n    {end}"
            FullScript += "\n\n"
            if found_import:
                FileList.append(os.path.splitext(os.path.basename(full_path))[0])

print(FileList)
print(imports, from_imports)
MainScript = "import "
HandleLater = []
for i in imports[:]:
    Split = i.split("as")
    if len(Split) > 1:
        print("From file", i)
        imports.remove(i)
        HandleLater.append(i)
for i in imports:
    MainScript +=  i+", "
FullScript = FullScript[:-2]
print(MainScript)
print(HandleLater)
print(Test)
FullScript = f"{MainScript}\n{FullScript}"
with open("output.py", "w", encoding="utf-8") as f:
    f.write(FullScript)

