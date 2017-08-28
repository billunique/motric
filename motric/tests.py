from django.test import TestCase
from django.shortcuts import render
from motric.models import *
from django.db.models.functions import TruncMonth, ExtractMonth, ExtractYear
from django.db.models import Sum, Count
from collections import Counter

# Create your tests here.

import gviz_api

page_template = """
<html>
  <script src="https://www.google.com/jsapi" type="text/javascript"></script>
  <script>
    google.load('visualization', '1', {packages:['table']});

    google.setOnLoadCallback(drawTable);
    function drawTable() {
      %(jscode)s
      var jscode_table = new google.visualization.Table(document.getElementById('table_div_jscode'));
      jscode_table.draw(jscode_data, {showRowNumber: true});

      var json_table = new google.visualization.Table(document.getElementById('table_div_json'));
      var json_data = new google.visualization.DataTable(%(json)s, 0.6);
      json_table.draw(json_data, {showRowNumber: true});
    }
  </script>
  <body>
    <H1>Table created using ToJSCode</H1>
    <div id="table_div_jscode"></div>
    <H1>Table created using ToJSon</H1>
    <div id="table_div_json"></div>
  </body>
</html>
"""

def main():
  # Creating the data
  description = {"name": ("string", "Name"),
                 "salary": ("number", "Salary"),
                 "full_time": ("boolean", "Full Time Employee")}
  data = [{"name": "Mike", "salary": (10000, "$10,000"), "full_time": True},
          {"name": "Jim", "salary": (800, "$800"), "full_time": False},
          {"name": "Alice", "salary": (12500, "$12,500"), "full_time": True},
          {"name": "Bob", "salary": (7000, "$7,000"), "full_time": True}]

  # Loading it into gviz_api.DataTable
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)

  # Create a JavaScript code string.
  jscode = data_table.ToJSCode("jscode_data",
                               columns_order=("name", "salary", "full_time"),
                               order_by="salary")
  # Create a JSON string.
  json = data_table.ToJSon(columns_order=("name", "salary", "full_time"),
                           order_by="salary")

  # Put the JS code and JSON string into the template.
  print "Content-type: text/html"
  print
  print page_template % vars()

def main2():

	description = {"name": ("string", "Name"),
	               "salary": ("number", "Salary"),
	               "full_time": ("boolean", "Full Time Employee")}
	data = [{"name": "Mike", "salary": (10000, "$10,000"), "full_time": True},
	        {"name": "Jim", "salary": (800, "$800"), "full_time": False},
	        {"name": "Alice", "salary": (12500, "$12,500"), "full_time": True},
	        {"name": "Bob", "salary": (7000, "$7,000"), "full_time": True}]

	data_table = gviz_api.DataTable(description)
	data_table.LoadData(data)
	print "Content-type: text/plain"
	print
	print data_table.ToJSonResponse(columns_order=("name", "salary", "full_time"),
	                                order_by="salary")


if __name__ == '__main__':
  main2()

def dash(request):
	# Creating the data
	description1 = {"name": ("string", "Name"),
	               "salary": ("number", "Salary"),
	               "full_time": ("boolean", "Full Time Employee")}
	data1 = [{"name": "Mike", "salary": (10000, "$10,000"), "full_time": True},
	        {"name": "Jim", "salary": (800, "$800"), "full_time": False},
	        {"name": "Alice", "salary": (12500, "$12,500"), "full_time": True},
	        {"name": "Bob", "salary": (7000, "$7,000"), "full_time": True}]


	rds = RequestedDevice.objects.filter(resolved__in=[0,1])
	mset = rds.values_list('model_type').annotate(qty=Sum('quantity')).order_by('-qty')

	description_model = [("model_type", "string", "Model"),
				         ("qty", "number", "Quantity")]
	data_model = list(mset)


	# Loading it into gviz_api.DataTable
	data_table = gviz_api.DataTable(description_model)
	data_table.LoadData(data_model)

	# Create a JavaScript code string.
	jscode = data_table.ToJSCode("jscode_data",
	                             columns_order=("model_type", "qty"), order_by="-qty")
	# Create a JSON string.
	json_model = data_table.ToJSon(columns_order=("model_type", "qty"), order_by="-qty")


	rset = rds.annotate(month=ExtractMonth('request_date'), year=ExtractYear('request_date')).values_list('year', 'month').annotate(request=Count('id'), device=Sum('quantity')).values_list('year', 'month', 'request', 'device')
	data_request = [(str(e[0]) + "/" + str(e[1]), e[2], e[3]) for e in rset]
	description_request = [("month", "string", "Month"),
						   ("request_times", "number", "Request times"),
						   ("request_device_quantity", "number", "Requested Device Quantity")]

	data_table_r = gviz_api.DataTable(description_request)
	data_table_r.LoadData(data_request)
	json_request = data_table_r.ToJSon(columns_order=("month", "request_times", "request_device_quantity"), order_by="month")


	return render(request, 'motric_test.html', {'jscode':jscode, 'json_model':json_model, 'json_request':json_request})