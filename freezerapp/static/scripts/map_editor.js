function initGrid() {
    let count = 0;
    grids.forEach(function(grid) {
            muuri_grids[count++] =  new Muuri('.'+grid, {
            dragEnabled: true,
            layoutOnInit: false,
            dragContainer: document.body,
            dragSort: function () {
                return muuri_grids.concat([editor_grid]) 
            }
          }).on('receive', function (data) {
              console.log(data)
              cloneMap[data.item._id] = {
                item: data.item,
                grid: data.fromGrid,
                index: data.fromIndex
              };
          }).on('send', function (data) {
              delete cloneMap[data.item._id];
        }).on('dragReleaseStart', function (item) {
              var cloneData = cloneMap[item._id];
              if (cloneData) {
                delete cloneMap[item._id];

                var clone = cloneData.item.getElement().cloneNode(true);
                clone.setAttribute('style', 'display:none;');
                clone.setAttribute('class', 'item code-1');
                clone.children[0].setAttribute('style', '');
         
                cloneData.grid.add(clone, {index: cloneData.index});
                cloneData.grid.show(clone);
              }
        });
        
    });

    // Editor grid
      editor_grid = new Muuri('.grid-0', {
          dragEnabled: true,
          layoutOnInit: false,
          dragContainer: document.body,
          dragStartPredicate: function (item, hammerEvent) {
               // Don't drag if target is button
            if (hammerEvent.target.matches("i")) {
                return false;
            }
               // handle Drag
            return true;
        },
          dragSort: function () {
              return muuri_grids
          }
      }).on('receive',function(data){
          var item = data.item.getElement();
          console.log("removed: "+data.item._id);
          editor_grid.remove(item,{removeElements: true});
      });

      // Initialize layout
      muuri_grids.forEach(function(muuri_grid) {
          muuri_grid.layout(true);
      });
      editor_grid.layout(true);
}

function saveAll(freezer_name){
    var size_check = true;

    grids.forEach(function(grid) {
        if(!checkSize(grid)){
            size_check = false;
        }
    });

    if(size_check){
        let layouts = [];
        muuri_grids.forEach(function(muuri_grid) {
            layouts.push(serializeLayout(muuri_grid));
        })

        $.ajax({
            url: "/edit-freezer/".concat(freezer_name),
            type: "POST",
            data: JSON.stringify(layouts),
            contentType: "application/json; charset=utf-8",
            success: function(dat) {
                location.href = dat;
            }
        });

    }else{
        alert("Please double check the number of elements before saving");
    }
    
}

// Saving Layout into a list of dictionaries
function serializeLayout(grid) {
    
    // keys: vacancy list and type
    //iterate through all items of grid
      let list = grid.getItems().map(function (item) {
          item_dict = {};
          item_dict['list'] = [];
          //iterate through the children of the items
          let children = item.getElement().childNodes[1].getElementsByClassName('sub-item')

          Array.from(children).forEach(function(child) {
              split = child.id.split('.');
              item_dict['type'] = split[0];
              item_dict['list'].push(split[1]);
          });
        return item_dict;
      });

      return list;
}

function checkSize(id){
    var container = document.getElementById(id);
    if(container.getElementsByClassName('item').length != 10){
        alert(id + " has an invalid number of items");
        return false;
    }
    return true;
}

// <div class="item-content">
//   <div class="splitcell sub-item" id="box.B##">
//       <i class="far fa-edit edit-btn" onclick="edit(this)"></i>
//       <p contentEditable="false" class="editcontent">B##</p>
//   </div>
//   <div class="splitcell sub-item" id="box.B##">
//       <p contentEditable="false" class="editcontent">B##</p>
//   </div>
//   <div class="splitcell sub-item" id="box.B##">
//       <p contentEditable="false" class="editcontent">B##</p>
//   </div>
//   <div class="splitcell sub-item" id="box.B##">
//       <p contentEditable="false" class="editcontent">B##</p>
//   </div>
// </div>

// Automatically fills the compartment given a single start point
function edit(dom){
    let regex = new RegExp('[PTKB][0-9][0-9]');
    let text = prompt("Enter new name: ");
    if(text){
        if(regex.test(text)){
            // by default use plate
            let type = 'plate.';
            let limit = 4;
            if(text.charAt(0) == 'T'){
                type = 'tube.';
            }else if (text.charAt(0) == 'B'){
                type = 'box.';
            }
            // extract the number from the data
            let temp = text.slice(1,3);
            let start = parseInt(temp, 10);

            // iterate through each rack of the compartment
            $(dom.parentNode.parentNode).children('.sub-item').each(function() {
                let rack_name = text.charAt(0).toString();
                if(start < 10){
                    rack_name = rack_name.concat('0', start.toString());
                } else {
                    rack_name = rack_name.concat(start.toString());
                }
                // change rack id
                $(this).attr('id', type.concat(rack_name));
                // change text
                $(this).children('p').html(rack_name);
                start ++;
            });
        }else{
            alert("Invalid name, must follow pattern: [PTKB][0-9][0-9]")
        }
    }
}

function add_cabinet(freezer_name){
  let check = confirm("Add a new cabinet to this freezer?")
  if(check){
    $.ajax({
        url: "/edit-freezer/".concat(freezer_name),
        type: "POST",
        data: JSON.stringify({'command': 'add_cabinet'}),
        contentType: "application/json; charset=utf-8",
        success: function(dat) {
            location.href = dat;
        }
    });
  }
}

var editor_grid;
var cloneMap = {};

var grids = $.map($(".grid"), function(n, i){
    if(n.id != "grid-0"){
        return n.id;
    }
});
var muuri_grids = [];

initGrid();
