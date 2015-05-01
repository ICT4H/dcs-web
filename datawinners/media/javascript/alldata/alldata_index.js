$(function(){
     var reminderAddDialogOptions = {
                    link_selector: "#undelete_project_section",
                    title: "Undone Delete",
                    dialogDiv: "#reminder_add_dialog",
                    successCallBack: function(callback){
                        callback();
                        return true;
                    },
                    open: function(event, ui){
                        //hide the close button
                        $(".ui-dialog-titlebar-close", ui.dialog).hide();
                    },
                    width:500
                };
     new DW.Dialog(reminderAddDialogOptions).init().initializeLinkBindings();
});