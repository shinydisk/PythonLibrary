
import npyscreen
import subprocess
import shutil

class NmapScannerForm(npyscreen.ActionForm):
    def create(self):
        self.add(npyscreen.FixedText, value="Interface Nmap CLI Interactive", editable=False)
        self.add(npyscreen.FixedText, value="-------------------------------", editable=False)
        self.target_type = self.add(npyscreen.TitleSelectOne, max_height=4, name="Type de cible", values=["IP unique", "Plage CIDR", "Fichier"], scroll_exit=True)
        self.target_value = self.add(npyscreen.TitleText, name="Cible:")

        self.add(npyscreen.FixedText, value="-------------------------------", editable=False)
        self.scan_options = self.add(npyscreen.TitleMultiSelect, max_height=8, name="Options de scan", 
                                     values=["Scan rapide (-F)", "Ports spécifiques (-p)", "Scan UDP (-sU)", 
                                             "Scan agressif (-A)", "Détection de version (-sV)", "Détection de l'OS (-O)"], scroll_exit=True)
        self.custom_ports = self.add(npyscreen.TitleText, name="Ports (si sélectionné):")

        self.add(npyscreen.FixedText, value="-------------------------------", editable=False)
        self.save_output = self.add(npyscreen.TitleSelectOne, max_height=3, name="Sauvegarder sortie ?", values=["Oui", "Non"], scroll_exit=True)
        self.filename = self.add(npyscreen.TitleText, name="Nom du fichier de sortie:")

    def on_ok(self):
        if shutil.which("nmap") is None:
            npyscreen.notify_confirm("Erreur : Nmap n'est pas installé sur ce système.", title="Erreur")
            return

        target = self.target_value.value
        scan_flags = []

        if self.scan_options.value:
            for index in self.scan_options.value:
                if index == 0:
                    scan_flags.append("-F")
                elif index == 1 and self.custom_ports.value:
                    scan_flags.append(f"-p {self.custom_ports.value}")
                elif index == 2:
                    scan_flags.append("-sU")
                elif index == 3:
                    scan_flags.append("-A")
                elif index == 4:
                    scan_flags.append("-sV")
                elif index == 5:
                    scan_flags.append("-O")

        command = ["nmap"] + scan_flags + [target]

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            output_text = result.stdout
            npyscreen.notify_wait(output_text[:3000], title="Résultat du scan (tronqué)")
        except subprocess.CalledProcessError as e:
            npyscreen.notify_confirm(f"Erreur d'exécution :\n{e}", title="Erreur")

        if self.save_output.value and self.save_output.value[0] == 0:
            filename = self.filename.value or "nmap_result.txt"
            with open(filename, "w") as f:
                f.write(output_text)
            npyscreen.notify_confirm(f"Résultat sauvegardé dans : {filename}", title="Fichier sauvegardé")

    def on_cancel(self):
        self.parentApp.setNextForm(None)

class NmapApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", NmapScannerForm)

if __name__ == '__main__':
    app = NmapApp()
    app.run()
