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

                        /** Refresh company filter */
                        refresh_company_list();

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
    
    let formData = new FormData(form);
    
    /** Validate inputs */
    let formValid = true;
    if (form.company_name.value == ""){
        $('#import_preloader').removeClass("show").addClass("hide");       
        $(form.company_name).removeClass("valid").addClass("invalid");

        formValid = false;
    }

    if (form.sales_file_input.value == ""){
        $('#import_preloader').removeClass("show").addClass("hide");
        $(form.sales_file_input).removeClass("valid").addClass("invalid");
     
        formValid = false;
    }

    if (!(formValid)){
        return
    }

    /** Send the file via ajax  */
    $.ajax({
        url: "http://localhost:8000/dashboard/import/",
        type: 'POST',
        data: formData,
        dataType: 'json',
        success: function (data) {

            /** Clear fields */
            $('#id_company_name').val('');
            $('#sales_file').val('');
            $('#sales_file_input').val('');

            /** Show success Modal */
            var modal_success = M.Modal.getInstance(import_success_modal);
            modal_success.open();

            /** Refresh the process list queue */
            refresh_proc_list(data.proc_data);

            /** Hide preloader */
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

function refresh_company_list(){

    $.ajax({
        url: "http://localhost:8000/dashboard/company_list",
        type: 'GET',
        success: function (data) {
            $('#company_select').html(data);
            $('select#company').formSelect();

            $('select#company').on('change', function(obj) {
                let id_company = $('select#company').val();
                console.log($('select#company').val());
                if (id_company != 'undefined'){
                    /** Show filter options */
                    $('#info_select_company').removeClass("show").addClass("hide");
                    $('#row_product').removeClass("hide").addClass("show");
                    $('#row_category').removeClass("hide").addClass("show");

                    refresh_category_list(id_company);
                }
            });

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

function refresh_category_list(company){

    $.ajax({
        url: "http://localhost:8000/dashboard/category_list?company="+company,
        type: 'GET',
        success: function (data) {
            $('#category_select').html(data);
            $('select#category').formSelect();

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
     * Handle Search Filter submit
     */
    
    
    $('#data_table_preloader').removeClass("hide").addClass("show");
    
    var formData = new FormData(form);

    let company = form.company.value;
    let product_name = form.product_name.value;
    let category = $('#category').val();
    let use_category = $('#use_category:checked').val();
    let use_product = $('#use_product:checked').val();

    /** Validate inputs */
    let formValid = true;
    if (form.company.value == ""){
        $('#data_table_preloader').removeClass("show").addClass("hide");       
        $('#company_empty').removeClass("valid").addClass("invalid");

        alert('Please, select a company')
        return
    }

    $.ajax({
        url: "http://localhost:8000/dashboard/filter/?company="+company+
                                                     "&product_name="+product_name+
                                                     "&category="+category+
                                                     "&use_category="+use_category+
                                                     "&use_product="+use_product,
        type: 'GET',
        success: function (data) {

            //Scroll to Results
            $([document.documentElement, document.body]).animate({
                scrollTop: $("#results_ss").offset().top
            }, 1000);

            //Hide preloader
            $('#data_table_preloader').removeClass("show").addClass("hide");

            //Populate data
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
