import sys, os

extensions = []
templates_path = []
source_suffix = ".rst"
master_doc = "index"
project = u"anafero"
package = "anafero"
copyright = u"2013, Eldarion"
exclude_patterns = ["_build"]
pygments_style = "sphinx"
html_theme = "default"
html_static_path = []
htmlhelp_basename = "anaferodoc"
latex_documents = [
  ("index", "anafero.tex", u"anafero Documentation",
   u"Eldarion", "manual"),
]
man_pages = [
    ("index", "anafero", u"anafero Documentation",
     [u"Eldarion"], 1)
]

sys.path.insert(0, os.pardir)
m = __import__(package)

version = m.__version__
release = version
