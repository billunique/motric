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