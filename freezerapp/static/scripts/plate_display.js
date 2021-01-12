function fillnav(id,plate_name){
	var container = document.getElementById(id);
	let letters = ['A','B','C','D','E','F','G'];
	var row = document.createElement('div');
	var i;
	row.className = 'row';

	var front = document.createElement('div');
	front.innerHTML = 'front';
	front.className = 'col-xs-x navcell';
	front.setAttribute('style',"writing-mode: vertical-rl;");
	row.appendChild(front);

	for(i = 0 ; i <letters.length ; i++){
		var cell = document.createElement('div');
		cell.className = 'col-xs-x navcell';
		var button = document.createElement('button');
		button.innerHTML = letters[i];
		button.className = 'btn btn-outline-primary';
		var tag = '#'+plate_name+letters[i];
		button.setAttribute('onclick','window.location.href = "'+tag+'"');
		cell.appendChild(button);
		row.appendChild(cell);
	}

	var back = document.createElement('div');
	back.innerHTML = 'back';
	back.className = 'col-xs-x navcell';
	back.setAttribute('style',"writing-mode: vertical-rl;");
	row.appendChild(back);

	container.appendChild(row);
}

/*
<div class="dropdown">
  <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
    Dropdown button
  </button>
  <div class="dropdown-menu">
    <form class="px-4 py-3">
      <div class="form-group">
        <label for="exampleDropdownFormEmail1">Email address</label>
        <input type="email" class="form-control" id="exampleDropdownFormEmail1" placeholder="email@example.com">
      </div>
      <div class="form-group">
        <label for="exampleDropdownFormPassword1">Password</label>
        <input type="password" class="form-control" id="exampleDropdownFormPassword1" placeholder="Password">
      </div>
      <div class="form-check">
        <input type="checkbox" class="form-check-input" id="dropdownCheck">
        <label class="form-check-label" for="dropdownCheck">
          Remember me
        </label>
      </div>
      <button type="submit" class="btn btn-primary">Sign in</button>
    </form>
    <div class="dropdown-divider"></div>
    <a class="dropdown-item" href="#">New around here? Sign up</a>
    <a class="dropdown-item" href="#">Forgot password?</a>
  </div>
</div>


function filltable(id, plate_name){
	// letters to use for the plate location
	let letters = ['A','B','C','D','E','F','G'];
	var table = document.getElementById(id);
	var i;
	// create header and fill with plate_name
	var header = document.createElement('div');
	header.className = "row"
	var header_cell = document.createElement('div');
	header_cell.innerHTML = plate_name;
	header_cell.className = "col header";
	header.appendChild(header_cell);
	// add anchor
	var head_anchor = document.createElement('a');
	var head_tag = ''+plate_name+letters[0];
	head_anchor.setAttribute("name",head_tag);
	header.appendChild(head_anchor);

	table.appendChild(header);

	for(i = 0 ; i < 7 ; i++){
		var j;
		for(j = 0 ; j<8 ; j++){
			// location: plate_name + i + j  --> P01A
			var row = document.createElement('div');
			row.className = "row"

			var count = document.createElement('div');
			var verify = document.createElement('div');
			count.className = 'col- hovercell';
			count.innerHTML = letters[i]+(j+1);

			verify.className = 'col- hovercell';
			verify.innerHTML = 'v';

			row.appendChild(count);
			row.appendChild(getbutton("sample-name"));
			row.appendChild(verify);

			table.appendChild(row);
		}
		// 'br' is the row portion and 'eak' is the column: combined to form BREAK (necessary for centering text)
		var br = document.createElement('div');
		var eak = document.createElement('div');

		br.id = 'break'+i;
		br.className = "row";
		eak.className = "col break";
		eak.innerHTML = '- '+plate_name+' '+letters[i+1]+' -';
		
		br.appendChild(eak);
		//create anchor tag for page jumps
		if(i<7){
			var anchor = document.createElement('a');
			var tag = ''+plate_name+letters[i+1];
			anchor.setAttribute("name",tag);
			br.appendChild(anchor);
		}	
		table.appendChild(br);
	}
	table.removeChild(document.getElementById('break6')); //remove last break
}

filltable('table1','P01');
filltable('table2','P02');
*/
