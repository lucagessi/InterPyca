from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
import os 
import shutil

class Base:
    def __init__(self):
        self.pdir = Path(__file__).parent
        self.assets_dir = self.pdir / "assets"
        self.env = Environment(
            loader=FileSystemLoader(self.pdir / "assets"),
            autoescape=select_autoescape()
        )
    
    def __copy_files(self, src, dst):
        os.makedirs(dst, exist_ok=True)
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dst_path = os.path.join(dst, item)
            if os.path.isdir(src_path):
                self.__copy_files(src_path, dst_path)  # copia ricorsiva delle sottocartelle
            else:
                shutil.copy2(src_path, dst_path)

    def __copy_assets(self, outout_dir):
        # bootstrap
        self.__copy_files( os.path.join(self.assets_dir, "bootstrap"), os.path.join(outout_dir, "bootstrap") )

    def render(self, outout_dir = "output"):
        template = self.env.get_template("basic.html")
        d = Path(outout_dir)
        if not d.exists():
            d.mkdir(parents=True)
        # Copio assets
        self.__copy_assets( outout_dir )
        content = template.render( 
            title = "Prova",
            author = "Luca Gessi"
        )

        with open(os.path.join( outout_dir,"index.html" ), mode="w", encoding="utf-8") as message:
            message.write(content)