function addDevice() {
	var tb = document.getElementById("device_table");

	var row = tb.insertRow(-1);
	var model = row.insertCell(0);
	var os = row.insertCell(1);
	var quan = row.insertCell(2);
	var abrow = row.rowIndex;

	var imodel = document.createElement("INPUT");
	imodel.setAttribute("type", "text");
	imodel.setAttribute("class", "mtinput form-control device_extraline");
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

	window.scrollTo(0,document.body.scrollHeight)  // Scroll automatically to the bottom of the page.

	// window.alert(imodel.getAttribute("id") +"\n" + ios.getAttribute("id") +"\n" + inum.getAttribute("id"));
}

/* The AngularJS controller */
// var mo_request = angular.module('requestPage', []);

// mo_request.controller('requestCtrl', function($scope) {
// });


RECOMMANDED_DEVICE_LIST = '\
			<select class="form-control mtinput" name="deviceq" required>\
	          <option value="" hidden>--Select recommanded device--</option>\
	          <option value="marlin25">Pixel XL(API 25)</option>\
	          <option value="taimen27">Pixel 2 XL(API 27)</option>\
	          <option value="taimen28">Pixel 2 XL(API 28)</option>\
	          <option value="blueline28">Pixel 3(API 28)</option>\
	          <option value="blueline29">Pixel 3(API 29)</option>\
	          <option value="crosshatch29">Pixel 3 XL(API 29)</option>\
	          <option value="flame29">Pixel 4(API 29)</option>\
	          <option value="starqlteue">Galaxy S9(API 26)</option>\
	          <option value="G8142">Xperia XZ Premium(API 25)</option>\
	          <option value="iphone8">iPhone 8(OS 12.4)</option>\
	          <option value="iphonexr">iPhone Xr(OS 12.4)</option>\
	          <option value="flo">Nexus 7 2013(API 18)</option>\
	          <option value="bullhead">Nexus 5X(API 25)</option>\
	          <option value="FRT">Nokia 1-Android GO(API 27)</option>\
	          <option value="k61v1_basic_ref">Tecno-Android GO(API 29)</option>\
	          <option value="">Manually input</option>\
	        </select>\
	        '

function addQuotaDevice() {

	var tb = document.getElementById("deviceq_table");

	var row = tb.insertRow(-1);
	var model = row.insertCell(0);
	var quan = row.insertCell(1);
	// var abrow = row.rowIndex;

	var imodel = document.createElement("INPUT");
	imodel.setAttribute("type", "text");
	imodel.setAttribute("class", "mtinput form-control device_extraline");
	imodel.setAttribute("name", "deviceq");
	model.appendChild(imodel);

	var inum = document.createElement("INPUT");
	inum.setAttribute("type", "number");
	inum.setAttribute("class", "mtinput form-control");
	inum.setAttribute("min", "1");
	inum.setAttribute("name", "quantity");
	quan.appendChild(inum);

	window.scrollTo(0,document.body.scrollHeight)  // Scroll automatically to the bottom of the page.

	$('input[name="deviceq"]').on('focus', function(event) {
		$(this).parent().empty().append(RECOMMANDED_DEVICE_LIST)
			$('select[name="deviceq"]').on('change', function(event) {
				if ($(this).children('option:last-child').is(':selected')) {
				  $(this).parent().empty().append('<input class="mtinput form-control" type="text" name="deviceq">')
				}
			});
			// on_select_change()
	});
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

var operator = '';
function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log(profile.getName() + ' is signed in! -------------------------')
  console.log('ID: ' + profile.getId()); 
  console.log('Name: ' + profile.getName());
  console.log('Email: ' + profile.getEmail());
  var ldap = profile.getEmail().split('@')[0];
  console.log('Ldap: ' + ldap);
  console.log(window.location.href)
  operator = ldap;

  var name = profile.getGivenName();
  // document.getElementById("signed_name").innerText = "Welcome, " + name + "!";
  // document.getElementById("signout").style.visibility = "visible";

  document.getElementById("user_name").innerText = "Welcome, " + name + "!"
  document.getElementById("signin_close").classList.remove('hidden');
  document.getElementById("dont_clickme1").classList.add('hidden');
  document.getElementById("dont_clickme2").classList.add('hidden');
}

function SignIn() {
	var auth2 = gapi.auth2.getAuthInstance();
	auth2.signIn();	
}

function SignOut() {
	var auth2 = gapi.auth2.getAuthInstance();
	auth2.signOut();
	document.getElementById("signed_name").innerText = '';
	auth2.disconnect();
	var user = auth2.currentUser.get();
	var profile = user.getBasicProfile();
	console.log('After signing out, I still know -------------------------- ')
	console.log('ID: ' + profile.getId()); 
	console.log('Name: ' + profile.getName());
	console.log('Image URL: ' + profile.getImageUrl());
	console.log('Email: ' + profile.getEmail());
	document.getElementById("signout").style.visibility = "hidden";
}

function getUser() {
	var auth2 = gapi.auth2.getAuthInstance();
	var user = auth2.currentUser.get();
	return user;
}

function getProfile() {
	var auth2 = gapi.auth2.getAuthInstance();
	var user = auth2.currentUser.get();
	var profile = user.getBasicProfile();
	return profile;
}

function getUserName() {
	var profile = getProfile();
	console.log('ID: ' + profile.getId()); 
	console.log('Name: ' + profile.getName());
	console.log('Image URL: ' + profile.getImageUrl());
	console.log('Email: ' + profile.getEmail());
	return profile.getName();
}

function getLdap() {
	var profile = getProfile();
	var email = profile.getEmail();
	var ldap = email.split('@')[0];
	// console.log('Ldap: ' + ldap);
	return ldap;
}

/* Retreive responsed device list from server, pass it to handleResult to handle */
function getResponseStatus(primary_key, handleResult) {
	var token = $('input[name="csrfmiddlewaretoken"]').prop('value');
	var array = []
    $.ajax({
      type: 'POST',
      url: '/response_status/',
      data: {pk: primary_key, 'csrfmiddlewaretoken': token},
    })
    .done(function(result) {
    	// alert(result);
    	handleResult(result);
    });
}


// toastr.options.progressBar = true;
toastr.options.closeButton = true;
// toastr.options.closeMethod = 'fadeOut';
// toastr.options.closeMethod = 'slideUp';
toastr.options.positionClass = 'toast-center'; // This is my customized postion, need to name and config this class in 'toastr.css'.
toastr.options.timeOut = '2000';

/* jQury functions start from here. */
$(document).ready(function(){

	// $("th, td").each (function(index) {
	// 	console.log(index + ": " + $(this).text());
	// });
	// $.fn.editable.defaults.mode = 'inline';
	// toastr.success('Saved successfully!', 'IAmTitle', {timeOut: 1000}); // Must override the title before the timeOut override takes effect.

	// $('body').css('zoom','80%');

	$(".navul a").on("click", function(){
	   $(".navul").find(".active").removeClass("active");
	   $(this).addClass("active");
	   if ($(this).attr('id') == 'mytasks') {
	    $.ajax({
	      type: 'POST',
	      url: '/who/',
	      data: {'operator': operator, 'csrfmiddlewaretoken': token},
	    })
	   }
	});


	$("#tips-toggle").on("click", function() {
		if($("#search-tips").css('display') == 'none' ) {
			$("#search-tips").removeClass('hidden');
		}
		else {
			$("#search-tips").addClass('hidden');
		}
	});

	$("#search_submit").on("click", function() {
		var dest = $("#search_box");
		// dest.val(dest.val().split(" ").join(""))
		dest.val(dest.val().replace(/\s*\|\s*/g, '|'))
		dest.val(dest.val().replace(/\s*\:\s*/g, ':'))
		// dest.val(dest.val().replace(/(\s*)\|(\s*)/, '|'))

		$('#opter').val(operator)  // My trick to transfer the operator to backend.
	});

	$("#mini_search_submit").on("click", function() {
		var dest = $("#mini_search_bar");
		dest.val(dest.val().replace(/\s*\|\s*/g, '|'))
		dest.val(dest.val().replace(/\s*\:\s*/g, ':'))

		$('#opter_mini').val(operator)  // My trick to transfer the operator to backend.
	});

	var token = $('input[name="csrfmiddlewaretoken"]').prop('value');
	var currency_rate = '6.8';

	$('a[data-target="req_editor"]').editable({
		// type: 'text',
		placement: 'left',
		// pk: function(){}
		url: '/edit_request/',
        ajaxOptions: {
           dataType: 'json', 
           // headers: { "X-CSRFToken": token }
        }, 

        source: [
		 	// {text: ''},
		 	{value: 'PEK', text: 'PEK'},
		 	{value: 'MTV', text: 'MTV'},
			{value: 'TWD', text: 'TWD'},
        ],

        //This is not necessary if the header is set with token, vice versa. But the params option is really useful.
        params: function(params) {
		    //originally params contain pk, name and value
		    params.csrfmiddlewaretoken = token;
		    // params.operator = getLdap();
		    params.ov = $(this).text();  // ov stands for OldValue, this will be recorded by default.
		    params.opt = operator;
		    return params;
		},
        // emptytext:'Input',
        success: function(response, newValue) {
        	// console.log(response, response.status, response.statusText, newValue);
    		// if (response.status === 200) { // This needs to be defined by server definitely.
    			// alert('oldValue: ' + $(this).text() +'\nnewValue: ' + newValue);
    		// }
    			// if ($(this).attr('data-name') == 'ex_rate') {
    			// 	var rate = newValue;
    			// 	var preMatching = $(this).parent().prev().find('a');
    			// 	var nextMatching = $(this).parent().next().find('a');
    			// 	var price_c = preMatching.editable('getValue', true);  // Boolean: wheter to return just value of single element.
    			// 	var price_u = nextMatching.editable('getValue', true);

    			// 	// if ( price_c != 'Empty') {  // for the text() method inside editable, will identify the empty value as string 'Empty'.
    			// 	if ( price_c ) {
    			// 		price_u = (price_c / rate).toFixed(2);
    			// 		// This is for the database restore.
    			// 		$(nextMatching).editable('submit', {
    			// 			// ajaxOptions: {
					  //            // dataType: 'json', 
					  //            // headers: { "X-CSRFToken": token }
						 //    // }, 
    			// 			data: {
    			// 				'value': price_u,
    			// 				// 'csrfmiddlewaretoken': token
    			// 			}
    			// 		});
    			// 		// This is for the UI presentation.
    			// 		$(nextMatching).editable('setValue', price_u, false); // Boolean: whether to convert value from string to internal format.				
    			// 	} else if ( price_u ) {
    			// 		price_c = (price_u * rate).toFixed(2);
    			// 		$(preMatching).editable('submit', {
    			// 			// ajaxOptions: {
					  //            // dataType: 'json', 
					  //            // headers: { "X-CSRFToken": token }
						 //    // }, 
    			// 			data: {
    			// 				'value': price_c,
    			// 			}
    			// 		});
    			// 		$(preMatching).editable('setValue', price_c, false);       
    			// 	}
    			// }

    			if ($(this).attr('data-name') == 'po_number') {

    				var htitle = document.title;
    				if ( htitle.startsWith("Pending") ) {
	    				// var td_status = $(this).parent().next().next().next().next();
	    				var td_status = $(this).parent().nextAll(".td_status")
	    				var oldValue = td_status.text();

	    				if ($(this).text() == 'Empty') {
	    					var pkid = $(this).attr('data-pk');
		    				$.post('/edit_request/', {pk:pkid, name: 'status', value:'ORD', 'csrfmiddlewaretoken':token, ov:oldValue, 'opt':operator});
		    				td_status.html('Ordered');
		    				$("select[data-pk=" + pkid + "] option[value='REF']").remove();
		    				$("select[data-pk=" + pkid + "] option[value='APP']").remove();
	    				}
    				}

    				if ( htitle.startsWith("Resolved") ) {
	    				var pkid = $(this).attr('data-pk');
		    			$.post('/sync_info/', {pk:pkid, name: 'po', value:newValue, 'csrfmiddlewaretoken':token, 'opt':operator});    					
    				}
    			}

    			if ($(this).attr('data-name') == 'price_cny') {
    				var pkid = $(this).attr('data-pk');
    				var td_ex_rate = $(this).parent().next().find('a');
    				var td_price_u = $(this).parent().next().next().find('a');
    				$(td_ex_rate).editable('submit', {
    					data: {
    						'value': currency_rate,
    					}
    				});
    				$(td_ex_rate).editable('setValue', currency_rate, false);
    				var price_c = newValue;
    				var price_u = (price_c / currency_rate).toFixed(2);
    				var oldValue = td_price_u.text();
    				setTimeout(function() {
						// $(td_price_u).editable('submit', {
	    	// 				data: {
	    	// 					'value': price_u,
	    	// 				}
    		// 			});
    					$.post('/edit_request/', {pk:pkid, name: 'price_usd', value: price_u, 'csrfmiddlewaretoken': token, ov:oldValue, 'opt':operator});
    					$(td_price_u).editable('setValue', price_u, false);
					}, 200);

    			}    			

    			if ($(this).attr('data-name') == 'price_usd') {
    				var pkid = $(this).attr('data-pk');
    				var td_ex_rate = $(this).parent().prev().find('a');
    				var td_price_c = $(this).parent().prev().prev().find('a');
    				$(td_ex_rate).editable('submit', {
    					data: {
    						'value': currency_rate,
    					}
    				});
    				$(td_ex_rate).editable('setValue', currency_rate, false);
    				var price_u = newValue;
    				var price_c = (price_u * currency_rate);
    				var oldValue = td_price_c.text();

    				setTimeout(function() {
						// $(td_price_c).editable('submit', {
	    	// 				data: {
	    	// 					'value': price_c,
	    	// 				}
    		// 			});
    					$.post('/edit_request/', {pk:pkid, name: 'price_cny', value: price_c, 'csrfmiddlewaretoken': token, ov:oldValue, 'opt':operator});
    					$(td_price_c).editable('setValue', price_c, false);
					}, 200);

    			}

    			if (location.pathname == '/details/'){
    				location.reload();
    			}


		},
		error: function(response, newValue) {
			if (response.status === 500) {
				return 'submit might be illegal, try again.';
			} else {
				console.log(response);
				console.log(response.status);
				$(this).editable('setValue', newValue, false); 
				$(this).editable('hide');
				// location.reload(); // This is a work-around to resolve the weired PO_Number issue: if feed it with character, the error will occur even the reponse status code is 200.
				// return response.responseText;
			}
		}

	});


	$('a[data-target="labd_editor"]').editable({
		// mode: 'inline',
		// type:'text',
		placement: 'bottom',
		url: '/edit_labdevice/',
        ajaxOptions: {
           dataType: 'json', 
        }, 

        source: function() {
        	var elem = $(this)
        	if ( elem.attr('data-name') == 'lab_location' ){
        		return [
				{value: 'PEK', text: 'PEK'},
			 	{value: 'MTV', text: 'MTV'},
				{value: 'TWD', text: 'TWD'},
        		]
        	} else { // data-name == 'status'
        		return [
			 	// {text: ''},
			 	{value: 'AVA', text: 'Public'},
			 	{value: 'ASS', text: 'Assigned'},
				{value: 'BRO', text: 'Broken'},
				// {value: 'SUB', text: 'Replaced'}
				{value: 'REP', text: 'In Repair'},
				{value: 'RET', text: 'Retrieved'},
				{value: 'RTR', text: 'Retired'},
        		]
        	}
        	// prepend: $(this).text(),
        },

        params: function(params) {
		    //originally params contain pk, name and value
		    params.csrfmiddlewaretoken = token;
		    // params.operator = getLdap();
		    params.ov = $(this).text();
		    params.opt = operator;
		    return params;
		},

		validate: function(newValue) {
			// var oldValue = $(this).editable('getValue', true);  // by this way, oldValue could be empty.
			var oldText = ($(this).text());
			var valuedict = {'Public':'AVA', 'Assigned':'ASS', 'Broken':'BRO', 'REP':'In Repair', 'RET':'Retrieved', 'RTR':'Retired'};
			var oldValue = valuedict[oldText];
			var htitle = document.title;

			if (newValue == 'AVA' || newValue == 'ASS') { // newValue is much better than $(this).text(), it reflects the change.
				var td_owner = $(this).parent().prevAll().find('a[data-name="owner"]');
				var td_project = $(this).parent().prevAll().find('a[data-name="project"]');
				if (newValue == 'AVA') {
					td_owner.editable('submit', {
						data:{value:'mobileharness'},
						success: function(data) {
							td_owner.editable('setValue', 'mobileharness', false);
						},
						error: function(errors) {
							console.log($(this));
						}
					});

					setTimeout(function() {
						td_project.editable('submit', {
							data:{value:'PUBLIC'},
							success: function(data) {
								td_project.editable('setValue', 'PUBLIC', false);
							},
							error: function(errors) {
								console.log($(this));
							}
						});
					}, 200);

					if ( htitle.startsWith("Dedicated") || htitle.startsWith("Broken") ) {
						$(this).parent().parent().fadeOut(1500);
					}
				} else {  // newValue == 'ASS'
					if ( td_owner.text() == 'mobileharness' || td_project.text() == 'PUBLIC' ) {
						alert("Please modify owner and project to proper target first!")
						if ( td_owner.text() == 'mobileharness') {
							td_owner.editable('show');
						} else {
							td_project.editable('show');
						}
						return  newValue = oldValue;

					} else { // owner is other than mobileharness and project isn't 'PUBLIC', it's probably modified ahead.
						if ( htitle.startsWith("Public") || htitle.startsWith("Broken") ) {
							$(this).parent().parent().fadeOut(1500);
						}
					}
				} // end of condition newValue 'ASS'.
			} // end of condition newValue 'AVA' or 'ASS'.
			if ( (['BRO', 'REP', 'RTR'].indexOf(newValue) > -1) && !htitle.startsWith("Broken") ) {
				primary_key = $(this).attr('data-pk')
				console.log(primary_key)
				$('#broken_modal').modal({backdrop: "static"});
				// $(this).parent().parent().fadeOut(1500);

			}

		},

		success: function(response, newValue) {
			console.log('-------------In success block----------------');
			// console.log(response);
			// Validation is supposed to be done on the validate block.
		},

		error: function(response, newValue) {
			if (response.status === 500) {
				return 'submit might be illegal, try again.';
			} else if (response.status === 200) {
				console.error('-------------In error block----------------');
				console.log(response);
				console.log('newValue is: ', newValue);
			}
		}

	});


	// $('#rate').tooltip({title:"Click me to edit the exchage rate in one place!!!", placement:"bottom"});  //Weired behavior: cause the table column auto-grow.


/* Bind the approvoal checkbox and the submit button on device request page. */
    $('#req_submit').attr('disabled', 'disabled');
    $('#approval').on('change', function() {
      console.log('the status of the checkbox has been changed to: ' + $(this).prop('checked'));
      if ( $(this).prop('checked') ) {
        $('#req_submit').removeAttr('disabled')
      } else {
        $('#req_submit').attr('disabled', 'disabled');
      }
      console.log('the status of the button is: ' + $('#req_submit').prop('disabled'));    
    });
    $('#approval').prop('checked', false); //In case when user browse back, the checkbox is checked but the submit button is disabled.


/* Handle the various select options on the Request Disposal page. */
	var primary_key = 'hello world';
	var status = '';
    $('select[data-name="req_action"]').on('change', 
    	// { pk: $(this).attr('data-pk') },
    	function(event) {
    		var data =  { pk: $(this).attr('data-pk'), };
    		primary_key = data.pk;
    		status = $(this).val();
    		var td_project = $('td[data-pk=' + primary_key + '][data-name="project"]')
    		var td_price_c = $('a[data-pk=' + primary_key + '][data-name="price_cny"]')
    		var td_price_u = $('a[data-pk=' + primary_key + '][data-name="price_usd"]')
    		if ( (status == 'ASS' || status == 'AVA') && (td_price_c.text() == 'Empty' || td_price_u.text() == 'Empty') ){
    			alert("Please input complete price info first!");
    			$(this).val('');
    			return;
    		}
			switch ( status ) {
				case 'REF': 
					$('#confirm_modal').modal('show'); 
					break;

				case 'APP':
					// var poi = $(this).parent().prevAll().find('a[data-name="po_number"]');
				    // var td_status = $(this).parent().prev();
    				// var oldValue = td_status.text().trim();
					$('#eta_modal').modal({backdrop: "static"});
					break;

				case 'ASS':
				case 'CUR':
					if (td_project.text().toUpperCase() == 'PUBLIC'){
						alert("Guess you're adding PUBLIC devices,\nplease use the menu option \"Make Public\".")
						$(this).val('');
						break;
					}
					$('#allocation_modal').modal({backdrop: "static"}); // This option is to make the click outside of modal unable to close the dialog window.
					$(this).val('');
					break;
				case 'AVA':
					if (td_project.text().toUpperCase() != 'PUBLIC'){
						aw = confirm("Guess you're allocating devices to user,\nplease use the menu option \"Allocate New\" or \"Allocate Current\".\n\nIf you'are indeed adding PUBLIC devices, please click OK to confirm it, else click Cancel.")
						$(this).val('');
						if (aw == true) {
							$('#allocation_modal').modal({backdrop: "static"});
						}
						break;
					}
					$('#allocation_modal').modal({backdrop: "static"});
					$(this).val('');
					break;

				default:

			}

	});


	$('#submit_eta').on('click', function(event) {

  		eta = $('#eta_date').val();
  		if (eta == '') {
  			alert("Please choose a date!");
  		} else {
	  		$.post('/edit_request/', {pk: primary_key, name: 'status', value:'APP', 'eta': eta, 'csrfmiddlewaretoken':token, ov: 'Requested', 'opt':operator})
				.done( function(response) {
					toastr.success('Saved successfully!', {timeOut: 2000});
					$('#eta_date').val('');
					// $('#eta_form')[0].reset();
					$('#eta_modal').modal('hide');
					$("select[data-pk=" + primary_key + "]").parent().prevAll(".td_status").html('Approved');
					$("select[data-pk=" + primary_key + "]").val('');
					// $("select[data-pk=" + primary_key + "] option[value='REF']").remove();
    				$("select[data-pk=" + primary_key + "] option[value='APP']").remove();

					// if ( poi.text() == 'Empty') {
					//     setTimeout(function() {
					//         poi.editable('show');
					//     }, 200);						
					// }
				})
				.fail(function() {
					alert("Error! You might input something illegal.")
				});
		}
  	});

/* When user clicks Yes on the confirm modal. */
	$('#yes').on('click', {pk: primary_key}, function(event) {

  		$.post('/edit_request/', {pk: primary_key, name: 'status', value:'REF', 'csrfmiddlewaretoken': token, ov:'Requested', 'opt':operator, 'reason':$('#refuse_reason').val()})
  			.done( function(response) {
  				// alert('Response is ' + response);
  				$('a[data-pk=' + primary_key + ']').parent().parent().fadeOut(1000);
  			});

    });	

/* When user clicks Cancel on the confirm modal or allocation modal. */
	$('#no, #cancel').on('click', {pk:primary_key}, function(event) {
		var target = $('select[data-pk=' + primary_key + ']')
		$(target).val('');
		// console.log($(target).prop('value'));
		$('#allocation_table').children().remove();
		$('#inst').html('');
		$('#title').html('');

	});

	var required_qty = 0;
/* Dynamically create the input box based on the devices' quantity user requested. */
	$('#allocation_modal').on('show.bs.modal', {pk:primary_key, st:status}, function(event) {  /* Note show is way better than shown in latency */
		var td_quantity = $('a[data-pk=' + primary_key + ']').first().parent().prev()
		var quantity = td_quantity.text();
		// console.log('User requested ' + quantity + ' devices.');
		var td_model = $(td_quantity).prev().prev();
		var model = td_model.text();
		getResponseStatus(primary_key, function(device_list_string) {
			var device_array = JSON.parse(device_list_string);
			var responsed_qty = device_array.length;
			required_qty = quantity - responsed_qty
			// alert("required shots:" + required_qty)
			switch ( status ) {
				case 'ASS':
					$('#inst').html('You can now allocate device to users from newly purchased devices. Input <b><span style="color:red">device id</b>(for Android, it is serial number, for iOS, it is unique identifier) please.');
					$('#title').html('Allocate Newly Purchased Devices');
					for (n = 0; n < responsed_qty; n++) {
						$('#allocation_table').append('<tr><td style="padding:10px">' + model + '</td><td><input type="text" class="form-control" value="' + device_array[n] + '" name="did" disabled></td></tr>');
					}
					for (i = 0; i < required_qty; i++) {
						$('#allocation_table').append('<tr><td style="padding:10px">' + model + '</td><td><input type="text" class="form-control" placeholder="input device id" name="did" ></td></tr>');
					}
					break;		
				case 'CUR':
					$('#inst').html('You can now allocate device to users from public pool. Input <b><span style="color:red">first #</span></b> on the <a href="/public_device/" target="_blank">public devices</a> page please.');
					$('#title').html('Allocate Public Devices');
					for (n = 0; n < responsed_qty; n++) {
						$('#allocation_table').append('<tr><td style="padding:10px">' + model + '</td><td><input type="text" class="form-control" value="' + device_array[n] + '" name="pkid" disabled></td></tr>');
					}
					for (i = 0; i < required_qty; i++) {
						$('#allocation_table').append('<tr><td style="padding:10px">' + model + '</td><td><input type="text" class="form-control" placeholder="input first #" name="pkid" ></td></tr>');
					}
					break;
				case 'AVA':
					$('#inst').html('Register the newly purchased devices and put them into PUBLIC pool of our lab.');
					$('#title').html('Make Device Public');
					for (n = 0; n < responsed_qty; n++) {
						$('#allocation_table').append('<tr><td style="padding:10px">' + model + '</td><td><input type="text" class="form-control" value="' + device_array[n] + '" name="did" disabled></td></tr>');
					}
					for (i = 0; i < required_qty; i++) {
						$('#allocation_table').append('<tr><td style="padding:10px">' + model + '</td><td><input type="text" class="form-control" placeholder="input device id" name="did" ></td></tr>');
					}
					break;
				case 'LOC':
					$('#inst').html('Choose location of the central lab for the devices.');
					$('#title').html('Set location');
					$('#allocation_table').append('<tr><td style="padding:10px"><input type="radio" name="location" value="PEK">Beijing</td> \
						<td style="padding:10px"><input type="radio" name="location" value="MTV">Mountain View</td> \
						<td style="padding:10px"><input type="radio" name="location" value="TWD">Taiwan DataCenter</td></tr> \
						<tr><td style="padding:10px;color:red">Current: ' + $('input[data-pk=' + primary_key + '][data-name="lab_location"]').val() + '</td></tr>' );
					break;
				default:
			}

			$('#allocation_table').append('<tr><td><input type="hidden" name="pk" value=' + primary_key + '></td></tr>');
			$('#allocation_table').append('<tr><td><input type="hidden" name="status" value=' + status + '></td></tr>');
		});

 	});


/* When user clicks Submit on the allocation modal and the submit is successfully done. */
	$('#allocation_form').on('submit', function(event) {
		// var val =  $(this).find('input');
		var shots = 0
    	$(this).find('input[name="pkid"], input[name="did"]').each(function (){
    		if ($.trim($(this).val()) === '') {
				$(this).prop("disabled", true);
				// $(this).attr("disabled", "disabled");
    		} else if (!$(this).prop("disabled")) { // DO NOT calculate the partly allocated devices.
    			shots +=1;
    		}
    		return true;
    	});
    	// alert("shots:" + shots)
		var val = $(this).serialize() + '&opt=' + operator;

		// console.log($(this).serializeArray());
		// console.log(JSON.stringify($(this).serializeArray()));

		// var new_location = val.split('&')[1].substr(-3);

		// ## The post shorthand method just doesn't work in this case.
		// $.post('/device_allocate/', {data: val, 'csrfmiddlewaretoken': token, dataType:'json'})
  			// .done( function(response) {
  				// alert('Response is ' + response);
  				// $('a[data-pk=' + primary_key + ']').parent().parent().fadeOut(1000);
  			// });
  		$.ajax({
            url: '/device_allocate/',
            type: 'post',
            data: val,
        })
        // ## .done(), .fail(), .always() are alternative constructs to the callback options of success(), error(), complete(), the latter will be deprecated as of jQuery 3.0.
        .done(function(data) {
        	if (data != "[]") { // If no duplication, server only return a empty list [], else return the list of duplicates.
        		alert("Devices already exist:\n\n" + data)
        	}
        	else {
        		toastr.success('Saved successfully!', {timeOut: 2000});
        		$('#allocation_modal').modal('hide');
        		$('#allocation_table').children().remove();
        		if ( shots == required_qty ){
        			$('a[data-pk=' + primary_key + ']').parent().parent().fadeOut(1000);
        		} else {
        			// $('input[data-pk=' + primary_key + '][data-name="lab_location"]').val(new_location);
        		}
        	}

        })
        /* ---------- (UPDATED 170518) Duplication elimination is better to be done on server side before trying to write data to database. --------*/
        // .fail(function(xhr) {
        // 	exceptionType = 'IntegrityError'
        // 	var xtext = xhr.responseText
        // 	if ( xtext.indexOf(exceptionType) > -1 ) {
        // 		var start = xtext.indexOf("Duplicate entry")
        // 		substring = xtext.substr(start, 200)  // 200 is long enough to get the subtring that contains the device id.
        // 		did = substring.split("\'")[1]

        // 		alert("Error! you input device that already exists: " + did +".\n\nServer only tell me one duplicate entry at one time, so please exclude devices one by one :)")
        // 	}
        // 	else {
        // 		alert("Error! You might input something illegal.")
        // 	}
        // });
        .fail(function(xhr) {
        	alert("Error! You might input something illegal.")
        })
        event.preventDefault();
	});


/* When user clicks the Replace button of every device item */
	$('.btn-hidden-replace').on('click', function(event) {
		primary_key = $(this).attr('data-pk');
		$('#replacement_modal').modal({backdrop: "static"});
	});

	$('#submit_rep').on('click', {pk:primary_key}, function(event) {
  		$.post('/device_replacement/', {pk: primary_key, replacement_pk:$('#replacement_pk').val(), 'csrfmiddlewaretoken':token, 'opt':operator})
			.done( function(response) {
				toastr.success('Saved successfully!', {timeOut: 2000});
				$('#replacement_modal').modal('hide');
				$('#replacement_pk').val('');
			})
			.fail(function() {
        		alert("Error! You might input something illegal.")
        	});	
	});

	$('#cancel_rep').click(function() {
		$('#replacement_pk').val('');
	});



/* When user clicks the Received button of every request item */
	$('.btn-hidden-receive').on('click', function(event) {
		primary_key = $(this).attr('data-pk');
		td_status = $(this).parent()
  		$.post('/edit_request/', {pk: primary_key, name: 'status', value:'REC', 'csrfmiddlewaretoken':token, ov:'Ordered', 'opt':operator })
  			.done( function(response) {
  				td_status.html('Received');
  			});
  	});

  /* When user clicks the Charged button of every request item */
	$('.btn-hidden-charge').on('click', function(event) {
		primary_key = $(this).attr('data-pk');
		td_status = $(this).parent()
  		$.post('/edit_request/', {pk: primary_key, name: 'charged', value:'1', 'csrfmiddlewaretoken':token, ov:'0', 'opt':operator})
  			.done( function(response) {
  				td_status.addClass("bold_green");
  			});
  	}); 

  /* When user clicks the Attach_bug button of every request item */
	$('.btn-hidden-attach_bug').on('click', function(event) {
		primary_key = $(this).attr('data-pk');
		td_bug = $(this).parent()
		$('#bug_modal').modal('show'); 
  	});

  	$('#submit_bugid').on('click', function(event) {
  		bugid = $('#bugid_input').val()
  		$.post('/edit_request/', {pk: primary_key, name: 'bug_id', value: bugid, 'csrfmiddlewaretoken':token, ov:'Empty', 'opt':operator})
			.done( function(response) {
				toastr.success('Saved successfully!', {timeOut: 2000});
				$('#bugid_input').val('');
				td_bug.html('<a href="http://b/' + bugid + '" target="_blank">' + bugid +'</a>');
			});
  	});



  /* When user clicks the Show or Hide anchor */
	$('#toggle-show').on('click', function(event) {
		// if($(this).text() == 'Show more') {
		// 	$('.hidden_column').removeClass('hidden_column').addClass('shown_column');
		// 	$(this).text('Show less')
		// }
		// else {
		// 	$('.shown_column').removeClass('shown_column').addClass('hidden_column');
		// 	$(this).text('Show more');
		// }

		if($(this).text() == 'Show more columns') {
			$('.l2_column').removeClass('hidden');
			$(this).text('Show less columns')
		}
		else {
			$('.l2_column').addClass('hidden');
			$(this).text('Show more columns');
		}
		// $('.l2_column').toggle();
  	});


   $('select[name="pref_loc"]').on('change', function(event) {
   		var opt = $(this).val();
   		console.log("Preferred location is: " + opt);
   		if (opt == 'MTV'){
   			$('#lab_modal').modal({backdrop: "static"});
   		}
   });

      $('#submit_lab').on('click', function(event) {
   		if ( $('input[name="device_choice"]:checked').val() == 'DIY') {
   			$('#comment').val('Buy the devices myself.');  //input uses val(), while table cell uses html() to set values.
   		}
   });

	// $('select').each(function(index) {
		// console.log(index + ': ' + $(this).text());
	// });


	$(':text[name="device"]').each(function() {
		var elem = $(this);
		elem.bind("change", function(event){ //"change" is better than "input", the latter will trigger "Nexus 5" one time before when user will actually input "Nexus 5x"
			switch (elem.val()){
				case 'Nexus 5':
				case 'nexus 5':
					// alert("please expect long time for preparing!");
					$('#notice1').removeClass("hidden");
					break;
				case 'Nexus 5x':
				case 'nexus 5x':
				case 'Nexus 5X':
				case 'nexus 5X':
				case 'Nexus 7':
				case 'nexus 7':
					$('#notice2').removeClass("hidden");
			}
		});
	});

	// Dynamically bind the price_cny and price_usd on the Device Register page.
	$(':text[data-name="price"]').each(function() {
		var elem = $(this);
		elem.on("input", function (event) {  // Here "input" is better than "change", input gives quick feedback one letter by one letter.
			if (elem.attr('name') == 'price_cn') {
				var price_usd = (elem.val() / currency_rate).toFixed(2);
				$('input[name="price_us"]').val(price_usd)
			}
			else {
				var price_cny = (elem.val() * currency_rate).toFixed(2);
				$('input[name="price_cn"]').val(price_cny)
			}
		})
	})


	$('#add-more').on('click', function(event) {

		var tb = document.getElementById("deviceid_table")
		var amount = $('#more-amount').val();

		for (i = 0; i < amount; i++) {
			var row = tb.insertRow(-1);
			var td1 = row.insertCell(0);
			var td2 = row.insertCell(1);

			var idevid = document.createElement("INPUT");
			idevid.setAttribute("type", "text");
			idevid.setAttribute("class", "mtinput form-control");
			idevid.setAttribute("name", "device_id");
			td1.appendChild(idevid);

			var idevid = document.createElement("INPUT");
			idevid.setAttribute("type", "text");
			idevid.setAttribute("class", "mtinput form-control");
			idevid.setAttribute("name", "device_id");
			td2.appendChild(idevid);
		}

		window.scrollTo(0,document.body.scrollHeight)  // Scroll automatically to the bottom of the page.

	});

	$('#moha-device-request').on('submit', function(event) {

    	$(this).find('.device_extraline').each(function (){
    		if ($.trim($(this).val()) === '') {
    			$(this).parent().parent().remove(); // Remove the whole line if model type isn't defined.
				// $(this).prop("disabled", true);
				// $(this).attr("disabled", "disabled");
    		}

    		return true;
    	});

    	vals = $(this).serialize() + '&opt=' + operator;
    	console.log(vals);
    	// $.ajax({
     //        url: '/request/',
     //        type: 'post',
     //        // dataType: 'json',
     //        data: vals,
     //    })

    	// event.preventDefault();
	});

	$('#device_register_form').on('submit', function(event) {

		// var val = $(this).find('input, select').not('[value=""]').serialize();  // This doesn't work.

		// var vals = $('#device_register_form input, #device_register_form select').map(function () {  // This assasinates those inputs that allows empty value.
  //       	return $(this).val().trim() == "" ? null : this;
  //   	}).serialize();

  		// $(this).find(':input[name="device_id"][value=""]').attr("disabled", "disabled");

  		// var vals = $('#device_register_form input, #device_register_form select').filter(function () {  // This assasinates those inputs that allows empty value.
    //     	return $(this).val();
    // 	}).serialize();

    	$(this).find(':input[name="device_id"]').each(function (){
    		if ($.trim($(this).val()) === '') {
				$(this).prop("disabled", true);
				// $(this).attr("disabled", "disabled");
    		}

    		return true;
    	});

    	vals = $(this).serialize() + '&opt=' + operator;
    	console.log(vals);

  		$.ajax({
            url: '/register/',
            type: 'post',
            // dataType: 'json',
            data: vals,
        })
        .done(function(data) {
        	if (data != "[]") { // If the device isn't a duplicate, server only return a empty list [], else return the list of duplicates.
        		alert("Devices already exist:\n\n" + data)
        	}
        	else {
        		toastr.success('Saved successfully!', {timeOut: 2000});
        	}
        })
        .fail(function() {
        	alert("Error! You might input something illegal.")
        })
    //     .always(function () {
    //     	$(this).find(':input[name="device_id"]').each(function (){
				// console.log($(this));
				// $(this).removeAttr("disabled");
    // 	    });
    //     });	
        event.preventDefault();
        $(this).find(':input[name="device_id"]').each(function (){  // This block doesn't work in .done and .always... don't know why.
			$(this).removeAttr("disabled");
			$(this).val('')
	    });
	});


/* When user clicks the MalRecord button of every device item */
	$('.btn-hidden-malrec').on('click', function(event) {
		primary_key = $(this).attr('data-pk');
		$('#malfunction_modal').modal({backdrop: "static"});
	});

	$('#malfunction_form, #broken_form').on('submit', function(event) {
    	vals = $(this).serialize() + '&pk=' + primary_key +'&opt=' + operator;
    	console.log(vals);

  		$.ajax({
            url: '/mal_record/',
            type: 'post',
            data: vals,
        })
        .done(function(data) {
        	toastr.success('Saved successfully!', {timeOut: 2000});
        	$('#malfunction_form')[0].reset()
        	$('#broken_form')[0].reset()
        	$('#malfunction_modal, #broken_modal').modal('hide');

        })
        // .fail(function(data) {
        // 	alert("Error! You might input something illegal.")
        // })
        event.preventDefault();

	});

	function on_select_change(){
		$('select[name="deviceq"]').on('change', function(event) {
			if ($(this).children('option:last-child').is(':selected')) {
			  console.log("Manually input!!!");
			  $(this).parent().empty().append('<input class="mtinput form-control" type="text" placeholder="e.g. Pixel 3A, API 27 -- leave OS/API level empty if doesn\'t matter." name="deviceq">')
			}
			else {
		 		var opt = $(this).val();
				console.log("Selected device is: " + opt);
				// var optext = $(this).find("option:selected").text()
				// // console.log(optext.split("(")[1].slice(0, -1));
				// var api=optext.split("(")[1].slice(0, -1);
				// $(this).parent().next().text(api);
			}
		});
	}

	on_select_change()


	$('input[name="deviceq"]').on('focus', function(event) {
 		var opt = $(this).val();
		console.log("Lets call selection!");
		$(this).parent().empty().append(RECOMMANDED_DEVICE_LIST)
			$('select[name="deviceq"]').on('change', function(event) {
				if ($(this).children('option:last-child').is(':selected')) {
				  console.log("Manually input!!!");
				  $(this).parent().empty().append('<input class="mtinput form-control" type="text" name="deviceq">');
				}
			});
			// on_select_change()
	});

	$(window).on('load', function() {

		setTimeout(function() {
			if ( location.pathname != '/' && location.pathname != '/device_request/') {   //Force to signin except nav and device request page.
			    var auth2 = gapi.auth2.getAuthInstance();
			    var guser = auth2.currentUser.get();
			    var profile = guser.getBasicProfile();
			    console.log(window.location);
			    // console.log('Current User: ', guser);
			    // console.log('User profile: ', profile);
			    if (profile === undefined) {
			    	var token = $('input[name="csrfmiddlewaretoken"]').prop('value');
			    	var yip;
			    	// copied from http://stackoverflow.com/questions/391979/how-to-get-clients-ip-address-using-javascript-only
					var findIP = new Promise(r=>{var w=window,a=new (w.RTCPeerConnection||w.mozRTCPeerConnection||w.webkitRTCPeerConnection)({iceServers:[]}),b=()=>{};a.createDataChannel("");a.createOffer(c=>a.setLocalDescription(c,b,b),b);a.onicecandidate=c=>{try{c.candidate.candidate.match(/([0-9]{1,3}(\.[0-9]{1,3}){3}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})/g).forEach(r)}catch(e){}}})

					findIP.then(ip => {console.log('your ip: ', ip); yip = ip }).catch(e => console.error(e))

					setTimeout(function() {
						$.ajax({
						  type: 'POST',
						  url: '/who/',
						  data: {operator: yip, 'csrfmiddlewaretoken': token},
						  success: function(result) {
						    // Handle or verify the server response.
						  },
						});
					}, 500);

					$('#signin_modal').modal({backdrop: "static"});

			  //   	auth2.signIn().then(function(){  // This pop-up will be blocked by browser by default.
					//   	var guser2 = auth2.currentUser.get();
					//   	var profile = guser2.getBasicProfile();
					//   	console.log('Current User: ', guser2);
					//   	console.log('Current Username: ', profile.getName());
					// 	var name = profile.getGivenName();
					//     $('#signed_name').text("Welcome, " + name + "!");
					//     $('#signout').css('visibility', 'visible');
					//     onSignIn(guser);
					// });
			    }
			// } else {
			// 	gapi.load('auth2', function() {
			// 		auth2 = gapi.auth2.init({
			// 			client_id: '613024433503-bplsrhovk0a60ng7lrlb6slg49ta320h.apps.googleusercontent.com',
			// 		    scope:'profile email',
			// 		});
			// 	});
			}

		}, 2000);  // Set latency to make sure the login status is obtained after the page loaded completely.

		if ( location.pathname == '/request_disposal/' || location.pathname == '/device_register/' || location.pathname == '/request_history/' ) {
			$.ajax({
				type: 'GET',
				dataType: 'jsonp',
				jsonp: 'callback',
				// jsonpCallback: '?',
				// url: 'http://freecurrencyrates.com/api/action.php?s=fcr&iso=USDCNY&f=USD&v=1&do=cvals&ln=en',
				url: 'https://api.fixer.io/latest?base=USD&symbols=CNY',
				crossDomain: true,
				success: function(data) {
					// var jsonobj = JSON.parse(data);
					console.warn('Newest currency(USD -> CNY): ', data.rates.CNY);
					currency_rate = data.rates.CNY;
				}
			});
		}

	});

});