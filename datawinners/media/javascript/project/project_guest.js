
$(document).ready(function() {

    var showSuccessMsg = function(message) {
        $('#message').remove();
        $('<div id="message" class="success_message success-message-box">' + message + '</div>').insertBefore($('#message_text'));
    }
    var showErrorMsg = function(message) {
        $('#message').remove();
        $('<div id="message" class="error_message message-box clear-left">' + message + '</div>').insertBefore($('#message_text'));
    }

    var uploader = new qq.FileUploader({
        // pass the dom node (ex. $(selector)[0] for jQuery users)
        element: document.getElementById('file_uploader'),
        // path to server-side upload script
        action: import_guest_link,
        params: {},
        onSubmit: function () {
            $.blockUI({ message: '<h1><img src="/media/images/ajax-loader.gif"/><span class="loading">' + gettext("Just a moment") + '...</span></h1>', css: { width: '275px'}});
        },
        onComplete: function (id, fileName, responseJSON) {
            $.unblockUI();
            $('#message').remove();
            if ($.isEmptyObject(responseJSON) || responseJSON.success == false) {
                showErrorMsg(responseJSON.message);
            } else {
                showSuccessMsg(responseJSON.message);
                $("#guest_table").dataTable().fnReloadAjax();
            }
        }
    });

    var get_warning_dialog_options = function(waring_dialog_id, table, url, selected_ids, all_selected) {
        return {container: waring_dialog_id,
            continue_handler: function () {
                DW.loading();
                $.ajax({
                        type: 'POST',
                        url: url,
                        data: {
                            'id_list': JSON.stringify(selected_ids),
                            'all_selected': all_selected,
                            'email_status_filter': $('#email_status').val()
                        },
                        success: function (response) {
                            var data = JSON.parse(response);
                            if (data.success) {
                                showSuccessMsg(data.success_message);
                                table.fnReloadAjax();
                            } else {
                                showErrorMsg(data.error_message);
                            }
                        },
                        error: function (e) {
                            showErrorMsg(e.responseText);
                        }
                    }
                )
                ;

                return false;
            },
            title: gettext("Confirmation"),
            cancel_handler: function () {
            },
            height: 170,
            width: 550
        };
    }

    var handle_send_emails = function(table, selected_ids, all_selected) {
        var warning_dialog = new DW.warning_dialog(get_warning_dialog_options('#warning_dialog', table, project_guests_send_email_link, selected_ids, all_selected));
        warning_dialog.show_warning();
        warning_dialog.ids = selected_ids;
    }

    var handle_delete_guests = function(table, selected_ids, all_selected) {
        var warning_dialog = new DW.warning_dialog(get_warning_dialog_options('#warning_dialog_delete', table, delete_project_guests_link, selected_ids, all_selected));
        warning_dialog.show_warning();
        warning_dialog.ids = selected_ids;
    }

    $(function(){
        function col(header_class_name){
            return $('#guest_table th.' + header_class_name).index('#guest_table th');
        }
        $("#guest_table").dwTable({
            "concept": "Project Guest",
            "sAjaxSource": project_guests_ajax_url,
            "dData": function() { return $('#email_status').val()},
            "sAjaxDataIdColIndex": 1,
            "bServerSide": true,
            "sDom": 'ip<"toolbar">rtipl',
            "oLanguage": {
                "sEmptyTable": $('#no_registered_subject_message').clone(true, true).html()
            },
            "aoColumnDefs": [
                {"aTargets": [0], "sWidth": "30px"}
            ],
            "actionItems" : [
                {"label":"Send survey email", handler:handle_send_emails, "allow_selection": "multiple"},
                {"label":"Delete guest(s)", handler:handle_delete_guests, "allow_selection": "multiple"}
            ],
            "aaSorting": [ [ col("name"), "asc"] ]
        });
        $("#guest_table").dataTable().fnSetColumnVis(1, false);
        _add_email_send_filter_select();
    });

    function _add_email_send_filter_select() {
        var s = $("<select id=\"email_status\"/>");
        $("<option />", {value: 'all', text: 'Show All'}).appendTo(s);
        $("<option />", {value: '1', text: 'Email Send'}).appendTo(s);
        $("<option />", {value: '0', text: 'Email Not Send'}).appendTo(s);
        s.appendTo('div.toolbar');
        s.change(function() {
            $("#guest_table").dataTable().fnReloadAjax();
        });
        $('div.toolbar').css('float', 'right');
    }



});