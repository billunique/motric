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

/* The AngularJS controller */
// var mo_request = angular.module('requestPage', []);

// mo_request.controller('requestCtrl', function($scope) {
// });

/* My raw javascript handler for the options selected. */
// function action_handler(value) {
// 	try {
// 		switch (value) {
// 			case 'REF': confirm("You're refusing the request from our adorable user, you sure?"); break;
// 			// case 'REF': pop_warning(); break;
// 			case 'APP': popup_po(); break;
// 			case 'AVA': popup_add_sn(); break;
// 			case 'ASS': popup_add_sn(); break;
// 			default: 
// 		}
// 	}
// 	catch(err) {
// 		alert(err.message);
// 	}
// }

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

function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log(profile.getName() + ' is signed in! -------------------------')
  console.log('ID: ' + profile.getId()); 
  console.log('Name: ' + profile.getName());
  console.log('Email: ' + profile.getEmail());
  var ldap = profile.getEmail().split('@')[0];
  console.log('Ldap: ' + ldap);

  var name = profile.getGivenName();
  document.getElementById("signed_name").innerText = "Welcome, " + name + "!";
  document.getElementById("signout").style.visibility = "visible";

  var token = $('input[name="csrfmiddlewaretoken"]').prop('value');
  $.ajax({
      type: 'POST',
      url: '/who/',
      data: {operator: ldap, 'csrfmiddlewaretoken': token},
      success: function(result) {
        // Handle or verify the server response.
      },
    });
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
	console.log('Ldap: ' + ldap);
	return ldap;
}

// Create the XHR object.
function createCORSRequest(method, url) {
  var xhr = new XMLHttpRequest();
  if ("withCredentials" in xhr) {
    // XHR for Chrome/Firefox/Opera/Safari.
    xhr.open(method, url, true); // true for asynchronous.
  } else if (typeof XDomainRequest != "undefined") {
    // XDomainRequest for IE.
    xhr = new XDomainRequest();
    xhr.open(method, url);
  } else {
    // CORS not supported.
    xhr = null;
  }
  return xhr;
}


// Make the actual CORS request.
function makeCorsRequest(url) {

  var xhr = createCORSRequest('GET', url);
  if (!xhr) {
    alert('CORS not supported');
    return;
  }

  // Response handlers.
  xhr.onload = function() {
    var text = xhr.responseText;
    return text;
  };

  // xhr.onerror = function() {
  //   alert('Woops, there was an error making the request.');
  // };

  xhr.send();
}

// toastr.options.progressBar = true;
toastr.options.closeButton = true;
// toastr.options.closeMethod = 'fadeOut';
// toastr.options.closeMethod = 'slideUp';
toastr.options.positionClass = 'toast-center'; // This is my customized postion, need to name and config this class in 'toastr.css'.
toastr.options.timeOut = '2000';

/* jQury functions start from here. */
$(document).ready(function(){
	// alert(window.location.href);
	// alert(window.location.pathname);
	// $("th, td").each (function(index) {
	// 	console.log(index + ": " + $(this).text());
	// });
	// $.fn.editable.defaults.mode = 'inline';
	// toastr.success('Saved successfully!', 'IAmTitle', {timeOut: 1000}); // Must override the title before the timeOut override takes effect.

	var token = $('input[name="csrfmiddlewaretoken"]').prop('value');
	var currency_rate = '6.6';
	$('a[data-target="req_editor"]').editable({
		// type: 'text',
		placement: 'left',
		// pk: function(){}
		url: '/edit_request/',
        ajaxOptions: {
           dataType: 'json', 
           // headers: { "X-CSRFToken": token }
        }, 
        //This is not necessary if the header is set with token, vice versa. But the params option is really useful.
        params: function(params) {
		    //originally params contain pk, name and value
		    params.csrfmiddlewaretoken = token;
		    // params.operator = getLdap();
		    params.ov = $(this).text();
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
    			// 	// var price_c = $(this).parent().prev().text();
    			// 	var price_c = preMatching.editable('getValue', true);  // Boolean: wheter to return just value of single element.
    			// 	var price_u = nextMatching.editable('getValue', true);
    			// 	console.log(price_c + price_u)
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
    				var td_status = $(this).parent().next().next().next().next();
    				var oldValue = td_status.text();
    				var pkid = $(this).attr('data-pk');
    				$.post('/edit_request/', {pk:pkid, target: 'status', target_value:'ORD', 'csrfmiddlewaretoken': token, ov:oldValue});
    				td_status.html('Ordered');
    				$("select[data-pk=" + pkid + "] option[value='REF']").remove();
    				$("select[data-pk=" + pkid + "] option[value='APP']").remove();
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
    					$.post('/edit_request/', {pk:pkid, name: 'price_usd', value: price_u, 'csrfmiddlewaretoken': token, ov:oldValue});
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
    					$.post('/edit_request/', {pk:pkid, name: 'price_cny', value: price_c, 'csrfmiddlewaretoken': token, ov:oldValue});
    					$(td_price_c).editable('setValue', price_c, false);
					}, 200);

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

        source: [
		 	// {text: ''},
		 	{value: 'AVA', text: 'Public'},
		 	{value: 'ASS', text: 'Assigned'},
			{value: 'BRO', text: 'Broken'},
			// {value: 'SUB', text: 'Replaced'}
        ],
        // prepend: $(this).text(),

        params: function(params) {
		    //originally params contain pk, name and value
		    params.csrfmiddlewaretoken = token;
		    // params.operator = getLdap();
		    params.ov = $(this).text();
		    return params;
		},

		success: function(response, newValue) {
			console.log('-------------In success block----------------');
			console.log(response);
			// var oldValue = $(this).editable('getValue', true);  // by this way, oldValue could be empty.
			// console.log(oldValue);
			var oldText = ($(this).text());
			var valuedict = {'Public':'AVA', 'Assigned':'ASS', 'Broken':'BRO'};
			var oldValue = valuedict[oldText];

			$(this).editable('setValue', newValue, false); 
			$(this).editable('hide');

			var htitle = document.title;
			if (newValue == 'AVA' || 'ASS') { // newValue is much better than $(this).text(), it reflects the change.
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
				} else if ( newValue == 'ASS' ) {  // to avoid the case newValue is empty, explicitly state the else if.
					if ( td_owner.text() == 'mobileharness' ) {
						setTimeout(function() {
							td_owner.editable('show');
						}, 200);
						$(this).editable('setValue', oldValue, true);
					} else { // owner is other than mobileharness, it's probably modified ahead.
						if ( td_project.text() == 'PUBLIC' ) {
							setTimeout(function() {
								td_project.editable('show');
							}, 200);
							$(this).editable('setValue', oldValue, false);
						} else if ( htitle.startsWith("Public") || htitle.startsWith("Broken") ) {
							$(this).parent().parent().fadeOut(1500);
						}
					}
				} // end of condition newValue 'ASS'.
			} // end of condition newValue 'AVA' or 'ASS'.
			if ( newValue == 'BRO' && !htitle.startsWith("Broken") ) {
				$(this).parent().parent().fadeOut(1500);
			}
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




	// $('a[data-type="select"]').editable({
	// 	placement: 'left',
 //        value: '',    
 //        source: [
 //        	{value: '', text: 'not selected'},
 //            {value: 'REF', text: 'Decline'},
 //            {value: 'APP', text: 'Approve'},
 //            {value: 'AVA', text: 'Make public'},
 //            {value: 'ASS', text: 'Allocate'}
 //        ]
 //    });


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
    $('select').on('change', 
    	// { pk: $(this).attr('data-pk') },
    	function(event) {
    		console.log(this);
    		console.log($(this));
    		var data =  { pk: $(this).attr('data-pk'), };
    		primary_key = data.pk;
    		status = $(this).val();
			switch ( status ) {
				case 'REF': 
					// var answ = confirm("Sure?");
					// console.log(answ);					
					// $('#confirm_modal').on('show.bs.modal', data, function(event) {
					//     var pk = data.pk;
					//     alert('Before the modal shown, I am popping up first.');
					//     console.log('The primary key that I will receive is: ', pk);
					// });
					$('#confirm_modal').modal('show'); 

					// $('#yes').one('click', data, function(event) {
					// 	console.log('I am inside the on listener...............................................................My index is: ', index);
					// 	var ele = $(this);
					// 	console.log(ele);
					// 	alert('index' + $(this).index());
					// 	console.log('data.pk', event.data.pk);
					// 	console.log('-------------------------------------------------------------------------------');
					// });	

					console.log('Primary key of this event: ', 
						// event.data.pk, 
						data.pk
						// $(this).attr('data-pk')
						);
					break;

				case 'APP': 
    				var td_status = $(this).parent().prev();
    				var oldValue = td_status.text();
					$.post('/edit_request/', {pk: primary_key, target: 'status', target_value:'APP', 'csrfmiddlewaretoken': token, ov:oldValue});
					td_status.html('Approved');
					$("select[data-pk=" + primary_key + "] option[value='REF']").remove();
    				$("select[data-pk=" + primary_key + "] option[value='APP']").remove();
					// $(this).parent().prevAll().find('a[data-name="po_number"]').trigger("click");
					var poi = $(this).parent().prevAll().find('a[data-name="po_number"]');
					console.log(poi, poi.val(), poi.text());
					if ( poi.text() == 'Empty') {
					    setTimeout(function() {
					        poi.editable('show');
					    }, 200);						
					}
					break;

				case 'ASS':
				case 'AVA':
    				var td_price_c = $('a[data-pk=' + primary_key + '][data-name="price_cny"]')
					var td_price_u = $('a[data-pk=' + primary_key + '][data-name="price_usd"]')
					if (td_price_c.text() == 'Empty' || td_price_u.text() == 'Empty'){
						alert("Please input complete price info first!");
						$(this).val('');
						break;
					}
				case 'CUR':
				case 'LOC':
					$('#allocation_modal').modal({backdrop: "static"}); // This option is to make the click outside of modal unable to close the dialog window.
					$(this).val('');
					break;

				default:

			}

		}
	);

/* When user clicks Yes on the confirm modal. */
	$('#yes').on('click', {pk: primary_key}, function(event) {
		// console.log('I am outside of the on listener...............................................................');
		// var ele = $(this);
		// console.log(ele);
  // 		// alert('index' + $(this).index());
  // 		alert('primary key of this element: ' + primary_key);
  // 		console.log('data.pk', event.data);
  // 		console.log('target', event.target);
  // 		console.log('currentTarget', event.currentTarget);
  // 		console.log('relatedTarget', event.relatedTarget);
  // 		console.log('delegateTarget', event.delegateTarget);
  // 		console.log('result', event.result);
  // 		console.log('which', event.which);
  // 		console.log('type', event.type);
  // 		console.log('timestamp', event.timeStamp);
  // 		console.log('pageX + pageY', event.pageX, event.pageY);
  // 		console.log('offsetX + offsetY', event.offsetX, event.offsetY);
  // 		console.log('----------------------------------------------');
  		$.post('/edit_request/', {pk: primary_key, target: 'status', target_value:'REF', 'csrfmiddlewaretoken': token, ov:'Requested'})
  			.done( function(response) {
  				// alert('Response is ' + response);
  				$('a[data-pk=' + primary_key + ']').parent().parent().fadeOut(1000);
  			});

    });	

/* When user clicks Cancel on the confirm modal or allocation modal. */
	$('#no, #cancel').on('click', {pk:primary_key}, function(event) {
		var target = $('select[data-pk=' + primary_key + ']')
		// console.log(target);
		// console.log($(target));
		$(target).val('');
		// console.log($(target).prop('value'));
		$('#allocation_table').children().remove();
		$('#inst').html('');
		$('#title').html('');

	});


/* Dynamically create the input box based on the devices' quantity user requested. */
	$('#allocation_modal').on('show.bs.modal', {pk:primary_key, st:status}, function(event) {  /* Note show is way better than shown in latency */
		var td_quantity = $('a[data-pk=' + primary_key + ']').first().parent().prev()
		console.log($(td_quantity));
		var quantity = td_quantity.text();
		// console.log('User requested ' + quantity + ' devices.');
		var td_model = $(td_quantity).prev().prev();
		var model = td_model.text();
		switch ( status ) {
			case 'ASS':
				$('#inst').html('You can now allocate device to users from newly purchased devices. Input <b><span style="color:red">device id</b>(for Android, it is serial number, for iOS, it is unique identifier) please.');
				$('#title').html('Allocate Newly Purchased Devices');
				for (i = 0; i < quantity; i++) {
					$('#allocation_table').append('<tr><td style="padding:10px">' + model + '</td><td><input type="text" class="form-control" placeholder="input device id" name="did" required></td></tr>');
				}
				break;		
			case 'CUR':
				$('#inst').html('You can now allocate device to users from public pool. Input <b><span style="color:red">first #</span></b> on the public devices page please.');
				$('#title').html('Allocate Public Devices');
				for (i = 0; i < quantity; i++) {
					$('#allocation_table').append('<tr><td style="padding:10px">' + model + '</td><td><input type="text" class="form-control" placeholder="input first #" name="pkid" required></td></tr>');
				}
				break;
			case 'AVA':
				$('#inst').html('Register the newly purchased devices and put them into PUBLIC pool of our lab.');
				$('#title').html('Make Device Public');
				for (i = 0; i < quantity; i++) {
					$('#allocation_table').append('<tr><td style="padding:10px">' + model + '</td><td><input type="text" class="form-control" placeholder="input device id" name="did" required></td></tr>');
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


/* When user clicks Submit on the allocation modal and the submit is successfully done. */
	$('#allocation_form').on('submit', function(event) {
		// var val =  $(this).find('input');
		var val = $(this).serialize();
		console.log(val);
		var new_location = val.split('&')[1].substr(-3);
		// ## The post shorthand method just doesn't work in this case.
		// $.post('/device_allocate/', {data: val, 'csrfmiddlewaretoken': token, dataType:'json'})
  			// .done( function(response) {
  				// alert('Response is ' + response);
  				// $('a[data-pk=' + primary_key + ']').parent().parent().fadeOut(1000);
  			// });
  		$.ajax({
            url: '/device_allocate/',
            type: 'post',
            // dataType: 'json',
            data: val,
        })
        // ## .done(), .fail(), .always() are alternative constructs to the callback options of success(), error(), complete(), the latter will be deprecated as of jQuery 3.0.
        .done(function(data) {
            toastr.success('Saved successfully!', {timeOut: 2000});
            $('#allocation_modal').modal('hide');
            $('#allocation_table').children().remove();
            if (!val.includes('LOC')){ // status is 'ASS' or 'AVA'
            	$('a[data-pk=' + primary_key + ']').parent().parent().fadeOut(1000);
            } else {
            	$('input[data-pk=' + primary_key + '][data-name="lab_location"]').val(new_location);
            }
        })
        .fail(function() {
        	alert("Error! You might input something illegal.")
        });	
        event.preventDefault();
	});


/* When user clicks the Replace button of every device item */
	$('.btn-hidden-replace').on('click', function(event) {
		primary_key = $(this).attr('data-pk');
		$('#replacement_modal').modal({backdrop: "static"});
	});

	$('#submit_rep').on('click', {pk:primary_key}, function(event) {
  		$.post('/device_replacement/', {pk: primary_key, replacement_pk:$('#replacement_pk').val(), 'csrfmiddlewaretoken': token})
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


/* When user clicks the Received button of every device item */
	$('.btn-hidden-receive').on('click', function(event) {
		primary_key = $(this).attr('data-pk');
		tb_status = $(this).parent()
  		$.post('/edit_request/', {pk: primary_key, target: 'status', target_value:'REC', 'csrfmiddlewaretoken': token, ov:'Ordered'})
  			.done( function(response) {
  				tb_status.html('Received');
  				// console.log($(this));
  			});
  	});

	// $('select').each(function(index) {
		// console.log(index + ': ' + $(this).text());
	// });


	$(window).on('load', function() {

		setTimeout(function() {
			if ( window.location.pathname == '/') {  /* ONLY detect sign-in state on the navigation page. */
			    var auth2 = gapi.auth2.getAuthInstance();
			    var guser = auth2.currentUser.get();
			    var profile = guser.getBasicProfile();
			    console.log(window.location);
			    console.log('Current User: ', guser);
			    console.log('User profile: ', profile);
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

			  //   	auth2.signIn().then(function(){
					//   	var guser2 = auth2.currentUser.get();
					//   	var profile = guser2.getBasicProfile();
					//   	console.log('Current User: ', guser2);
					//   	console.log('Current Username: ', profile.getName());
					// 	var name = profile.getGivenName();
					//     $('#signed_name').text("Welcome, " + name + "!");
					//     $('#signout').css('visibility', 'visible');
					//     // onSignIn(guser);
					// });
			    }
			} else {
				gapi.load('auth2', function() {
					auth2 = gapi.auth2.init({
						client_id: '613024433503-bplsrhovk0a60ng7lrlb6slg49ta320h.apps.googleusercontent.com',
					    scope:'profile email',
					});
					console.log(window.location, '\nauth2: ', auth2);
					var guser = auth2.currentUser.get();
					console.log('User: ', guser);
					var profile = guser.getBasicProfile();
				 //  auth2.signIn().then(function(){
				 //  	var guser2 = auth2.currentUser.get()
				 //  	var profile = guser2.getBasicProfile();
				 //  	console.log('Current User: ', guser2);
				 //  	console.log('Current Username: ', profile.getName());
					// var name = profile.getGivenName();
				 //    $('#signed_name').text("Welcome, " + name + "!");
				 //    $('#signout').css('visibility', 'visible');
				 //    // onSignIn(guser2);
				 //  });
				 	if ( profile === undefined ) {
			    		// window.location.replace("https://accounts.google.com/signin/oauth?client_id=613024433503-bplsrhovk0a60ng7lrlb6slg49ta320h.apps.googleusercontent.com&as=11abbfd16a3d1ede&destination=http://xiawang.bej:8080&approval_state=*AH-1Ng3728E7_XHAWrYGZDv7wKsXH2NYLw7aSahU09SpwhQw2K6YL361iwJ_d31kIKy6LnVFisafGLSze9ZjYE_RYQvdMZCTQe4rpJuJMzl98A9_qJG9H2FMbzIt50Op2Ym3KzYg3WJT4nHoXiI6tC8saEvsxYUjog0XRVb2-XcKtxU0oR1Fzsy_6Z_Pc3Cc6xvJv-pmWuQWLZ__9XxDTJu4C3LgQcCCUP4U0MkmCX29cYYzdh6fEwA7iMWIv7rhjivznXn-Soy7anKX2kJM3YoxYUkEcv4ZjgDFdPVQbDPdxlQ2aTpghTfuTK-aEut6pfizx9Mcot3GjuCNpVv-n8_vxUrZfY2t89u0pCk5KGDKp0QMAy4bZ0FG_8rBWbo7BPiHthxyylT4ieUW9UJ7w-UvuB5h_WdSKjgaicxM6GNeg474I6--CB8Sz7RjQC6KkoDpSQWhXJTMN8uNagvKLm-nWqqimwQKyYJy-u5nWpLFfFtYKnQ3cSSDSG58dOh5vAA_TV4PROeUH_BJUxjXojJajVyoKuXe1V0UIFbqDcdQnM9mb8gzCcc%3D&xsrfsig=AHgIfE9IrH541bWSBsw2lzTCF0fEh6J4Og");
			    		// $(location).attr('target', "_blank");
			    		// $(location).attr('href', "https://www.baidu.com");
			    		// auth2.signIn();
			    		$('#g-signin').trigger("click");
			    	}
				});
			}

		}, 500);  // Set latency to make sure the login status is obtained after the page loaded completely.

		if ( window.location.pathname == '/request_disposal/') {
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
					console.log('Newest currency(USD -> CNY): ', data.rates.CNY);
					currency_rate = data.rates.CNY;
				}
			});
		}

	});

});