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


/* jQury functions start from here. */
$(document).ready(function(){
	// $("th, td").each (function(index) {
	// 	console.log(index + ": " + $(this).text());
	// });
	// $.fn.editable.defaults.mode = 'inline';
	var token = $('input[name="csrfmiddlewaretoken"]').prop('value');
	$('a[data-type="text"]').editable({
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
		    return params;
		},
        // emptytext:'Input',
        success: function(response, newValue) {
    		// if (response.status == 200) { // This needs to be defined by server definitely.
    			// alert('oldValue: ' + $(this).text() +'\nnewValue: ' + newValue);
    		// }
    			if ($(this).attr('data-name') == 'ex_rate') {
    				var rate = newValue;
    				var preMatching = $(this).parent().prev().find('a');
    				var nextMatching = $(this).parent().next().find('a');
    				// var price_c = $(this).parent().prev().text();
    				var price_c = preMatching.editable('getValue', true);
    				var price_u = nextMatching.editable('getValue', true);
    				console.log(price_c + price_u)
    				// if ( price_c != 'Empty') {  // for the text() method inside editable, will identify the empty value as string 'Empty'.
    				if ( price_c ) {
    					price_u = (price_c / rate).toFixed(2);
    					// This is for the database restore.
    					$(nextMatching).editable('submit', {
    						// ajaxOptions: {
					             // dataType: 'json', 
					             // headers: { "X-CSRFToken": token }
						    // }, 
    						data: {
    							'value': price_u,
    							// 'csrfmiddlewaretoken': token
    						}
    					});
    					// This is for the UI presentation.
    					$(nextMatching).editable('setValue', price_u, false);    					
    				} else if ( price_u ) {
    					price_c = (price_u * rate).toFixed(2);
    					$(preMatching).editable('submit', {
    						// ajaxOptions: {
					             // dataType: 'json', 
					             // headers: { "X-CSRFToken": token }
						    // }, 
    						data: {
    							'value': price_c,
    						}
    					});
    					$(preMatching).editable('setValue', price_c, false);       
    				}
    			}
		},
		error: function(response, newValue) {
			if (response.status == 500) {
				return 'submit might be illegal, try again.';
			} else {
				return response.responseText;
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


/* Handle the various select options */
	var primary_key = 'hello world';
	var status = '';
    $('select').on('change.sel', 
    	// { pk: $(this).attr('data-pk') },
    	function(event) {
    		console.log(this);
    		console.log($(this));
    		var data =  { pk: $(this).attr('data-pk'), };
    		primary_key = data.pk;
    		status = $(this).val();
			switch ( status) {
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
					// 	// console.log('I am inside the on listener...............................................................My index is: ', index);
					// 	var ele = $(this);
					// 	console.log(ele);
				 //  		// alert('index' + $(this).index());
				 //  		console.log('data.pk', event.data.pk);
				 //  		console.log('target', event.target);
				 //  		console.log('currentTarget', event.currentTarget);
				 //  		console.log('relatedTarget', event.relatedTarget);
				 //  		console.log('delegateTarget', event.delegateTarget);
				 //  		console.log('result', event.result);
				 //  		console.log('which', event.which);
				 //  		console.log('type', event.type);
				 //  		console.log('timestamp', event.timeStamp);
				 //  		console.log('pageX + pageY', event.pageX, event.pageY);
				 //  		console.log('offsetX + offsetY', event.offsetX, event.offsetY);
				 //  		console.log('-------------------------------------------------------------------------------');
				 //    });	


					console.log('Primary key of this event: ', 
						// event.data.pk, 
						data.pk
						// $(this).attr('data-pk')
						);

					break;
				case 'APP': 
					$.post('/edit_request/', {pk: primary_key, target: 'approve_date', target_value:event.timeStamp, 'csrfmiddlewaretoken': token})
					// $(this).parent().prevAll().find('a[data-name="po_number"]').trigger("click");
					var poi = $(this).parent().prevAll().find('a[data-name="po_number"]');
					console.log(poi, poi.val(), poi.text());
					if ( poi.text() == 'Empty') {
					    setTimeout(function() {
					        poi.editable('show');
					    }, 200);						
					}

					break;
				case 'AVA': 
					$('#allocation_modal').modal('show');

					break;
				case 'ASS': 

					$('#allocation_modal').modal('show');
					break;
				default: 


			}

			// $('#confirm_modal').on('hide.bs.modal', data, function(event) {
			// 	var mod = $(this);
			// 	console.log(mod);
			// 	alert('primary key of this element: ' + event.data.pk);
			// 	// console.log('target', event.target);
			// 	// console.log('currentTarget', event.currentTarget);
			// 	// console.log('relatedTarget', event.relatedTarget);
			// 	// console.log('delegateTarget', event.delegateTarget);
			// 	console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
			// });		
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
  		$.post('/edit_request/', {pk: primary_key, target: 'status', target_value:'REF', 'csrfmiddlewaretoken': token})
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
	});


/* Dynamically create the input box based on the devices' quantity user requested. */
	$('#allocation_modal').on('shown.bs.modal', {pk:primary_key, st:status}, function(event) {
		var td_quantity = $('a[data-pk=' + primary_key + ']').first().parent().prev()
		console.log($(td_quantity));
		var quantity = td_quantity.text();
		// console.log('User requested ' + quantity + ' devices.');
		var td_model = $(td_quantity).prev().prev();
		var model = td_model.text();
		if (status == 'ASS') {
			$('#inst').html('You can now allocate device to users. The devices can be the public ones in lab or newly purchased devices.');
			$('#title').html('Allocate Device');
		} else {
			$('#inst').html('Register the newly purchased devices and put them into PUBLIC pool of our lab.');
			$('#title').html('Make Device Public');
		}
		for (i = 0; i < quantity; i++) {
			$('#allocation_table').append('<tr><td style="padding:10px">' + model + '</td><td><input type="text" class="form-control minput" placeholder="input device id" name="sn" required></td></tr>');
		}
		$('#allocation_table').append('<tr><td><input type="hidden" name="pk" value=' + primary_key + '></td></tr>');
		$('#allocation_table').append('<tr><td><input type="hidden" name="status" value=' + status + '></td></tr>');

 	});


/* When user clicks Submit on the allocation modal. */
	// $('#submit').on('click', {pk: primary_key}, function(event) {
	// 	$.post('')
	// });

	// $('select').each(function(index) {
		// console.log(index + ': ' + $(this).text());
	// });


	
});