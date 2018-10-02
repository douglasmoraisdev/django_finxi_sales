function update_proc_status() {
    /**
     * Update file process status list
     */

    // execute ajax for each active proc pid
    // look for proc_ids
    $("#proc_ids li").each(function (index, element) {

        let pid = $(element).text();

        $.ajax({
            type: "GET",
            url: "http://localhost:8000/dashboard/proc_state?job=" + pid,
            success: function (msg) {

                //$("#process_status_list li#"+pid).remove();

                let json_msg = JSON.parse(msg);
                let id = json_msg.id;
                let status = json_msg.status;
                let status_message = '';

                // Success or Pending
                if (typeof status === 'string' || status instanceof String) {
                    status_message = status;

                    // remove from query list
                    if (status == 'SUCCESS') {
                        $("#proc_ids li#" + pid).remove();
                    }

                } else {
                    status_message = status.current + '/' + status.total;
                }

                let search_li = $("#process_status_list li#" + pid);

                if (search_li.length > 0) {

                    $(search_li).html(
                        '<li id=' + id + '>\
                            <span class="tab">Proc id: '+ id + '</span>\
                            <span class="tab">Status: '+ status_message + '</span>\
                        </li>'
                    );


                } else {

                    $("#process_status_list").append(
                        '<li id=' + id + '>\
                            <span class="tab">Proc id: '+ id + '</span>\
                            <span class="tab">Status: '+ status_message + '</span>\
                        </li>'
                    );

                }

                console.log(msg);
            }
        });

    })
}

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

}
    

function import_file(form) {
    /**
     * Handle Import Form Submit
     */

    var formData = new FormData(form);
    
    $.ajax({
        url: "http://localhost:8000/dashboard/import/",
        type: 'POST',
        data: formData,
        success: function (data) {
            var modal_success = M.Modal.getInstance(import_success_modal);
            modal_success.open();
        },
        error: function (data) {
            var modal_fail = M.Modal.getInstance(import_fail_modal);
            modal_fail.open();
        },
        cache: false,
        contentType: false,
        processData: false,
    });
    

};