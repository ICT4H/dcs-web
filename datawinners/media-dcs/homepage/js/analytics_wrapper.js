var DW = {};

$.ajaxSetup ({
    // Disable caching of AJAX responses
    cache: false
});

//Google analytics event tracking
DW.trackEvent = function(category, action, label, value){
    if (typeof _gaq !== 'undefined') {
        if(typeof label === 'undefined'){
            _gaq.push(['_trackEvent', category, action]);
        }
        else{
            if(typeof value === 'undefined'){
                _gaq.push(['_trackEvent', category, action, label]);
            }
            else{
                _gaq.push(['_trackEvent', category, action, label, value]);
            }
        }
    }

};