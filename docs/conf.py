import pkg_resources

extensions = []
templates_path = []
source_suffix = ".rst"
master_doc = "index"
project = u"pinax-referrals"
package = "pinax.referrals"
copyright = u"2015, James Tauber and contributors"
exclude_patterns = ["_build"]
pygments_style = "sphinx"
html_theme = "default"
html_static_path = []
htmlhelp_basename = "pinaxreferralsdoc"
latex_documents = [(
    "index", "pinax-referrals.tex", u"pinax-referrals Documentation", u"Pinax", "manual"
)]
man_pages = [(
    "index", "pinax-referrals", u"pinax-referrals Documentation", [u"Pinax"], 1
)]

version = pkg_resources.get_distribution("pinax-blog").version
release = version
