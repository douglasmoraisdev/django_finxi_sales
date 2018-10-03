function update_proc_status() {
    /**
     * Update file process status list
     */

    // execute ajax for each active proc pid
    // look for proc_queue
    $("#process_status_list").removeClass("show").addClass("hide");
    $("#no_files_queue").removeClass("hide").addClass("show");
    
    $("#proc_queue li").each(function (index, element) {
        
        let pid = $(element).text();
        
        $("#process_status_list").removeClass("hide").addClass("show");
        $("#no_files_queue").removeClass("show").addClass("hide");


        $.ajax({
            type: "GET",
            url: "http://localhost:8000/dashboard/proc_state?job=" + pid,
            success: function (msg) {

                let json_msg = JSON.parse(msg);
                let id = json_msg.id;
                let status = json_msg.status;
                let filename = $("#proc_queue li#"+id).attr('name'); //get from item list queue
 
                let search_li = $("#process_status_list li#" + pid);
                    
                let percent = status.current;

                // Success or Pending
                if (typeof status === 'string' || status instanceof String) {

                    // remove from query list
                    if (status == 'SUCCESS') {
                        $("#proc_queue li#" + pid).remove();
                        percent = 100;

                        var modal_complete = M.Modal.getInstance(import_complete_modal);
                        $('#import_complete_message').html('A new file was proccessed succefully!')
                        modal_complete.open();
                        $("#" + pid).remove();
                    }

                }                

                if (search_li.length > 0) {

                    
                    $(search_li).html(
                        "<li id=" + id + ">Processing File '" + filename + "'...\
                            <div class='progress'>\
                                <div class='determinate' style='width: "+ percent + "%'></div>\
                            </div>\
                        </li>"
                    );


                } else {

                    $("#process_status_list").append(
                        "<li id=" + id + ">Processing File '" + filename + "'...\
                            <div class='progress'>\
                                <div class='determinate' style='width: "+ percent + "%'></div>\
                            </div>\
                        </li>"
                    );

                }
            

                console.log(msg);
            }
        });

    })
};

function switch_filters(elem){
    /**
     * Turn on/off a filter input
     */

    let target = $(elem).attr('target');

    /** Set enabled/disabled to a element */
    $('#'+target).prop("disabled", !($(elem).prop("checked")));    

    /** Reset the Materialized Select if any */
    if ( $('#'+target).prop('nodeName') == 'SELECT'){
        $('#'+target).formSelect();
    }

};
    
function import_file(form) {
    /**
     * Handle Import Form Submit
     */

    
    
    $('#import_preloader').removeClass("hide").addClass("show");
    
    var formData = new FormData(form);
    /** Validate inputs */

    if ((form.sales_file.value == "") || (form.company_name.value == "")){
        $('#import_preloader').removeClass("show").addClass("hide");
        alert("Please, fill all fields!");
        return
    }

    $.ajax({
        url: "http://localhost:8000/dashboard/import/",
        type: 'POST',
        data: formData,
        dataType: 'json',
        success: function (data) {
            var modal_success = M.Modal.getInstance(import_success_modal);
            modal_success.open();
            refresh_proc_list(data.proc_data);
            $('#import_preloader').removeClass("show").addClass("hide");

        },
        error: function (data) {
            var modal_fail = M.Modal.getInstance(import_fail_modal);
            modal_fail.open();
            $('#import_preloader').removeClass("show").addClass("hide");
        },
        cache: false,
        contentType: false,
        processData: false,
    });
    

};

function refresh_proc_list(items){

    $("#proc_queue").html("");

    $(items).each(function(index, item){

        console.log('appending ' + item);

        $("#proc_queue").append(
            '<li id="' + item + '" name="' + item + '">' + item + '</li>'
        );

    });

};

function search_filter(form) {
    /**
     * Handle Import Form Submit
     */

    
    
    $('#data_table_preloader').removeClass("hide").addClass("show");
    
    var formData = new FormData(form);
    /** Validate inputs */

    /*
    if ((form.sales_file.value == "") || (form.company_name.value == "")){
        $('#import_preloader').removeClass("show").addClass("hide");
        alert("Please, fill all fields!");
        return
    }
    */

    $.ajax({
        url: "http://localhost:8000/dashboard/filter/",
        type: 'POST',
        data: formData,
        success: function (data) {

            //return new Promise(resolve => setTimeout(resolve, 2));

            $('#data_table_preloader').removeClass("show").addClass("hide");

            $('#data_table').html(data);
  
        },
        error: function (data) {
            alert('A wild error appear');
            $('#data_table_preloader').removeClass("show").addClass("hide");
        },
        cache: false,
        contentType: false,
        processData: false,
    });
    

};
