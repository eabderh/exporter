
from .extend import Exporter

export = Exporter().top()
exp = export.duck
#export.val('exp', export.duck)


