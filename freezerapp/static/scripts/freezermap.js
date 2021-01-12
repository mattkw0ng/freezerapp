var grids = $.map($(".grid"), function(n, i){
  return n.id;
});

function initGrid() {
	grids.forEach(function(grid) {
		new_grid =  new Muuri('.'+grid);
	});
}

function verify(freezer) { //add more secure method later
	location.href = '/edit-freezer/'.concat(freezer);

	// var admins = {'matthew': 'password','matt': 'pass' ,'jerry': 'terry'};
	// var person = prompt("Please enter your username");
	// if(person in admins){
	// 	var password = prompt("Please enter your password")
	// 	if(password == admins[person]){
	// 		location.href = '/edit-freezer/Mr. Freeze'; 
	// 	}else{
	// 		alert("incorrect password");
	// 	}
	// }else if(person){
	// 	alert("Error: admins only");
	// }
}

initGrid();