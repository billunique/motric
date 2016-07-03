function addDevice() {
	var tb = document.getElementById("device_table");

	var row = tb.insertRow(-1);
	var model = row.insertCell(0);
	var os = row.insertCell(1);
	var quan = row.insertCell(2);
	var abrow = row.rowIndex;

	var imodel = document.createElement("INPUT");
	imodel.setAttribute("type", "text");
	imodel.setAttribute("class", "mtinput form-control");
	imodel.setAttribute("id", "device" + abrow);
	imodel.setAttribute("name", "device");
	model.appendChild(imodel);

	var ios = document.createElement("INPUT");
	ios.setAttribute("type", "text");
	ios.setAttribute("class", "mtinput form-control");
	ios.setAttribute("id", "os" + abrow);
	ios.setAttribute("name", "os");
	os.appendChild(ios);

	var inum = document.createElement("INPUT");
	inum.setAttribute("type", "number");
	inum.setAttribute("class", "mtinput form-control");
	inum.setAttribute("min", "1");
	inum.setAttribute("id", "quantity" + abrow);
	inum.setAttribute("name", "quantity");
	quan.appendChild(inum);

	// window.alert(imodel.getAttribute("id") +"\n" + ios.getAttribute("id") +"\n" + inum.getAttribute("id"));
}

function action_handler(value) {
	try {
		switch (value) {
			case 'REF': confirm("You're refusing the request from our adorable user, you sure?"); break;
			case 'APP': popup_po(); break;
			case 'AVA': popup_add_sn(); break;
			case 'ASS': popup_add_sn(); break;
			default: 
		}
	}
	catch(err) {
		alert(err.message);
	}
}

function popup_po() {
	document.getElementById("translayer").style.display="block";
	document.getElementById("popupwindow").style.display="block";
}

function popdown() {
	document.getElementById("popupwindow").style.display="none";
    document.getElementById("translayer").style.display="none";
}


function getFormData() {
	try {
		var frm = document.forms["moha-device-request"];
		// alert(frm.length);
		var text = "";
		var i;
		for (i = 0; i < frm.length; i++) {
			text += frm.elements[i].id + ":" + frm.elements[i].value + ", ";
		}
		text = "{" + text + "}";
		// alert(text);
		return text;
	}
	catch(err) {
		alert(err.message);
	}
}


// jQury functions start here.
$(document).ready(function(){
	// $.fn.editable.defaults.mode = 'inline';
	var token = $('input[name="csrfmiddlewaretoken"]').prop('value');
	$('#ex_rate').editable();
	$('#disposal a').editable({
		type: 'text',
		placement: 'left',
		// pk: function(){}
		url: '/edit_request/',
        ajaxOptions: {
           dataType: 'json', //assuming json response
           headers: { "X-CSRFToken": token }
        }, 
        data: { 'csrfmiddlewaretoken': token }, 
        success: function(response, newValue) {
    		if(!response.success) return response.msg;
		}
	});

	// $('#rate').tooltip({title:"Click me to edit the exchage rate in one place!!!", placement:"bottom"});  //Weired behavior: cause the table column auto-grow.
});