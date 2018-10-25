from flask_table import Table, Col

class Results(Table):
manufacturer = Col('manufacturer'),
modelNumber  = Col('modelNumber'),
description  = Col('description'),
weight       = Col('weight')
